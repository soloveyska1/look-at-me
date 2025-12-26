# 🎬 CINEMA-LEVEL COLOR GRADING & VFX BIBLE
## "СМОТРЕЛА" — Саймурр | $500K Music Video Treatment

---

**ВИЗУАЛЬНАЯ ФИЛОСОФИЯ:**
*Чёрно-белое кино встречает современный phonk. Изумрудные глаза — единственная память о цвете. Каждый кадр — это картина. Каждый переход — это удар сердца.*

---

## 📊 TECHNICAL FOUNDATION

### Master Project Settings
```python
# DaVinci Resolve / MoviePy Settings
RESOLUTION = (1920, 1080)
FPS = 30
ASPECT_RATIO = 2.39  # Anamorphic letterbox
COLOR_SPACE = "Rec.709"
BIT_DEPTH = 10  # Minimum for professional grade
GAMMA = 2.4
```

### Color Science Pipeline
```
RAW FOOTAGE → LOG CONVERSION → B&W CHANNEL MIXER →
PRIMARY GRADE → SECONDARY ISOLATION → GREEN EYE BOOST →
HALATION → GRAIN → CHROMATIC AB → OUTPUT LUT
```

---

# 1. 🎨 COLOR GRADING СТРАТЕГИЯ

## 1.1 B&W CONVERSION (Не простая десатурация!)

### Channel Mixer Formula (Hollywood B&W)
```python
def cinematic_bw_conversion(frame):
    """
    Профессиональная конверсия в B&W с сохранением контраста кожи и глаз.
    Основано на методике Roger Deakins (1917, Blade Runner 2049).
    """
    img = frame.astype(np.float32) / 255.0

    # Weighted luminosity (НЕ простое среднее!)
    # Red: 30% — кожа
    # Green: 59% — глаза, детали
    # Blue: 11% — тени, атмосфера
    gray = (img[:,:,0] * 0.30 +
            img[:,:,1] * 0.59 +
            img[:,:,2] * 0.11)

    # Применяем S-образную кривую для "плёночного" контраста
    gray = s_curve_contrast(gray, toe=0.10, shoulder=0.92)

    return np.stack([gray]*3, axis=2)

def s_curve_contrast(img, toe=0.10, shoulder=0.90, strength=1.2):
    """
    S-кривая для кинематографического контраста.
    toe: точка сжатия теней (0.05-0.15)
    shoulder: точка сжатия света (0.85-0.95)
    strength: интенсивность кривой (1.0-1.5)
    """
    # Применяем кубическую интерполяцию
    x = np.clip(img, 0, 1)

    # Тени (0 → toe)
    shadows = np.where(x < 0.5,
                      toe + (x / 0.5) ** strength * (0.5 - toe),
                      x)

    # Света (shoulder → 1)
    result = np.where(shadows >= 0.5,
                     0.5 + ((shadows - 0.5) / 0.5) ** (1/strength) * (shoulder - 0.5),
                     shadows)

    return np.clip(result, 0, 1)
```

### СЕКЦИЯ-ПО-СЕКЦИИ GRADING BLUEPRINT

#### ⚫ INTRO (0.000s - 4.320s): "Пустота"

**Визуальная концепция:** Холодная бездна памяти, тёмная комната без неё.

**Primary Corrections:**
```python
intro_grade = {
    "lift": -0.18,        # Жёсткое сжатие чёрного
    "gamma": 0.92,        # Затемнение средних тонов
    "gain": 1.05,         # Лёгкое поднятие света
    "contrast": 1.30,     # Сильный контраст
    "saturation": 0.0,    # Полная десатурация
}

# Luma Curve (DaVinci Resolve стиль)
intro_curve = {
    "shadows": [
        (0, 0),           # Чистый чёрный
        (0.15, 0.08),     # Сжатие теней
        (0.30, 0.25),     # Переход к mid
    ],
    "midtones": [
        (0.30, 0.25),
        (0.50, 0.45),     # Слегка ниже линейной
        (0.70, 0.65),
    ],
    "highlights": [
        (0.70, 0.65),
        (0.85, 0.82),     # Мягкий rolloff
        (1.00, 0.94),     # Не чисто белый
    ]
}
```

**HSL Secondary (Skin Isolation):**
```python
intro_skin = {
    "hue_range": (15, 35),      # Оранжево-красный
    "sat_range": (0, 100),      # Любая сатурация
    "lum_range": (20, 80),      # Средние тона
    "qualifier_blur": 5,         # Мягкая маска
    "sat_output": 0,            # Убить цвет
    "lum_output": 1.08,         # +8% яркости кожи
}
```

**Vignette:**
```python
intro_vignette = {
    "amount": 0.42,              # 42% затемнения
    "midpoint": 0.50,            # Центр виньетки
    "roundness": 0.35,           # Слегка овальная
    "feather": 0.82,             # Мягкие края
}
```

**Film Grain:**
```python
intro_grain = {
    "size": 0.75,                # Мелкое зерно
    "intensity": 0.14,           # 14%
    "stock": "Kodak_5219",       # 500T pushed
    "temporal": False,           # Статичное
    "color_variance": 0.03,      # Лёгкая хроматическая вариация
}
```

**MOVIEPY КОД:**
```python
def grade_intro(frame):
    # B&W conversion
    bw = cinematic_bw_conversion(frame)

    # Primary grade
    bw = apply_lift_gamma_gain(bw,
                               lift=-0.18,
                               gamma=0.92,
                               gain=1.05)
    bw = apply_contrast(bw, 1.30)

    # Vignette
    bw = add_vignette(bw,
                      amount=0.42,
                      feather=0.82,
                      roundness=0.35)

    # Grain
    bw = add_film_grain(bw,
                        intensity=0.14,
                        size=0.75,
                        static=True)

    # Subtle halation на светлые участки
    bw = add_halation(bw,
                      threshold=0.80,
                      intensity=0.12,
                      radius=18)

    return bw
```

---

#### ⚡ BUILD-UP (4.320s - 10.016s): "Поиск"

**Визуальная концепция:** Фрагментированная реальность, учащённое сердцебиение, хаос поиска.

**Primary Corrections:**
```python
build_grade = {
    "lift": -0.12,
    "gamma": 0.98,        # Почти нейтральный
    "gain": 1.12,         # Больше света
    "contrast": 1.42,     # МАКСИМАЛЬНЫЙ контраст
    "saturation": 0.0,
}
```

**Advanced Curve (Steeper S):**
```python
build_curve = {
    "toe_crush": 0.05,          # Жёсткий чёрный
    "mid_contrast_boost": 1.6,  # Резкий контраст в середине
    "shoulder_rolloff": 0.88,   # Мягкие света
}

def apply_build_curve(img):
    # Более агрессивная S-кривая
    x = np.clip(img, 0, 1)

    # Toe crush (чёрные → 0.05)
    x = np.where(x < 0.05, x * 0.3, x)

    # Mid boost
    x = 0.5 + (x - 0.5) * 1.6

    # Shoulder rolloff
    x = np.where(x > 0.88,
                0.88 + (x - 0.88) * 0.5,
                x)

    return np.clip(x, 0, 1)
```

**Dynamic Adjustments (по типу кадра):**
```python
# Для crowd shots
crowd_boost = {
    "contrast": +0.10,          # Ещё больше контраста
    "grain": +0.05,             # Больше зерна = хаос
    "sharpness": +0.15,         # Резкость
}

# Для hand/piano shots
hand_adjustments = {
    "contrast": 0,              # Базовый
    "vignette": -0.05,          # Меньше виньетки
    "luminance": +0.08,         # Руки ярче
}
```

