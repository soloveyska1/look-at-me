#!/usr/bin/env python3
"""
CINEMA VFX TOOLKIT
Профессиональные функции для "СМОТРЕЛА" — Саймурр

Библиотека VFX эффектов уровня Hollywood production.
Все функции оптимизированы для MoviePy/NumPy.

Author: COLOR GRADING & VFX SUPERVISOR
Level: $500,000 Music Video Production
"""

import numpy as np
import cv2
from scipy.ndimage import gaussian_filter1d
from typing import Tuple, Optional, Dict, List


# ============================================================
# COLOR GRADING FUNCTIONS
# ============================================================

def cinematic_bw_conversion(frame: np.ndarray,
                            red_weight: float = 0.30,
                            green_weight: float = 0.59,
                            blue_weight: float = 0.11) -> np.ndarray:
    """
    ПРОФЕССИОНАЛЬНАЯ конверсия в B&W (luminosity-based).

    НЕ простая десатурация! Сохраняет контраст кожи и глаз.
    Основано на методике Roger Deakins (Blade Runner 2049).

    Args:
        frame: RGB frame (H, W, 3) uint8
        red_weight: вес красного канала (кожа)
        green_weight: вес зелёного канала (глаза, детали)
        blue_weight: вес синего канала (тени, атмосфера)

    Returns:
        Grayscale frame в RGB (H, W, 3)
    """
    img = frame.astype(np.float32) / 255.0

    # Weighted luminosity
    gray = (img[:,:,0] * red_weight +
            img[:,:,1] * green_weight +
            img[:,:,2] * blue_weight)

    # Clip
    gray = np.clip(gray, 0, 1)

    # Convert back to RGB (all channels same)
    result = np.stack([gray, gray, gray], axis=2)

    return (result * 255).astype(np.uint8)


def apply_s_curve_contrast(img: np.ndarray,
                          toe: float = 0.10,
                          shoulder: float = 0.92,
                          strength: float = 1.2) -> np.ndarray:
    """
    S-образная кривая для кинематографического контраста.

    Args:
        img: Float image [0, 1]
        toe: точка сжатия теней (0.05-0.15)
        shoulder: точка сжатия света (0.85-0.95)
        strength: интенсивность кривой (1.0-1.5)

    Returns:
        Processed image [0, 1]
    """
    x = np.clip(img, 0, 1)

    # Shadows (0 → toe)
    shadows = np.where(x < 0.5,
                      toe + (x / 0.5) ** strength * (0.5 - toe),
                      x)

    # Highlights (shoulder → 1)
    result = np.where(shadows >= 0.5,
                     0.5 + ((shadows - 0.5) / 0.5) ** (1/strength) * (shoulder - 0.5),
                     shadows)

    return np.clip(result, 0, 1)


def apply_lift_gamma_gain(frame: np.ndarray,
                          lift: float = 0.0,
                          gamma: float = 1.0,
                          gain: float = 1.0) -> np.ndarray:
    """
    Primary color corrections как в DaVinci Resolve.

    Args:
        frame: RGB frame uint8
        lift: -1.0 to 1.0 (shadows adjustment)
        gamma: 0.5 to 2.0 (midtones)
        gain: 0.5 to 2.0 (highlights)

    Returns:
        Corrected frame uint8
    """
    img = frame.astype(np.float32) / 255.0

    # Lift (add/subtract from all values)
    img = img + lift

    # Gamma (power curve on midtones)
    img = np.power(np.clip(img, 0.001, 1.0), 1.0 / gamma)

    # Gain (multiply highlights)
    img = img * gain

    return np.clip(img * 255, 0, 255).astype(np.uint8)


def apply_contrast(frame: np.ndarray,
                  contrast: float = 1.0,
                  pivot: float = 0.5) -> np.ndarray:
    """
    Pivot-based contrast adjustment.

    Args:
        frame: RGB frame uint8
        contrast: 0.5 to 2.0
        pivot: точка вокруг которой применяется контраст (обычно 0.5)

    Returns:
        Contrasted frame uint8
    """
    img = frame.astype(np.float32) / 255.0

    # Pivot around specified point
    img = pivot + (img - pivot) * contrast

    return np.clip(img * 255, 0, 255).astype(np.uint8)