**Grain Animation (двигается с ритмом):**
```python
build_grain = {
    "size": 0.80,
    "intensity_base": 0.18,
    "intensity_pulse": 0.08,    # Пульсирует на битах
    "temporal": True,           # Анимированное
    "pulse_timing": BEAT_GRID,  # Синхронизировано с BPM
}
```

**MOVIEPY КОД:**
```python
def grade_build(frame, time_in_section, beat_phase):
    bw = cinematic_bw_conversion(frame)

    # Primary
    bw = apply_lift_gamma_gain(bw, -0.12, 0.98, 1.12)
    bw = apply_build_curve(bw)

    # Grain пульсирует на битах
    grain_intensity = 0.18
    if beat_phase < 0.15:  # На ударе бита
        grain_intensity += 0.08

    bw = add_film_grain(bw, intensity=grain_intensity, size=0.80)

    # Vignette
    bw = add_vignette(bw, amount=0.32, feather=0.78)

    # Chromatic aberration (subtle)
    bw = add_chromatic_aberration(bw, intensity=0.0022)

    return bw
```

---

#### 🌙 PRE-DROP (10.016s - 17.163s): "Затишье перед бурей"

**Визуальная концепция:** Время замедляется. Сон наяву. Близость к истине.

**Primary Corrections:**
```python
predrop_grade = {
    "lift": -0.05,        # Мягче чёрный
    "gamma": 1.05,        # Светлее средние тона
    "gain": 1.15,         # Больше света
    "contrast": 1.18,     # МЕНЬШЕ контраста (!)
    "saturation": 0.0,
}
```

**Dreamy Curve (softer S):**
```python
predrop_curve = {
    "toe_lift": 0.08,           # Мягкие чёрные
    "mid_expansion": 0.95,      # Расширение средних тонов
    "shoulder_extension": 0.95, # Больше деталей в свете
}
```

**Slow Motion Grade Enhancement:**
```python
# Для slow-mo кадров
slowmo_enhancement = {
    "motion_blur": 180,         # 180° shutter angle
    "optical_flow": True,       # Интерполяция
    "grain_temporal_lock": True,# Зерно следует за движением
    "sharpness": -0.10,         # Лёгкое размытие = мечтательность
}
```

**Selective DOF Simulation:**
```python
def add_selective_focus(frame, focus_region="center"):
    """
    Имитация малой глубины резкости для кинематографичности.
    """
    # Gaussian blur на фоне
    blurred = cv2.GaussianBlur(frame, (13, 13), 4.0)

    # Маска фокуса (центр резкий)
    h, w = frame.shape[:2]
    y, x = np.ogrid[:h, :w]

    if focus_region == "center":
        mask = np.exp(-((x - w/2)**2 + (y - h/2)**2) / (w*h*0.1))
    elif focus_region == "eyes":
        # Фокус на верхней трети (где глаза)
        mask = np.exp(-((x - w/2)**2 + (y - h*0.4)**2) / (w*h*0.08))

    mask = np.stack([mask]*3, axis=2)
    result = frame * mask + blurred * (1 - mask)

    return result.astype(np.uint8)
```

**Black Screen (16.500s - 17.163s):**
```python
black_screen_spec = {
    "rgb": (0, 0, 0),           # Чистый чёрный
    "duration": 0.663,          # 663ms
    "grain": 0.04,              # Лёгкое зерно даже на чёрном
    "subtle_flicker": True,     # Нестабильность чёрного
}

def create_tense_black(duration=0.663):
    """Напряжённый чёрный экран перед DROP."""
    def make_frame(t):
        base = np.zeros((1080, 1920, 3), dtype=np.uint8)

        # Добавляем едва заметное зерно
        base = add_film_grain(base, intensity=0.04)

        # Случайные мерцания (±2%)
        if np.random.random() < 0.3:
            flicker = np.random.uniform(-5, 5)
            base = np.clip(base + flicker, 0, 255).astype(np.uint8)

        return base

    return VideoClip(make_frame, duration=duration)
```

---

#### 💥 DROP (17.163s - 25.003s): "ЭПИФАНИЯ"

**ЭТО МОМЕНТ ИСТИНЫ. ВСЁ РАДИ ЭТОГО.**

**Primary Corrections:**
```python
drop_grade = {
    "lift": -0.22,        # МАКСИМАЛЬНОЕ сжатие чёрного
    "gamma": 0.96,        # Punch в mid
    "gain": 1.22,         # МАКСИМУМ света
    "contrast": 1.55,     # МАКСИМАЛЬНЫЙ контраст
}
```

**Green Eye Isolation (HSL SECONDARY):**
```python
green_eye_isolation = {
    # Hue range (OpenCV: 0-180)
    "hue_center": 80,           # ~160° в стандартной палитре
    "hue_tolerance": 15,        # ±15° (65-95 в OpenCV)

    # Saturation
    "sat_min": 40,              # Минимум насыщенности
    "sat_max": 255,             # Максимум

    # Luminance
    "lum_min": 30,              # Не слишком тёмные
    "lum_max": 200,             # Не слишком яркие

    # Mask refinement
    "blur": 7,                  # Размытие маски
    "erode": 1,                 # Сжатие
    "dilate": 2,                # Расширение
}

def isolate_green_eyes_pro(frame, sat_boost=0.85, lum_boost=0.20, glow=0.15):
    """
    ПРОФЕССИОНАЛЬНАЯ изоляция зелёных глаз.
    """
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

    # Create mask for green hues
    hue_mask = ((h >= 65) & (h <= 95)).astype(np.float32)
    sat_mask = ((s >= 40) & (s <= 255)).astype(np.float32)
    lum_mask = ((v >= 30) & (v <= 200)).astype(np.float32)

    # Combine masks
    mask = hue_mask * sat_mask * lum_mask

    # Refine mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (7, 7), 2.0)

    # Create B&W base
    bw = cinematic_bw_conversion(frame)

    # Boost green in masked areas
    s_boosted = np.clip(s * (1 + sat_boost * mask), 0, 255)
    v_boosted = np.clip(v * (1 + lum_boost * mask), 0, 255)

    # Apply
    hsv[:,:,1] = s_boosted
    hsv[:,:,2] = v_boosted

    # Convert back
    colored = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    # Blend B&W + colored eyes
    mask_3d = np.stack([mask]*3, axis=2)
    result = bw * (1 - mask_3d) + colored * mask_3d

    # Add green glow
    if glow > 0:
        result = add_green_glow(result, mask, intensity=glow)

    return result.astype(np.uint8)

def add_green_glow(frame, mask, intensity=0.15, radius=25):
    """Добавляет свечение вокруг зелёных глаз."""
    # Создаём glow layer
    glow_mask = cv2.GaussianBlur(mask, (radius*2+1, radius*2+1), radius/2)

    # Green color
    green = np.array([20, 180, 120], dtype=np.float32)

    # Apply glow
    glow_layer = np.outer(glow_mask, green).reshape(frame.shape)
    result = frame.astype(np.float32) + glow_layer * intensity * 255

    return np.clip(result, 0, 255).astype(np.uint8)
```

**Beat-Synced Green Pulsing:**
```python
def get_green_pulse_intensity(time, drop_start=17.163, bpm=170.5):
    """
    Зелёные глаза пульсируют в такт басу.
    """
    beat_interval = 60.0 / bpm
    time_since_drop = time - drop_start

    # Какой бит сейчас?
    beat_number = time_since_drop / beat_interval
    beat_phase = beat_number % 1.0

    # Пульс: быстрый рост, медленное падение
    if beat_phase < 0.15:
        # На ударе
        pulse = 1.0 - (beat_phase / 0.15) * 0.3  # 1.0 → 0.7
    else:
        # Восстановление
        pulse = 0.7 + ((beat_phase - 0.15) / 0.85) * 0.3  # 0.7 → 1.0

    return pulse

# В grade функции:
def grade_drop(frame, time):
    # ... базовый grade ...

    # Green boost с пульсацией
    pulse = get_green_pulse_intensity(time)
    sat_boost = 0.85 * pulse
    lum_boost = 0.20 * pulse

    result = isolate_green_eyes_pro(frame, sat_boost, lum_boost, glow=0.18)

    return result
```

**Aggressive Grain:**
```python
drop_grain = {
    "intensity": 0.28,          # МАКСИМУМ
    "size": 0.85,
    "temporal": "fast",         # Быстрая анимация
    "beat_sync": True,          # Спайки на битах
    "spike_amount": 0.12,       # +12% на ударах
}
```

**Heavy Vignette with Pulse:**
```python
def pulsing_vignette(frame, time, base_intensity=0.48):
    """Виньетка пульсирует с басом."""
    pulse = get_green_pulse_intensity(time)
    intensity = base_intensity + (1 - pulse) * 0.08  # 0.48 → 0.56

    return add_vignette(frame, amount=intensity, feather=0.72)
```

**Flash Frame @ DROP (17.163s):**
```python
drop_flash_sequence = {
    # Frame 0 (17.163s): Pure white
    "frame_0": {
        "rgb": (255, 255, 255),
        "duration": 0.033,      # 1 frame
    },

    # Frame 1-3: Recovery with effects
    "recovery": {
        "chromatic_ab": 0.025,  # MASSIVE
        "zoom_punch": 1.15,     # Масштаб
        "green_surge": 1.5,     # Зелёный взрыв
        "duration": 0.100,
    }
}

def create_drop_flash():
    """Создаёт идеальный DROP flash."""
    clips = []

    # White flash
    white = ColorClip(size=(1920, 1080),
                     color=(255, 255, 255),
                     duration=0.033)
    clips.append(white)

    return clips
```

---

#### 🔥 CLIMAX (21.451s - 22.880s): "Взгляд держит"

**1.429 СЕКУНД ЧИСТОГО ЭМОЦИОНАЛЬНОГО КОНТАКТА.**

**Primary Corrections:**
```python
climax_grade = {
    "lift": -0.18,
    "gamma": 1.02,        # Лёгкое поднятие
    "gain": 1.18,
    "contrast": 1.48,
}
```

**Green Eye Treatment (MAXIMUM):**
```python
climax_eyes = {
    "sat_boost": 1.0,           # 100% boost
    "lum_boost": 0.24,          # +24% яркости
    "glow_intensity": 0.22,     # Сильное свечение
    "glow_radius": 30,
    "micro_pulse": True,        # Дыхание
}

def apply_climax_eye_pulse(frame, time_in_hold):
    """
    Микро-пульсация глаз — эффект "дыхания".
    2 цикла за 1.429 секунды.
    """
    # Синусоидальная волна
    cycle_freq = 2.0 / 1.429  # 2 цикла
    phase = time_in_hold * cycle_freq * 2 * np.pi

    # Pulse от 0.22 до 0.26
    lum_variation = 0.24 + np.sin(phase) * 0.02

    return isolate_green_eyes_pro(frame,
                                 sat_boost=1.0,
                                 lum_boost=lum_variation,
                                 glow=0.22)
```

**Slow Zoom (Hypnotic Pull):**
```python
def apply_climax_zoom(clip, duration=1.429):
    """
    Медленный zoom 100% → 105% с ease-out.
    """
    def zoom_function(t):
        # Exponential ease-out
        progress = t / duration
        eased = 1 - (1 - progress) ** 3

        # Scale от 1.00 до 1.05
        scale = 1.00 + eased * 0.05
        return scale

    return clip.resized(lambda t: zoom_function(t))
```

**Frozen Grain (стабильность = истина):**
```python
climax_grain = {
    "intensity": 0.18,
    "temporal": "frozen",       # Заморозить паттерн
    "seed": 42,                 # Фиксированный seed
}
```

**Dynamic Vignette:**
```python
def climax_vignette(frame, time_in_hold, duration=1.429):
    """Виньетка усиливается 40% → 52%."""
    progress = time_in_hold / duration
    intensity = 0.40 + progress * 0.12

    return add_vignette(frame, amount=intensity, feather=0.75)
```

---

#### ⚡ PEAK (25.003s - 34.293s): "Катарсис"

**Визуальная концепция:** Постепенное успокоение, принятие, отпускание.

**Gradual Grade Transition:**
```python
def get_peak_grade_params(time, section_start=25.003, section_end=34.293):
    """Параметры плавно меняются через всю секцию."""
    progress = (time - section_start) / (section_end - section_start)

    return {
        "lift": lerp(-0.16, -0.08, progress),
        "gamma": lerp(0.98, 1.04, progress),
        "gain": lerp(1.16, 1.08, progress),
        "contrast": lerp(1.42, 1.22, progress),
        "vignette": lerp(0.38, 0.22, progress),
        "grain": lerp(0.24, 0.16, progress),
    }

def lerp(start, end, t):
    """Linear interpolation."""
    return start + (end - start) * t
```

---

#### 🌑 OUTRO (34.293s - 37.000s): "Растворение"

**Primary Corrections:**
```python
outro_grade = {
    "lift": -0.04,
    "gamma": 1.08,
    "gain": 1.04,
    "contrast": 1.12,
}
```

**Fade to Black:**
```python
def create_outro_fade(eye_clip, fade_start=0.777):
    """
    Последний взгляд растворяется в чёрном.
    """
    def opacity_curve(t):
        if t < fade_start:
            return 1.0
        else:
            # Exponential fade
            progress = (t - fade_start) / (1.1 - fade_start)
            return 1.0 - progress ** 2

    return eye_clip.with_opacity(lambda t: opacity_curve(t))
```

---

# 2. 🎬 VFX ЭФФЕКТЫ

## 2.1 Film Grain (Kodak Vision3 5219 Simulation)

**Базовые параметры:**
```python
GRAIN_PRESETS = {
    "INTRO": {
        "size": 0.75,
        "intensity_luma": 0.14,
        "intensity_chroma": 0.03,
        "temporal": False,
    },
    "BUILD": {
        "size": 0.80,
        "intensity_luma": 0.18,
        "intensity_chroma": 0.04,
        "temporal": True,
        "animation_speed": 0.5,
    },
    "PRE_DROP": {
        "size": 0.70,
        "intensity_luma": 0.11,
        "intensity_chroma": 0.02,
        "temporal": False,
    },
    "DROP": {
        "size": 0.85,
        "intensity_luma": 0.28,
        "intensity_chroma": 0.06,
        "temporal": "fast",
        "beat_reactive": True,
        "spike": 0.12,
    },
    "CLIMAX": {
        "size": 0.80,
        "intensity_luma": 0.18,
        "intensity_chroma": 0.04,
        "temporal": "frozen",
        "seed": 42,
    },
}

def add_film_grain_pro(frame, preset="INTRO", beat_phase=0):
    """
    Профессиональное плёночное зерно.
    """
    h, w = frame.shape[:2]
    params = GRAIN_PRESETS[preset]

    # Базовая интенсивность
    intensity = params["intensity_luma"]

    # Beat reactive spike
    if params.get("beat_reactive") and beat_phase < 0.15:
        intensity += params.get("spike", 0)

    # Generate grain
    grain_size = int(1.0 / params["size"])
    grain_h = h // grain_size
    grain_w = w // grain_size

    # Organic noise (NOT uniform)
    grain = np.random.normal(0, intensity * 255, (grain_h, grain_w))

    # Upscale with interpolation
    grain = cv2.resize(grain, (w, h), interpolation=cv2.INTER_LINEAR)

    # Apply to frame
    grain_3d = np.stack([grain] * 3, axis=2)
    result = frame.astype(np.float32) + grain_3d

    # Add subtle color variance
    if params.get("intensity_chroma", 0) > 0:
        chroma_grain = np.random.normal(0, params["intensity_chroma"] * 255, (h, w, 3))
        result += chroma_grain

    return np.clip(result, 0, 255).astype(np.uint8)
```