def isolate_green_eyes_pro(frame: np.ndarray,
                          sat_boost: float = 0.85,
                          lum_boost: float = 0.20,
                          glow: float = 0.15,
                          hue_center: int = 80,
                          hue_tolerance: int = 15) -> np.ndarray:
    """
    ПРОФЕССИОНАЛЬНАЯ изоляция и усиление зелёных глаз.

    Ключевой эффект для "СМОТРЕЛА": B&W фон + изумрудно-зелёные глаза.

    Args:
        frame: RGB frame uint8
        sat_boost: насыщенность зелёного (0.5-1.5)
        lum_boost: яркость зелёного (0-0.3)
        glow: интенсивность свечения (0-0.3)
        hue_center: центр зелёного оттенка в HSV (OpenCV: 0-180)
        hue_tolerance: допуск по hue

    Returns:
        B&W frame с зелёными глазами uint8
    """
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

    # Create mask for green hues (HSV hue range)
    hue_min = max(0, hue_center - hue_tolerance)
    hue_max = min(180, hue_center + hue_tolerance)

    hue_mask = ((h >= hue_min) & (h <= hue_max)).astype(np.float32)
    sat_mask = ((s >= 40) & (s <= 255)).astype(np.float32)
    lum_mask = ((v >= 30) & (v <= 220)).astype(np.float32)

    # Combine masks
    mask = hue_mask * sat_mask * lum_mask

    # Refine mask (morphological operations)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Gaussian blur для мягких краёв
    mask = cv2.GaussianBlur(mask, (7, 7), 2.0)

    # Create B&W base
    bw = cinematic_bw_conversion(frame)

    # Boost saturation and luminance в masked areas
    s_boosted = np.clip(s * (1 + sat_boost * mask), 0, 255)
    v_boosted = np.clip(v * (1 + lum_boost * mask), 0, 255)

    hsv[:,:,1] = s_boosted
    hsv[:,:,2] = v_boosted

    # Convert back to RGB
    colored = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    # Blend B&W + colored eyes
    mask_3d = np.stack([mask] * 3, axis=2)
    result = bw.astype(np.float32) * (1 - mask_3d) + colored.astype(np.float32) * mask_3d

    # Add green glow
    if glow > 0:
        result = add_green_glow(result.astype(np.uint8), mask, intensity=glow)

    return result.astype(np.uint8)


def add_green_glow(frame: np.ndarray,
                  mask: np.ndarray,
                  intensity: float = 0.15,
                  radius: int = 25,
                  color: Tuple[int, int, int] = (20, 180, 120)) -> np.ndarray:
    """
    Добавляет свечение вокруг зелёных глаз.

    Args:
        frame: RGB frame uint8
        mask: маска глаз (H, W) float [0, 1]
        intensity: интенсивность свечения
        radius: радиус blur для glow
        color: RGB цвет свечения (изумрудный)

    Returns:
        Frame с glow эффектом uint8
    """
    # Blur mask для glow
    glow_mask = cv2.GaussianBlur(mask, (radius*2+1, radius*2+1), radius/2)

    # Create colored glow layer
    glow_layer = np.zeros_like(frame, dtype=np.float32)
    for i in range(3):
        glow_layer[:,:,i] = glow_mask * color[i] * intensity

    # Add glow (additive blending)
    result = frame.astype(np.float32) + glow_layer

    return np.clip(result, 0, 255).astype(np.uint8)


# ============================================================
# VFX EFFECTS
# ============================================================