## 2.2 Chromatic Aberration

**Lens-Style RGB Separation:**
```python
def add_chromatic_aberration_pro(frame, intensity=0.003, radial=True):
    """
    Хроматическая аберрация как на anamorphic линзах.
    intensity: 0.001-0.01 (0.003 = subtle, 0.01 = heavy)
    radial: True = радиальное смещение от центра
    """
    h, w = frame.shape[:2]
    r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

    if radial:
        # Radial shift (stronger at edges)
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h / 2, w / 2

        # Distance from center (normalized)
        dist = np.sqrt(((x - center_x) / w) ** 2 +
                      ((y - center_y) / h) ** 2)

        # Shift amount (quadratic falloff)
        shift_map = dist ** 2 * intensity * w

        # Shift red outward, blue inward
        r_shift = shift_map.astype(int)
        b_shift = -shift_map.astype(int)

        # Apply shifts
        r_shifted = shift_image(r, r_shift, axis=1)
        b_shifted = shift_image(b, b_shift, axis=1)

    else:
        # Simple lateral shift
        shift = int(w * intensity)
        r_shifted = np.roll(r, -shift, axis=1)
        b_shifted = np.roll(b, shift, axis=1)

    result = np.stack([r_shifted, g, b_shifted], axis=2)
    return result

def shift_image(img, shift_map, axis=1):
    """Apply variable shift across image."""
    h, w = img.shape
    result = np.zeros_like(img)

    for i in range(h):
        for j in range(w):
            shift = int(shift_map[i, j])
            if axis == 1:  # Horizontal
                new_j = np.clip(j + shift, 0, w - 1)
                result[i, j] = img[i, new_j]
            else:  # Vertical
                new_i = np.clip(i + shift, 0, h - 1)
                result[i, j] = img[new_i, j]

    return result
```

**Секционные значения:**
```python
CHROMATIC_AB_SETTINGS = {
    "INTRO": 0.0015,      # Едва заметно
    "BUILD": 0.0022,      # Слегка больше
    "PRE_DROP": 0.0012,   # Меньше (чистота)
    "DROP": 0.0045,       # MAXIMUM (хаос)
    "CLIMAX": 0.0010,     # Минимум (ясность)
    "PEAK": 0.0028,       # Средне-высокий
    "OUTRO": 0.0015,      # Обратно к subtle
}
```

## 2.3 Lens Distortion

**Barrel/Pincushion Distortion:**
```python
def add_lens_distortion(frame, amount=0.0, type="barrel"):
    """
    Имитация lens distortion.
    amount: -1.0 to 1.0 (negative = pincushion, positive = barrel)
    """
    h, w = frame.shape[:2]

    # Create distortion map
    camera_matrix = np.array([[w, 0, w/2],
                             [0, h, h/2],
                             [0, 0, 1]], dtype=np.float32)

    # Distortion coefficients
    dist_coeff = np.array([amount, 0, 0, 0], dtype=np.float32)

    # Apply undistort (inverted for creative effect)
    map_x, map_y = cv2.initUndistortRectifyMap(
        camera_matrix, dist_coeff, None, camera_matrix, (w, h), cv2.CV_32FC1
    )

    result = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    return result

# Применение по кадрам:
DISTORTION_MAP = {
    "empty_chair": -0.005,      # Subtle pincushion (сжатие к центру)
    "eye_closeup": +0.003,      # Subtle barrel (расширение)
    "crowd_chaos": +0.008,      # Noticeable barrel (дезориентация)
}
```

## 2.4 Halation / Bloom

**Film-Style Highlight Bloom:**
```python
def add_halation_bloom(frame, threshold=0.75, intensity=0.20, radius=25):
    """
    Halation эффект как на плёнке.
    Яркие участки "расползаются".
    """
    img = frame.astype(np.float32) / 255.0

    # Luminance
    lum = img[:,:,0] * 0.3 + img[:,:,1] * 0.59 + img[:,:,2] * 0.11

    # Mask bright areas
    bright_mask = (lum > threshold).astype(np.float32)

    # Extract bright areas
    bright_areas = img * np.stack([bright_mask] * 3, axis=2)

    # Gaussian blur для bloom
    bloom = cv2.GaussianBlur(bright_areas,
                            (radius*2+1, radius*2+1),
                            radius/2)

    # Add back with intensity
    result = img + bloom * intensity

    # Clip
    result = np.clip(result, 0, 1)

    return (result * 255).astype(np.uint8)

HALATION_SETTINGS = {
    "INTRO": {"threshold": 0.82, "intensity": 0.12, "radius": 18},
    "BUILD": {"threshold": 0.78, "intensity": 0.08, "radius": 15},
    "PRE_DROP": {"threshold": 0.80, "intensity": 0.15, "radius": 22},
    "DROP": {"threshold": 0.70, "intensity": 0.28, "radius": 32},
    "CLIMAX": {"threshold": 0.68, "intensity": 0.32, "radius": 28},
}
```

## 2.5 Glitch Effects

**Digital Glitch (только на DROP момент):**
```python
def add_digital_glitch(frame, intensity=0.5, type="rgb_split"):
    """
    Glitch эффект для DROP impact.
    """
    if type == "rgb_split":
        # Extreme RGB channel offset
        r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

        offset = int(intensity * 10)
        r = np.roll(r, -offset, axis=1)
        b = np.roll(b, offset, axis=1)

        return np.stack([r, g, b], axis=2)

    elif type == "scan_lines":
        # Horizontal scan line displacement
        h = frame.shape[0]
        result = frame.copy()

        for i in range(0, h, 3):
            if np.random.random() < intensity:
                shift = np.random.randint(-5, 5)
                result[i] = np.roll(result[i], shift, axis=0)

        return result

    elif type == "block_damage":
        # Random block corruption
        h, w = frame.shape[:2]
        result = frame.copy()

        num_blocks = int(intensity * 20)
        for _ in range(num_blocks):
            x = np.random.randint(0, w - 50)
            y = np.random.randint(0, h - 50)
            block_w = np.random.randint(20, 80)
            block_h = np.random.randint(10, 30)

            # Shift block
            shift = np.random.randint(-10, 10)
            result[y:y+block_h, x:x+block_w] = np.roll(
                result[y:y+block_h, x:x+block_w],
                shift,
                axis=1
            )

        return result

# Применение только на DROP flash (17.163s):
drop_glitch_sequence = [
    {"time": 17.196, "type": "rgb_split", "intensity": 0.8, "duration": 0.066},
    {"time": 17.262, "type": "block_damage", "intensity": 0.3, "duration": 0.033},
]
```

---

# 3. 💡 СВЕТОВЫЕ ЭФФЕКТЫ

## 3.1 Flash Frames (White/Black)

**Типы flash frames:**
```python
FLASH_EVENTS = [
    # White flashes
    {"time": 17.163, "color": (255, 255, 255), "duration": 0.033, "purpose": "DROP impact"},
    {"time": 19.891, "color": (255, 255, 255), "duration": 0.130, "purpose": "Syncopation blast"},

    # Quick flashes on beats
    {"time": 17.515, "color": (255, 255, 255), "duration": 0.033, "opacity": 0.80},
    {"time": 18.507, "color": (255, 255, 255), "duration": 0.033, "opacity": 0.60},

    # Black flash (inverted - rare!)
    {"time": 24.299, "color": (0, 0, 0), "duration": 0.033, "opacity": 0.50, "purpose": "Tempo break"},
]

def create_flash_frame(color=(255, 255, 255), duration=0.033, opacity=1.0):
    """Создаёт flash frame."""
    def make_frame(t):
        frame = np.ones((1080, 1920, 3), dtype=np.uint8) * np.array(color)
        if opacity < 1.0:
            # Можно blend с предыдущим кадром, но для простоты:
            frame = (frame * opacity).astype(np.uint8)
        return frame

    return VideoClip(make_frame, duration=duration)
```

## 3.2 Light Leaks

**Organic Film Light Leaks:**
```python
def add_light_leak(frame, position="top_right", color=(200, 220, 255),
                   intensity=0.25, blur=60):
    """
    Световая утечка как на плёнке.
    """
    h, w = frame.shape[:2]
    leak = np.zeros((h, w, 3), dtype=np.float32)

    if position == "top_right":
        # Diagonal streak from top-right
        y, x = np.ogrid[:h, :w]
        gradient = np.clip((x / w) + (1 - y / h), 0, 1)
        gradient = gradient ** 2  # Quadratic falloff

    elif position == "left_edge":
        # Vertical glow on left
        x = np.linspace(1, 0, w)
        gradient = np.outer(np.ones(h), x)
        gradient = gradient ** 3

    elif position == "radial_center":
        # Radial bloom from center
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt(((x - w/2) / w) ** 2 + ((y - h/2) / h) ** 2)
        gradient = np.clip(1 - dist, 0, 1)
        gradient = gradient ** 2

    # Apply color
    for i, c in enumerate(color):
        leak[:,:,i] = gradient * c

    # Blur
    leak = cv2.GaussianBlur(leak, (blur*2+1, blur*2+1), blur/2)

    # Blend (screen mode)
    result = frame.astype(np.float32)
    result = result + leak * intensity

    return np.clip(result, 0, 255).astype(np.uint8)

LIGHT_LEAK_EVENTS = [
    {
        "time": 17.163,
        "duration": 0.400,
        "position": "top_right",
        "color": (180, 220, 255),  # Cyan
        "intensity": 0.28,
        "blur": 50,
    },
    {
        "time": 21.451,
        "duration": 1.429,
        "position": "left_edge",
        "color": (255, 220, 180),  # Warm amber
        "intensity": 0.16,
        "blur": 60,
    },
    {
        "time": 35.723,
        "duration": 0.777,
        "position": "radial_center",
        "color": (255, 255, 255),  # White bloom
        "intensity": 0.22,
        "blur": 70,
    },
]
```

## 3.3 Vignette (Dynamic)

**Уже рассмотрено в секции Color Grading, но дополнительно:**

```python
def add_advanced_vignette(frame, amount=0.35, feather=0.80,
                         shape="oval", color_tint=(0, 0, 5)):
    """
    Продвинутая виньетка с цветовым оттенком.
    color_tint: лёгкий синий оттенок в тенях для кинематографичности
    """
    h, w = frame.shape[:2]

    y, x = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2

    # Distance calculation
    if shape == "oval":
        dist = np.sqrt(((x - center_x) / (w/2)) ** 2 +
                      ((y - center_y) / (h/2)) ** 2)
    elif shape == "rectangular":
        dist_x = np.abs(x - center_x) / (w/2)
        dist_y = np.abs(y - center_y) / (h/2)
        dist = np.maximum(dist_x, dist_y)

    # Smooth falloff
    vignette = 1 - np.clip((dist - (1 - feather)) / feather, 0, 1) * amount
    vignette = np.power(vignette, 1.5)

    # Apply
    vignette_3d = np.stack([vignette] * 3, axis=2)
    result = frame.astype(np.float32) * vignette_3d

    # Add color tint to darkened areas
    tint_strength = 1 - vignette  # Inverse of vignette
    tint = np.array(color_tint, dtype=np.float32)
    tint_3d = np.outer(np.outer(tint_strength, np.ones(w)), tint).reshape(h, w, 3)
    result = result + tint_3d

    return np.clip(result, 0, 255).astype(np.uint8)
```

## 3.4 Anamorphic Flares

**Horizontal Blue Streaks на practicals:**
```python
def add_anamorphic_flare(frame, light_position=(960, 300),
                        length=0.4, intensity=0.20):
    """
    Anamorphic lens flare - горизонтальная синяя полоса.
    light_position: (x, y) координаты источника света
    length: 0-1, длина streak (процент от ширины кадра)
    """
    h, w = frame.shape[:2]
    x0, y0 = light_position

    # Create horizontal streak
    streak = np.zeros((h, w, 3), dtype=np.float32)

    # Горизонтальная линия через y0
    streak_width = int(length * w)
    x_start = max(0, x0 - streak_width // 2)
    x_end = min(w, x0 + streak_width // 2)

    # Создаём градиент от центра
    for x in range(x_start, x_end):
        dist = abs(x - x0) / (streak_width / 2)
        falloff = (1 - dist) ** 2

        # Вертикальный profil (узкий)
        for y in range(h):
            y_dist = abs(y - y0) / 30  # 30px вертикальная ширина
            if y_dist < 1:
                vertical_falloff = (1 - y_dist) ** 2
                brightness = falloff * vertical_falloff * intensity

                # Cyan-blue color
                streak[y, x] = [100 * brightness,
                               180 * brightness,
                               255 * brightness]

    # Blur the streak
    streak = cv2.GaussianBlur(streak, (51, 51), 15)

    # Add to frame (screen blend)
    result = frame.astype(np.float32) + streak

    return np.clip(result, 0, 255).astype(np.uint8)

# Где применять:
ANAMORPHIC_FLARE_SHOTS = [
    {"shot": "empty_chair_spotlight", "position": (960, 400), "length": 0.35},
    {"shot": "window_light", "position": (1400, 300), "length": 0.28},
]
```

---

# 4. 🖼️ ТЕКСТУРЫ И OVERLAYS

## 4.1 Film Scratches

**Царапины плёнки:**
```python
def add_film_scratches(frame, num_scratches=3, intensity=0.15):
    """
    Вертикальные царапины как на старой плёнке.
    """
    h, w = frame.shape[:2]
    scratches = np.zeros((h, w), dtype=np.float32)

    for _ in range(num_scratches):
        # Random vertical position
        x = np.random.randint(0, w)

        # Scratch width (1-3 pixels)
        scratch_width = np.random.randint(1, 4)

        # Variable opacity along height
        opacity_curve = np.random.random(h)
        opacity_curve = gaussian_filter1d(opacity_curve, sigma=h/20)

        # Draw scratch
        for dx in range(scratch_width):
            if x + dx < w:
                scratches[:, x + dx] = opacity_curve

    # Apply scratches (additive white)
    result = frame.astype(np.float32)
    scratch_layer = np.stack([scratches * 255 * intensity] * 3, axis=2)
    result = result + scratch_layer

    return np.clip(result, 0, 255).astype(np.uint8)

from scipy.ndimage import gaussian_filter1d
```

## 4.2 Dust Particles

**Пыль и частицы:**
```python
def add_dust_particles(frame, num_particles=30, intensity=0.20):
    """
    Случайные пятна пыли как на плёнке.
    """
    h, w = frame.shape[:2]
    dust = np.zeros((h, w), dtype=np.float32)

    for _ in range(num_particles):
        # Random position
        x = np.random.randint(0, w)
        y = np.random.randint(0, h)

        # Random size (2-10 pixels radius)
        radius = np.random.randint(2, 10)

        # Draw spot
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                if (dy**2 + dx**2) <= radius**2:
                    py, px = y + dy, x + dx
                    if 0 <= py < h and 0 <= px < w:
                        # Soft edge
                        dist = np.sqrt(dy**2 + dx**2) / radius
                        dust[py, px] = max(dust[py, px], (1 - dist) ** 2)

    # Apply dust (darkening)
    result = frame.astype(np.float32)
    dust_layer = np.stack([dust * intensity * 255] * 3, axis=2)
    result = result - dust_layer  # Subtract для затемнения

    return np.clip(result, 0, 255).astype(np.uint8)
```