def add_film_grain(frame: np.ndarray,
                  intensity: float = 0.15,
                  size: float = 0.80,
                  static: bool = False,
                  seed: Optional[int] = None) -> np.ndarray:
    """
    Плёночное зерно (Kodak Vision3 5219 style).

    Args:
        frame: RGB frame uint8
        intensity: интенсивность зерна (0.05-0.30)
        size: размер зерна (0.5-1.5, меньше = мельче)
        static: True = статичное зерно, False = анимированное
        seed: random seed для статичного зерна

    Returns:
        Frame с зерном uint8
    """
    if static and seed is not None:
        np.random.seed(seed)

    h, w = frame.shape[:2]

    # Generate grain at lower resolution для органичности
    grain_size = int(1.0 / size)
    grain_h = max(1, h // grain_size)
    grain_w = max(1, w // grain_size)

    # Organic noise (Gaussian distribution)
    grain = np.random.normal(0, intensity * 255, (grain_h, grain_w))

    # Upscale grain with linear interpolation
    grain = cv2.resize(grain, (w, h), interpolation=cv2.INTER_LINEAR)

    # Apply grain (additive)
    grain_3d = np.stack([grain] * 3, axis=2)
    result = frame.astype(np.float32) + grain_3d

    return np.clip(result, 0, 255).astype(np.uint8)


def add_chromatic_aberration(frame: np.ndarray,
                            intensity: float = 0.003,
                            radial: bool = True) -> np.ndarray:
    """
    Хроматическая аберрация (RGB channel separation).

    Имитация anamorphic lens эффекта.

    Args:
        frame: RGB frame uint8
        intensity: 0.001-0.01 (0.003 = subtle, 0.01 = heavy)
        radial: True = радиальное смещение от центра

    Returns:
        Frame с CA эффектом uint8
    """
    h, w = frame.shape[:2]
    r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

    if radial:
        # Radial shift (stronger at edges)
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h / 2, w / 2

        # Normalized distance from center
        dist = np.sqrt(((x - center_x) / w) ** 2 +
                      ((y - center_y) / h) ** 2)

        # Shift amount (quadratic falloff)
        shift_amount = (dist ** 2) * intensity * w

        # Convert to integer shifts
        shift_x = (shift_amount * (x - center_x) / w).astype(int)

        # Shift red outward, blue inward
        r_shifted = np.zeros_like(r)
        b_shifted = np.zeros_like(b)

        for i in range(h):
            for j in range(w):
                # Red shift
                new_j = int(j + shift_x[i, j])
                if 0 <= new_j < w:
                    r_shifted[i, j] = r[i, new_j]

                # Blue shift
                new_j = int(j - shift_x[i, j])
                if 0 <= new_j < w:
                    b_shifted[i, j] = b[i, new_j]

        result = np.stack([r_shifted, g, b_shifted], axis=2)

    else:
        # Simple lateral shift
        shift = int(w * intensity)
        r_shifted = np.roll(r, -shift, axis=1)
        b_shifted = np.roll(b, shift, axis=1)
        result = np.stack([r_shifted, g, b_shifted], axis=2)

    return result


def add_halation_bloom(frame: np.ndarray,
                      threshold: float = 0.75,
                      intensity: float = 0.20,
                      radius: int = 25) -> np.ndarray:
    """
    Halation/Bloom эффект (film highlight bloom).

    Яркие участки "расползаются" как на плёнке.

    Args:
        frame: RGB frame uint8
        threshold: порог яркости для bloom (0-1)
        intensity: интенсивность bloom
        radius: радиус Gaussian blur

    Returns:
        Frame с bloom эффектом uint8
    """
    img = frame.astype(np.float32) / 255.0

    # Calculate luminance
    lum = img[:,:,0] * 0.3 + img[:,:,1] * 0.59 + img[:,:,2] * 0.11

    # Mask bright areas
    bright_mask = (lum > threshold).astype(np.float32)

    # Extract bright regions
    bright_areas = img * np.stack([bright_mask] * 3, axis=2)

    # Gaussian blur для bloom
    bloom = cv2.GaussianBlur(bright_areas,
                            (radius*2+1, radius*2+1),
                            radius/2)

    # Add bloom (additive)
    result = img + bloom * intensity

    return np.clip(result * 255, 0, 255).astype(np.uint8)


def add_vignette(frame: np.ndarray,
                amount: float = 0.35,
                feather: float = 0.80,
                roundness: float = 0.5,
                color_tint: Tuple[int, int, int] = (0, 0, 5)) -> np.ndarray:
    """
    Кинематографическая виньетка с цветовым оттенком.

    Args:
        frame: RGB frame uint8
        amount: интенсивность затемнения (0-1)
        feather: мягкость края (0-1)
        roundness: 0 = прямоугольная, 1 = круглая
        color_tint: RGB оттенок в тенях (subtle cyan для кинематографичности)

    Returns:
        Frame с виньеткой uint8
    """
    h, w = frame.shape[:2]

    y, x = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2

    # Distance calculation
    if roundness > 0.5:
        # More circular
        dist = np.sqrt(((x - center_x) / (w/2)) ** 2 +
                      ((y - center_y) / (h/2)) ** 2)
    else:
        # More rectangular
        dist_x = np.abs(x - center_x) / (w/2)
        dist_y = np.abs(y - center_y) / (h/2)
        dist = np.maximum(dist_x, dist_y)

    # Smooth falloff
    vignette = 1 - np.clip((dist - (1 - feather)) / feather, 0, 1) * amount
    vignette = np.power(vignette, 1.5)  # Power curve for natural look

    # Apply vignette
    vignette_3d = np.stack([vignette] * 3, axis=2)
    result = frame.astype(np.float32) * vignette_3d

    # Add subtle color tint to darkened areas
    tint_strength = 1 - vignette
    tint_layer = np.zeros_like(frame, dtype=np.float32)
    for i, c in enumerate(color_tint):
        tint_layer[:,:,i] = tint_strength * c

    result = result + tint_layer

    return np.clip(result, 0, 255).astype(np.uint8)


def add_light_leak(frame: np.ndarray,
                  position: str = "top_right",
                  color: Tuple[int, int, int] = (200, 220, 255),
                  intensity: float = 0.25,
                  blur: int = 60) -> np.ndarray:
    """
    Световая утечка как на плёнке (light leak).

    Args:
        frame: RGB frame uint8
        position: "top_right", "left_edge", "radial_center"
        color: RGB цвет утечки
        intensity: интенсивность эффекта
        blur: радиус размытия

    Returns:
        Frame с light leak эффектом uint8
    """
    h, w = frame.shape[:2]
    leak = np.zeros((h, w), dtype=np.float32)

    if position == "top_right":
        # Diagonal streak from top-right
        y, x = np.ogrid[:h, :w]
        gradient = np.clip((x / w) + (1 - y / h), 0, 1)
        gradient = gradient ** 2

    elif position == "left_edge":
        # Vertical glow on left
        x_grad = np.linspace(1, 0, w)
        gradient = np.outer(np.ones(h), x_grad)
        gradient = gradient ** 3

    elif position == "radial_center":
        # Radial bloom from center
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt(((x - w/2) / w) ** 2 + ((y - h/2) / h) ** 2)
        gradient = np.clip(1 - dist, 0, 1)
        gradient = gradient ** 2

    else:
        gradient = np.zeros((h, w))

    # Apply color
    leak_layer = np.zeros((h, w, 3), dtype=np.float32)
    for i, c in enumerate(color):
        leak_layer[:,:,i] = gradient * c

    # Blur
    leak_layer = cv2.GaussianBlur(leak_layer, (blur*2+1, blur*2+1), blur/2)

    # Blend (screen/add mode)
    result = frame.astype(np.float32) + leak_layer * intensity

    return np.clip(result, 0, 255).astype(np.uint8)


def add_digital_glitch(frame: np.ndarray,
                      intensity: float = 0.5,
                      glitch_type: str = "rgb_split") -> np.ndarray:
    """
    Digital glitch эффект (только для DROP момента).

    Args:
        frame: RGB frame uint8
        intensity: интенсивность (0-1)
        glitch_type: "rgb_split", "scan_lines", "block_damage"

    Returns:
        Glitched frame uint8
    """
    if glitch_type == "rgb_split":
        # Extreme RGB channel offset
        r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

        offset = int(intensity * 10)
        r = np.roll(r, -offset, axis=1)
        b = np.roll(b, offset, axis=1)

        return np.stack([r, g, b], axis=2)

    elif glitch_type == "scan_lines":
        # Horizontal scan line displacement
        h = frame.shape[0]
        result = frame.copy()

        for i in range(0, h, 3):
            if np.random.random() < intensity:
                shift = np.random.randint(-5, 5)
                result[i] = np.roll(result[i], shift, axis=0)

        return result

    elif glitch_type == "block_damage":
        # Random block corruption
        h, w = frame.shape[:2]
        result = frame.copy()

        num_blocks = int(intensity * 20)
        for _ in range(num_blocks):
            x = np.random.randint(0, w - 50)
            y = np.random.randint(0, h - 50)
            block_w = np.random.randint(20, 80)
            block_h = np.random.randint(10, 30)

            shift = np.random.randint(-10, 10)
            result[y:y+block_h, x:x+block_w] = np.roll(
                result[y:y+block_h, x:x+block_w],
                shift,
                axis=1
            )

        return result

    return frame


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def get_beat_phase(time: float, bpm: float = 170.5) -> float:
    """
    Вычисляет фазу текущего бита (0-1).

    Args:
        time: текущее время в секундах
        bpm: темп трека

    Returns:
        Beat phase (0-1), где 0 = начало бита, 1 = конец
    """
    beat_interval = 60.0 / bpm
    return (time % beat_interval) / beat_interval


def get_green_pulse_intensity(time: float,
                             drop_start: float = 17.163,
                             bpm: float = 170.5) -> float:
    """
    Интенсивность пульсации зелёных глаз в такт басу.

    Args:
        time: текущее время
        drop_start: время DROP момента
        bpm: темп

    Returns:
        Pulse multiplier (0.7-1.0)
    """
    if time < drop_start:
        return 1.0

    beat_phase = get_beat_phase(time - drop_start, bpm)

    # Пульс: быстрый рост, медленное падение
    if beat_phase < 0.15:
        # На ударе бита
        pulse = 1.0 - (beat_phase / 0.15) * 0.3  # 1.0 → 0.7
    else:
        # Восстановление
        pulse = 0.7 + ((beat_phase - 0.15) / 0.85) * 0.3  # 0.7 → 1.0

    return pulse


def add_letterbox(frame: np.ndarray,
                 ratio: float = 2.39,
                 bar_color: Tuple[int, int, int] = (12, 12, 12)) -> np.ndarray:
    """
    Добавляет letterbox bars для cinematic aspect ratio.

    Args:
        frame: RGB frame uint8
        ratio: aspect ratio (2.39 = anamorphic, 1.85 = flat)
        bar_color: RGB цвет баров (тёмно-серый, не чёрный)

    Returns:
        Frame с letterbox uint8
    """
    h, w = frame.shape[:2]

    # Calculate target height
    target_h = int(w / ratio)
    bar_height = (h - target_h) // 2

    result = frame.copy()

    # Add bars
    result[:bar_height, :] = bar_color
    result[-bar_height:, :] = bar_color

    return result


# ============================================================
# SECTION-SPECIFIC GRADE PRESETS
# ============================================================

SECTION_PRESETS = {
    "INTRO": {
        "lift": -0.18,
        "gamma": 0.92,
        "gain": 1.05,
        "contrast": 1.30,
        "vignette_amount": 0.42,
        "grain_intensity": 0.14,
        "ca_intensity": 0.0015,
        "halation_threshold": 0.82,
        "halation_intensity": 0.12,
    },
    "BUILD": {
        "lift": -0.12,
        "gamma": 0.98,
        "gain": 1.12,
        "contrast": 1.42,
        "vignette_amount": 0.32,
        "grain_intensity": 0.18,
        "ca_intensity": 0.0022,
        "halation_threshold": 0.78,
        "halation_intensity": 0.08,
    },
    "PRE_DROP": {
        "lift": -0.05,
        "gamma": 1.05,
        "gain": 1.15,
        "contrast": 1.18,
        "vignette_amount": 0.20,
        "grain_intensity": 0.11,
        "ca_intensity": 0.0012,
        "halation_threshold": 0.80,
        "halation_intensity": 0.15,
    },
    "DROP": {
        "lift": -0.22,
        "gamma": 0.96,
        "gain": 1.22,
        "contrast": 1.55,
        "vignette_amount": 0.48,
        "grain_intensity": 0.28,
        "ca_intensity": 0.0045,
        "halation_threshold": 0.70,
        "halation_intensity": 0.28,
        "green_sat_boost": 0.85,
        "green_lum_boost": 0.20,
        "green_glow": 0.18,
    },
    "CLIMAX": {
        "lift": -0.18,
        "gamma": 1.02,
        "gain": 1.18,
        "contrast": 1.48,
        "vignette_amount": 0.50,
        "grain_intensity": 0.18,
        "ca_intensity": 0.0010,
        "halation_threshold": 0.68,
        "halation_intensity": 0.32,
        "green_sat_boost": 1.0,
        "green_lum_boost": 0.24,
        "green_glow": 0.22,
    },
    "PEAK": {
        "lift": -0.16,
        "gamma": 0.98,
        "gain": 1.16,
        "contrast": 1.42,
        "vignette_amount": 0.38,
        "grain_intensity": 0.24,
        "ca_intensity": 0.0028,
        "halation_threshold": 0.72,
        "halation_intensity": 0.20,
        "green_sat_boost": 0.6,
        "green_lum_boost": 0.10,
        "green_glow": 0.12,
    },
    "OUTRO": {
        "lift": -0.04,
        "gamma": 1.08,
        "gain": 1.04,
        "contrast": 1.12,
        "vignette_amount": 0.25,
        "grain_intensity": 0.08,
        "ca_intensity": 0.0015,
        "halation_threshold": 0.80,
        "halation_intensity": 0.10,
    },
}


def apply_section_grade(frame: np.ndarray,
                       section: str,
                       time: float = 0,
                       beat_phase: float = 0) -> np.ndarray:
    """
    Применяет полный grade для конкретной секции.

    MASTER PIPELINE:
    1. B&W Conversion
    2. Primary Corrections (Lift/Gamma/Gain)
    3. Contrast
    4. Green Eye Isolation (если нужно)
    5. Halation/Bloom
    6. Film Grain
    7. Chromatic Aberration
    8. Vignette

    Args:
        frame: RGB frame uint8
        section: название секции ("INTRO", "BUILD", etc.)
        time: текущее время (для пульсаций)
        beat_phase: фаза бита (0-1)

    Returns:
        Fully graded frame uint8
    """
    preset = SECTION_PRESETS.get(section, SECTION_PRESETS["INTRO"])

    # Step 1: B&W или Green Eyes
    if section in ["DROP", "CLIMAX", "PEAK"]:
        # Green eyes active
        pulse = get_green_pulse_intensity(time) if section == "DROP" else 1.0

        result = isolate_green_eyes_pro(
            frame,
            sat_boost=preset.get("green_sat_boost", 0.5) * pulse,
            lum_boost=preset.get("green_lum_boost", 0.1) * pulse,
            glow=preset.get("green_glow", 0.1)
        )
    else:
        # Pure B&W
        result = cinematic_bw_conversion(frame)

    # Step 2-3: Primary + Contrast
    result = apply_lift_gamma_gain(
        result,
        lift=preset["lift"],
        gamma=preset["gamma"],
        gain=preset["gain"]
    )
    result = apply_contrast(result, contrast=preset["contrast"])

    # Step 4: Halation
    result = add_halation_bloom(
        result,
        threshold=preset["halation_threshold"],
        intensity=preset["halation_intensity"],
        radius=25
    )

    # Step 5: Grain (с beat reactivity для DROP)
    grain_intensity = preset["grain_intensity"]
    if section == "DROP" and beat_phase < 0.15:
        grain_intensity += 0.12  # Spike на битах

    result = add_film_grain(
        result,
        intensity=grain_intensity,
        size=0.80,
        static=(section == "CLIMAX")  # Frozen grain на CLIMAX
    )

    # Step 6: Chromatic Aberration
    result = add_chromatic_aberration(
        result,
        intensity=preset["ca_intensity"],
        radial=True
    )

    # Step 7: Vignette
    vignette_amount = preset["vignette_amount"]

    # Pulsing vignette на DROP
    if section == "DROP":
        pulse = get_green_pulse_intensity(time)
        vignette_amount += (1 - pulse) * 0.08

    result = add_vignette(
        result,
        amount=vignette_amount,
        feather=0.80,
        roundness=0.5,
        color_tint=(0, 0, 5)  # Subtle cyan tint
    )

    return result


# ============================================================
# TESTING / EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    """
    Пример использования функций.
    """
    print("CINEMA VFX TOOLKIT")
    print("=" * 60)
    print("Функции загружены успешно.")
    print()
    print("Доступные функции:")
    print("  - cinematic_bw_conversion()")
    print("  - isolate_green_eyes_pro()")
    print("  - add_film_grain()")
    print("  - add_chromatic_aberration()")
    print("  - add_halation_bloom()")
    print("  - add_vignette()")
    print("  - add_light_leak()")
    print("  - apply_section_grade()")
    print()
    print("Пресеты для секций:")
    for section in SECTION_PRESETS:
        print(f"  - {section}")
    print()
    print("Готово к использованию в MoviePy!")
    print("=" * 60)

    # Example: Тест на случайном кадре
    test_frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)

    print("\nТест: применение INTRO grade...")
    graded = apply_section_grade(test_frame, "INTRO")
    print(f"Результат: {graded.shape}, dtype={graded.dtype}")

    print("\nТест: изоляция зелёных глаз...")
    green_eyes = isolate_green_eyes_pro(test_frame, sat_boost=1.0, lum_boost=0.2, glow=0.15)
    print(f"Результат: {green_eyes.shape}")

    print("\n✅ Все функции работают!")