## 4.3 VHS Effects (опционально)

**VHS эффект для ретро-моментов:**
```python
def add_vhs_effect(frame, intensity=0.3):
    """
    VHS искажения: scan lines, chroma bleeding, noise.
    """
    h, w = frame.shape[:2]
    result = frame.copy().astype(np.float32)

    # 1. Horizontal scan lines
    for y in range(0, h, 2):
        result[y] = result[y] * (1 - intensity * 0.3)

    # 2. Chroma bleeding (horizontal blur на цветовых каналах)
    if len(result.shape) == 3:
        # Blur chroma more than luma
        for c in range(3):
            result[:,:,c] = cv2.GaussianBlur(result[:,:,c], (5, 1), 1.5)

    # 3. Random horizontal distortion
    if np.random.random() < intensity:
        y_distort = np.random.randint(0, h)
        shift = np.random.randint(-10, 10)
        result[y_distort] = np.roll(result[y_distort], shift, axis=0)

    # 4. Color shift (green/magenta tint randomization)
    tint = np.random.uniform(-10, 10, 3) * intensity
    result = result + tint

    return np.clip(result, 0, 255).astype(np.uint8)

# Применять выборочно:
VHS_MOMENTS = [
    {"time": 8.619, "duration": 0.352, "intensity": 0.25},  # BUILD peak
]
```

## 4.4 Film Burn (Edge Damage)

**Повреждение краёв кадра:**
```python
def add_film_burn(frame, side="random", intensity=0.30):
    """
    Затемнение/выжигание краёв как на повреждённой плёнке.
    """
    h, w = frame.shape[:2]
    burn = np.ones((h, w), dtype=np.float32)

    sides = ["left", "right", "top", "bottom"]
    if side == "random":
        side = np.random.choice(sides)

    # Create burn pattern
    if side == "left":
        x = np.linspace(1, 0, int(w * 0.15))
        burn_gradient = np.pad(x, (0, w - len(x)), constant_values=0)
        burn = np.outer(np.ones(h), burn_gradient)
    elif side == "right":
        x = np.linspace(0, 1, int(w * 0.15))
        burn_gradient = np.pad(x, (w - len(x), 0), constant_values=0)
        burn = np.outer(np.ones(h), burn_gradient)
    # Similar for top/bottom...

    # Apply burn (multiplicative darkening)
    burn = 1 - burn ** 2 * intensity
    burn_3d = np.stack([burn] * 3, axis=2)
    result = frame.astype(np.float32) * burn_3d

    # Add warm color tint to burned areas
    burn_tint = (1 - burn) * np.array([30, 15, 5])
    result = result + np.stack([burn_tint] * 3, axis=2)

    return np.clip(result, 0, 255).astype(np.uint8)
```

---

# 5. ✍️ MOTION GRAPHICS & TYPOGRAPHY

## 5.1 Title Card Design

**Финальная заставка "СМОТРЕЛА":**

```python
def create_professional_title_card(duration=0.70):
    """
    Профессиональная title card с зелёным ирисом.

    Композиция:
    ◉ СМОТРЕЛА
      look at me
                    С А Й М У Р Р
    """
    from PIL import Image, ImageDraw, ImageFont

    def make_frame(t):
        # Background: очень тёмно-серый (не чёрный!)
        bg_color = (12, 12, 12)
        img = Image.new('RGB', (1920, 1080), bg_color)
        draw = ImageDraw.Draw(img)

        # Fade in curve
        fade_progress = min(t / 0.3, 1.0)  # Fade за 0.3s
        alpha = fade_progress

        # Colors
        white = (int(252 * alpha), int(252 * alpha), int(250 * alpha))
        gray = (int(160 * alpha), int(160 * alpha), int(162 * alpha))
        green = (int(48 * alpha), int(168 * alpha), int(107 * alpha))  # Изумрудный

        # Fonts (попытка загрузить, fallback на default)
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            artist_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            artist_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            # Fallback
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            artist_font = ImageFont.load_default()
            artist_small = ImageFont.load_default()

        # 1. Green Iris Symbol (◉)
        iris_x, iris_y = 960 - 280, 540 - 30
        iris_radius = 10
        draw.ellipse([iris_x - iris_radius, iris_y - iris_radius,
                     iris_x + iris_radius, iris_y + iris_radius],
                    fill=green, outline=None)

        # Optional: outer ring
        outer_radius = 13
        draw.ellipse([iris_x - outer_radius, iris_y - outer_radius,
                     iris_x + outer_radius, iris_y + outer_radius],
                    outline=green, width=1)

        # 2. Main Title: СМОТРЕЛА
        title_text = "СМОТРЕЛА"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        title_x = (1920 - title_w) // 2 + 30  # Offset for iris
        title_y = 540 - 50

        draw.text((title_x, title_y), title_text, fill=white, font=title_font)

        # 3. Subtitle: look at me
        subtitle = "look at me"
        sub_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = (1920 - sub_w) // 2 + 30
        sub_y = title_y + 110

        draw.text((sub_x, sub_y), subtitle, fill=gray, font=subtitle_font)

        # 4. Artist Name (bottom right)
        artist = "С А Й М У Р Р"
        artist_x = 1920 - 320
        artist_y = 1080 - 140

        # First letter in green
        draw.text((artist_x, artist_y), "С", fill=green, font=artist_font)

        # Rest in white
        first_bbox = draw.textbbox((0, 0), "С ", font=artist_font)
        rest_x = artist_x + (first_bbox[2] - first_bbox[0])
        draw.text((rest_x, artist_y), "А Й М У Р Р", fill=white, font=artist_font)

        # Latin transliteration
        latin = "saymurr"
        draw.text((artist_x, artist_y + 50), latin, fill=gray, font=artist_small)

        # Convert to numpy
        frame_array = np.array(img)

        # Add subtle grain
        frame_array = add_film_grain_pro(frame_array, preset="INTRO", beat_phase=1.0)

        # Vignette
        frame_array = add_vignette(frame_array, amount=0.15, feather=0.90)

        return frame_array

    return VideoClip(make_frame, duration=duration)
```

## 5.2 Text Animation (опционально)

**Анимированное появление текста:**

```python
def animate_title_text(text="СМОТРЕЛА", duration=1.0,
                       style="tracking_expand"):
    """
    Анимация текста различными способами.
    """
    if style == "tracking_expand":
        # Letter-spacing расширяется
        def make_frame(t):
            progress = t / duration
            tracking = int(progress * 100)  # 0 → 100
            # ... render text с tracking ...
            pass

    elif style == "fade_in_per_letter":
        # Каждая буква появляется поочерёдно
        def make_frame(t):
            progress = t / duration
            letters_visible = int(progress * len(text))
            visible_text = text[:letters_visible]
            # ... render visible_text ...
            pass

    elif style == "glitch_reveal":
        # Glitch эффект при появлении
        def make_frame(t):
            if t < duration * 0.5:
                # Glitch phase
                offset = np.random.randint(-5, 5)
                # ... render с offset ...
            else:
                # Stable phase
                # ... render нормально ...
            pass

    return VideoClip(make_frame, duration=duration)
```

## 5.3 Animated Iris Symbol

**Анимированный символ глаза:**

```python
def create_animated_iris(duration=2.0):
    """
    Пульсирующий зелёный ирис как логотип.
    """
    def make_frame(t):
        img = np.zeros((1080, 1920, 3), dtype=np.uint8)

        # Pulsing radius
        base_radius = 40
        pulse = np.sin(t * 2 * np.pi) * 5  # Pulse ±5px
        radius = int(base_radius + pulse)

        # Draw iris
        center = (960, 540)
        cv2.circle(img, center, radius, (48, 168, 107), -1)  # Filled green
        cv2.circle(img, center, radius + 3, (48, 168, 107), 2)  # Outline

        # Inner highlight (catchlight)
        highlight_pos = (center[0] - radius//3, center[1] - radius//3)
        cv2.circle(img, highlight_pos, radius//4, (180, 255, 200), -1)

        # Glow
        glow = cv2.GaussianBlur(img, (101, 101), 30)
        result = cv2.addWeighted(img, 0.7, glow, 0.3, 0)

        return result

    return VideoClip(make_frame, duration=duration)
```

---

# 6. ⚙️ ТЕХНИЧЕСКИЕ ПАРАМЕТРЫ ДЛЯ MOVIEPY

## 6.1 Complete Grade Pipeline

**Полный pipeline обработки кадра:**

```python
def apply_complete_cinema_grade(frame, time, section, beat_phase=0):
    """
    МАСТЕР-ФУНКЦИЯ: применяет ВСЕ эффекты в правильном порядке.

    Pipeline Order (критично!):
    1. B&W Conversion
    2. Primary Grade (Lift/Gamma/Gain)
    3. Curves
    4. Secondary Color (Green Eyes)
    5. Halation/Bloom
    6. Grain
    7. Chromatic Aberration
    8. Vignette
    9. Light Leaks (если нужно)
    10. Letterbox
    """

    # Step 1: B&W Conversion
    result = cinematic_bw_conversion(frame)

    # Step 2-3: Primary Grade & Curves (зависит от секции)
    if section == "INTRO":
        result = apply_lift_gamma_gain(result, -0.18, 0.92, 1.05)
        result = apply_contrast(result, 1.30)

    elif section == "BUILD":
        result = apply_lift_gamma_gain(result, -0.12, 0.98, 1.12)
        result = apply_build_curve(result)

    elif section == "PRE_DROP":
        result = apply_lift_gamma_gain(result, -0.05, 1.05, 1.15)
        result = apply_contrast(result, 1.18)

    elif section == "DROP":
        # GREEN EYES ACTIVE!
        pulse = get_green_pulse_intensity(time)
        result = isolate_green_eyes_pro(frame,  # Используем ORIGINAL frame
                                       sat_boost=0.85 * pulse,
                                       lum_boost=0.20 * pulse,
                                       glow=0.18)
        result = apply_lift_gamma_gain(result, -0.22, 0.96, 1.22)
        result = apply_contrast(result, 1.55)

    elif section == "CLIMAX":
        # MAXIMUM GREEN
        time_in_hold = time - 21.451
        result = apply_climax_eye_pulse(frame, time_in_hold)
        result = apply_lift_gamma_gain(result, -0.18, 1.02, 1.18)
        result = apply_contrast(result, 1.48)

    elif section == "PEAK":
        progress = (time - 25.003) / (34.293 - 25.003)
        params = get_peak_grade_params(time)
        result = isolate_green_eyes_pro(frame,
                                       sat_boost=0.6 + progress * 0.2,
                                       lum_boost=0.10,
                                       glow=0.12)
        result = apply_lift_gamma_gain(result, params["lift"],
                                      params["gamma"],
                                      params["gain"])
        result = apply_contrast(result, params["contrast"])

    elif section == "OUTRO":
        time_in_outro = time - 34.293
        fade = max(0, 1.0 - time_in_outro / 2.0)
        result = apply_lift_gamma_gain(result, -0.04, 1.08, 1.04)
        result = apply_contrast(result, 1.12)
        # Fade effect
        result = (result * fade).astype(np.uint8)

    # Step 4: Halation/Bloom
    halation_params = HALATION_SETTINGS.get(section.upper(),
                                           {"threshold": 0.75, "intensity": 0.15, "radius": 20})
    result = add_halation_bloom(result, **halation_params)

    # Step 5: Film Grain
    grain_preset = section.upper()
    if grain_preset not in GRAIN_PRESETS:
        grain_preset = "INTRO"
    result = add_film_grain_pro(result, preset=grain_preset, beat_phase=beat_phase)

    # Step 6: Chromatic Aberration
    ca_intensity = CHROMATIC_AB_SETTINGS.get(section.upper(), 0.002)
    result = add_chromatic_aberration_pro(result, intensity=ca_intensity)

    # Step 7: Vignette
    if section == "INTRO":
        result = add_advanced_vignette(result, amount=0.42, feather=0.82)
    elif section == "BUILD":
        result = add_advanced_vignette(result, amount=0.32, feather=0.78)
    elif section == "PRE_DROP":
        result = add_advanced_vignette(result, amount=0.20, feather=0.85)
    elif section == "DROP":
        result = pulsing_vignette(result, time, base_intensity=0.48)
    elif section == "CLIMAX":
        time_in_hold = time - 21.451
        result = climax_vignette(result, time_in_hold)
    elif section == "PEAK":
        progress = (time - 25.003) / (34.293 - 25.003)
        amount = 0.38 - progress * 0.16
        result = add_advanced_vignette(result, amount=amount, feather=0.75)
    elif section == "OUTRO":
        time_in_outro = time - 34.293
        fade = max(0, 1.0 - time_in_outro / 2.0)
        result = add_advanced_vignette(result, amount=0.25 * fade, feather=0.80)

    # Step 8: Light Leaks (проверка timing)
    for leak in LIGHT_LEAK_EVENTS:
        if leak["time"] <= time < leak["time"] + leak["duration"]:
            result = add_light_leak(result,
                                   position=leak["position"],
                                   color=leak["color"],
                                   intensity=leak["intensity"],
                                   blur=leak["blur"])

    # Step 9: Letterbox (cinematic 2.39:1)
    result = add_letterbox(result)

    return result

def add_letterbox(frame, ratio=2.39):
    """Добавляет чёрные полосы для anamorphic формата."""
    h, w = frame.shape[:2]
    target_h = int(w / ratio)
    bar_height = (h - target_h) // 2

    result = frame.copy()
    result[:bar_height, :] = [12, 12, 12]  # Тёмно-серый (не чёрный)
    result[-bar_height:, :] = [12, 12, 12]

    return result
```

## 6.2 Helper Functions

```python
def apply_lift_gamma_gain(frame, lift=0, gamma=1.0, gain=1.0):
    """
    Стандартные Primary Corrections как в DaVinci Resolve.
    lift: -1.0 to 1.0 (shadows)
    gamma: 0.5 to 2.0 (midtones)
    gain: 0.5 to 2.0 (highlights)
    """
    img = frame.astype(np.float32) / 255.0

    # Lift (add to all values)
    img = img + lift

    # Gamma (power curve)
    img = np.power(np.clip(img, 0, 1), 1.0 / gamma)

    # Gain (multiply)
    img = img * gain

    return np.clip(img * 255, 0, 255).astype(np.uint8)

def apply_contrast(frame, contrast=1.0):
    """
    Pivot-based contrast (вокруг 0.5).
    contrast: 0.5 to 2.0
    """
    img = frame.astype(np.float32) / 255.0

    # Pivot around 0.5
    img = 0.5 + (img - 0.5) * contrast

    return np.clip(img * 255, 0, 255).astype(np.uint8)
```

## 6.3 Main Render Loop

```python
def render_smotrela_cinema():
    """
    ГЛАВНАЯ функция рендера с полным cinema pipeline.
    """
    import moviepy as mp
    from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip

    print("🎬 СМОТРЕЛА — CINEMA-LEVEL RENDER")
    print("=" * 60)

    # Load audio
    audio = AudioFileClip("/home/user/look-at-me/СМОТРЕЛА_teaser.wav")
    duration = min(audio.duration, 37.0)

    # Load video sources
    sources = {}
    for name, path in VIDEOS.items():
        clip = VideoFileClip(path).resized((1920, 1080))
        sources[name] = clip
        print(f"✓ Loaded {name}: {clip.duration:.1f}s")

    # Build edit from EDL
    clips = []
    timeline_pos = 0.0

    for i, cut in enumerate(EDL):
        print(f"\n[{i+1}/{len(EDL)}] {cut['section']}: {cut['purpose']}")

        src = cut["src"]
        dur = cut["dur"]
        section = cut["section"]

        if src == "black":
            # Black frame
            clip = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=dur)

        elif src == "flash":
            # White flash
            clip = create_flash_frame(duration=dur)

        elif src == "title":
            # Title card
            clip = create_professional_title_card(duration=dur)

        else:
            # Video source
            source_clip = sources[src]
            in_point = cut.get("in", 0)

            # Extract subclip
            clip = source_clip.subclipped(in_point, in_point + dur)

            # Apply COMPLETE cinema grade
            section_name = section
            timeline_time = timeline_pos

            def make_grade_filter(sec, t_offset):
                def grade_filter(get_frame, t):
                    frame = get_frame(t)
                    global_time = t_offset + t

                    # Calculate beat phase
                    beat_phase = (global_time % BEAT_INTERVAL) / BEAT_INTERVAL

                    # Apply complete grade
                    graded = apply_complete_cinema_grade(
                        frame, global_time, sec, beat_phase
                    )

                    return graded

                return grade_filter

            clip = clip.transform(make_grade_filter(section_name, timeline_time))

        clips.append(clip)
        timeline_pos += dur

    # Concatenate
    print("\n\n🎞️ Concatenating clips...")
    final = mp.concatenate_videoclips(clips, method="compose")

    # Add audio
    final = final.with_audio(audio.subclipped(0, duration))

    # Render
    output_path = "/home/user/look-at-me/SMOTRELA_CINEMA_FINAL.mp4"
    print(f"\n\n🎬 Rendering to: {output_path}")
    print("Resolution: 1920x1080 @ 30fps")
    print("Estimated time: 15-30 minutes\n")

    final.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        bitrate='15000k',  # High quality
        preset='slow',     # Best quality
        threads=4,
    )

    print("\n" + "=" * 60)
    print("✅ RENDER COMPLETE")
    print(f"📁 {output_path}")
    print("=" * 60)
    print("\n◉ СМОТРЕЛА — she was looking")
    print("   Cinema-level color grading ✓")
    print("   Professional VFX ✓")
    print("   $500,000 look ✓")
    print()

if __name__ == "__main__":
    render_smotrela_cinema()
```

---

# 📋 ФИНАЛЬНЫЙ ЧЕКЛИСТ

## Pre-Production
- [ ] Все видео источники проверены и загружены
- [ ] Аудио трек синхронизирован
- [ ] Beat grid размечен (101 бит)
- [ ] Ключевые моменты идентифицированы (DROP 17.163s, CLIMAX 21.451s)

## Color Grading
- [ ] B&W conversion правильный (luminosity-based, не desaturation)
- [ ] Primary corrections применены по секциям
- [ ] S-curves настроены (toe crush, shoulder rolloff)
- [ ] Green eye isolation работает (HSL keying)
- [ ] Green saturation/luminance пульсирует на DROP
- [ ] Vignette динамическая (меняется по секциям)

## VFX
- [ ] Film grain органичное (Kodak 5219 style)
- [ ] Grain пульсирует на битах в DROP
- [ ] Chromatic aberration subtle (0.001-0.004)
- [ ] Halation/bloom на ярких участках
- [ ] Lens distortion применена выборочно
- [ ] Glitch effects только на DROP flash

## Lighting Effects
- [ ] Flash frames на 17.163s и 19.891s
- [ ] Light leaks в правильных моментах
- [ ] Anamorphic flares на practicals (опционально)
- [ ] Vignette с цветовым tint (subtle cyan в тенях)

## Textures
- [ ] Film scratches (опционально)
- [ ] Dust particles (опционально)
- [ ] Film burn на краях (опционально)

## Motion Graphics
- [ ] Title card профессиональная
- [ ] Green iris symbol анимирован
- [ ] Typography правильные шрифты
- [ ] Fade in/out smooth

## Technical
- [ ] Resolution: 1920x1080
- [ ] FPS: 30
- [ ] Aspect ratio: 2.39:1 letterbox
- [ ] Color space: Rec.709
- [ ] Bitrate: 15000k minimum
- [ ] Audio: 48kHz AAC

## Final QC
- [ ] Audio-visual sync идеальный (±8ms на критичных моментах)
- [ ] No clipping (RGB < 235)
- [ ] No crushed blacks (RGB > 0, кроме намеренных)
- [ ] Green eyes consistent цвет (Hue 160°)
- [ ] Grain без артефактов
- [ ] No banding в градиентах
- [ ] Letterbox чёрный ровный

---

# 🎯 КЛЮЧЕВЫЕ ПРИНЦИПЫ

## 1. КОНТРАСТ = ДРАМА
Чем выше контраст, тем сильнее эмоция. DROP должен иметь максимальный контраст (1.55).

## 2. ГЛАЗА — ЭТО ВСЁ
Зелёные глаза должны светиться как изумруды в угле. Это единственная память о цвете.

## 3. ЗЕРНО — ЭТО ТЕКСТУРА
Плёночное зерно делает digital органичным. Не бойтесь 25-28% на DROP.

## 4. ЧЁРНЫЙ СВЯЩЕНЕН
Не бойтесь чистого чёрного. Crushed blacks создают mystery.

## 5. СДЕРЖАННОСТЬ — СИЛА
Не каждый момент нуждается в максимальной обработке. CLIMAX должен быть чистым и ясным.

---

# 🎬 REFERENCE FILMS

**Для B&W + Selective Color:**
- *Sin City* (2005) — Robert Rodriguez
- *Schindler's List* (1993) — Steven Spielberg

**Для Grain & Texture:**
- *Dunkirk* (2017) — Christopher Nolan
- *No Time to Die* (2021) — Cary Joji Fukunaga

**Для Eye Close-ups:**
- *Blade Runner 2049* (2017) — Roger Deakins
- *Under the Skin* (2013) — Daniel Landin

**Для Music Video Style:**
- The Weeknd — "Blinding Lights" (Anton Tammi)
- Billie Eilish — "bad guy" (Dave Meyers)
- Drake — "Hotline Bling" (Director X)

---

# 💾 EXPORT SETTINGS

```python
EXPORT_SPECS = {
    "format": "MP4 (H.264)",
    "resolution": "1920x1080",
    "fps": 30,
    "bitrate": "15000k (VBR 2-pass)",
    "preset": "slow",  # Лучшее качество
    "profile": "high",
    "level": "4.1",
    "color_space": "Rec.709",
    "color_primaries": "BT.709",
    "color_trc": "BT.709",
    "color_range": "limited (16-235)",

    "audio_codec": "AAC",
    "audio_bitrate": "320k",
    "audio_sample_rate": "48000 Hz",
    "audio_channels": "Stereo",
}
```

---

**Document Version:** 2.0 CINEMA-LEVEL
**Created:** 2025-12-26
**Project:** СМОТРЕЛА — Саймурр
**Treatment Level:** $500,000 Music Video

**"Глаза помнят. Сделай это незабываемым."**

---

◉ СМОТРЕЛА
