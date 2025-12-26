#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ◉  С А Й М У Р Р  —  С М О Т Р Е Л А                                    ║
║                                                                              ║
║     TEASER V4: "37 СЕКУНД"                                                   ║
║     ═══════════════════════════════════════════════════════════              ║
║                                                                              ║
║     КОНЦЕПЦИЯ: Музыкант сидит перед пустым стулом. За 37 секунд             ║
║     он должен решить — сыграть последнюю ноту и ОТПУСТИТЬ,                  ║
║     или остаться в боли навсегда.                                           ║
║                                                                              ║
║     ЭМОЦИОНАЛЬНАЯ ДУГА:                                                     ║
║     ├── 0-4s:    ПАРАЛИЧ      (он не играет, музыка = память)              ║
║     ├── 4-10s:   БОРЬБА       (воспоминания атакуют)                        ║
║     ├── 10-16.5s: ЗАТИШЬЕ     (vulnerability, долгие планы)                 ║
║     ├── 16.5-17.163s: ЧЁРНЫЙ  (663ms тишины = максимум напряжения)         ║
║     ├── 17.163s: РЕШЕНИЕ      (DROP = глаза = она разрешает)               ║
║     ├── 17-25s:  КАТАРСИС     (он играет, release)                          ║
║     ├── 25-35s:  ОТПУСКАНИЕ   (она уходит)                                  ║
║     └── 35-37s:  ПРИНЯТИЕ     (peace)                                       ║
║                                                                              ║
║     КРИТИЧЕСКИЕ ПРАВИЛА (от Главного Критика):                              ║
║     1. Глаза появляются ТОЛЬКО после 17s - священный reveal                 ║
║     2. Пустой стул - минимум 1.5s на появление                              ║
║     3. Финальный кадр должен ЖЕЧЬ                                           ║
║     4. История должна быть понятна БЕЗ ЗВУКА                                ║
║                                                                              ║
║     TYPOGRAPHY: PIL/Pillow с DejaVu Sans Bold (кириллица работает!)         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import (
    VideoFileClip, AudioFileClip, ColorClip, CompositeVideoClip,
    concatenate_videoclips, VideoClip
)
import cv2

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = "/home/user/look-at-me"

VIDEOS = {
    "V1": os.path.join(BASE_DIR, "20251226_0026_01kdbpca1rfxjtx3zddgv48gjh.mp4"),  # Crowd
    "V2": os.path.join(BASE_DIR, "20251226_0130_01kdbr9ggwft8sr8k143r5xfs0.mp4"),  # Piano hands
    "V3": os.path.join(BASE_DIR, "20251226_0130_01kdbrazryf8wtabs5kk6kvmqx.mp4"),  # Profile girl
    "V4": os.path.join(BASE_DIR, "20251226_0130_01kdbsc29wehvbem5ertshqfed.mp4"),  # Chair
    "V5": os.path.join(BASE_DIR, "20251226_0131_01kdbsdwn8epg9amf3qtp17qsb.mp4"),  # Silhouette
    "V6": os.path.join(BASE_DIR, "20251226_0131_01kdbspmg9egv833wj0ngh944a.mp4"),  # Eyes
}

AUDIO_FILE = os.path.join(BASE_DIR, "СМОТРЕЛА_teaser.wav")
OUTPUT_FILE = os.path.join(BASE_DIR, "SMOTRELA_teaser_v4_STORY.mp4")

# Audio parameters
BPM = 170.5
BEAT_INTERVAL = 60 / BPM  # 0.352s
TOTAL_DURATION = 37.0

# Critical sync points (frame-perfect, ±8ms tolerance)
DROP_TIME = 17.163      # Frame 515 @ 30fps - THE MOMENT
CLIMAX_TIME = 21.451    # Frame 644 - Peak of catharsis
BLACK_START = 16.500    # Pre-drop silence begins
BLACK_END = 17.163      # DROP explosion

# Typography - PIL с поддержкой кириллицы
FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PATH_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Branding
ARTIST_NAME = "САЙМУРР"
TRACK_NAME = "СМОТРЕЛА"
SUBTITLE_EN = "look at me"

# Colors (RGB for PIL)
EMERALD_GREEN = (48, 168, 107)      # #30A86B - HER color
NEAR_BLACK = (12, 12, 12)           # #0C0C0C - void
OFF_WHITE = (252, 252, 250)         # #FCFCFA - text
GRAY = (139, 139, 142)              # #8B8B8E - secondary

# Video parameters
WIDTH = 1920
HEIGHT = 1080
FPS = 30
LETTERBOX_HEIGHT = 140  # 2.39:1 aspect ratio

# =============================================================================
# STORY STRUCTURE - "37 СЕКУНД"
# =============================================================================
"""
ИСТОРИЯ: Он сидит перед пустым стулом. Музыка играет, но это память.
За 37 секунд он проживает весь цикл grief и принимает решение отпустить.

ГЛАВНОЕ ПРАВИЛО: Глаза появляются ТОЛЬКО на DROP (17.163s) - это священный reveal.
До этого момента мы видим только: стул, руки, силуэт, профиль, толпу.
"""

# =============================================================================
# EDL (Edit Decision List) - ИСТОРИЯ В КАДРАХ
# =============================================================================

STORY_EDL = [
    # =========================================================================
    # ACT I: ПАРАЛИЧ (0-4s) - Он один, он не играет
    # =========================================================================
    # Длинные планы, slow dissolves, establishing the void

    {"start": 0.0,   "end": 0.5,   "type": "black", "desc": "Pure black - anticipation"},
    {"start": 0.5,   "end": 2.5,   "video": "V4", "src_start": 7.5, "desc": "Empty chair - THE SYMBOL",
     "transition_in": "fade", "fade_duration": 0.8},
    {"start": 2.5,   "end": 4.0,   "video": "V2", "src_start": 0.0, "desc": "Hands on piano - NOT playing",
     "transition_in": "dissolve", "fade_duration": 0.6},

    # =========================================================================
    # ACT II: БОРЬБА (4-10s) - Воспоминания атакуют
    # =========================================================================
    # Метрономный монтаж 0.7s cuts, машинная точность = тревога

    {"start": 4.0,   "end": 4.7,   "video": "V1", "src_start": 0.0, "desc": "Crowd - searching"},
    {"start": 4.7,   "end": 5.4,   "video": "V2", "src_start": 3.7, "desc": "Hands trembling"},
    {"start": 5.4,   "end": 6.1,   "video": "V1", "src_start": 3.7, "desc": "Crowd - faces blur"},
    {"start": 6.1,   "end": 6.8,   "video": "V5", "src_start": 0.0, "desc": "Silhouette - isolation"},
    {"start": 6.8,   "end": 7.5,   "video": "V2", "src_start": 7.3, "desc": "Hands - building intensity"},
    {"start": 7.5,   "end": 8.2,   "video": "V1", "src_start": 0.0, "desc": "Crowd - overwhelming"},
    {"start": 8.2,   "end": 8.9,   "video": "V3", "src_start": 0.0, "desc": "Profile - glimpse of her?"},
    {"start": 8.9,   "end": 9.6,   "video": "V4", "src_start": 0.0, "desc": "Chair - reminder"},
    {"start": 9.6,   "end": 10.0,  "video": "V5", "src_start": 3.7, "desc": "Silhouette - trapped"},

    # =========================================================================
    # ACT III: ЗАТИШЬЕ (10-16.5s) - Vulnerability, замедление
    # =========================================================================
    # Длинные планы, slow motion feeling, building to black

    {"start": 10.0,  "end": 11.8,  "video": "V4", "src_start": 7.5, "desc": "Chair - LONG HOLD - acceptance",
     "slow_motion": 0.7},
    {"start": 11.8,  "end": 13.3,  "video": "V3", "src_start": 3.7, "desc": "Profile - memory of her",
     "slow_motion": 0.8, "transition_in": "dissolve", "fade_duration": 0.4},
    {"start": 13.3,  "end": 14.8,  "video": "V5", "src_start": 7.5, "desc": "Silhouette at piano",
     "slow_motion": 0.8},
    {"start": 14.8,  "end": 16.0,  "video": "V4", "src_start": 3.7, "desc": "Chair again - haunting",
     "transition_in": "dissolve", "fade_duration": 0.5},
    {"start": 16.0,  "end": 16.5,  "video": "V3", "src_start": 7.3, "desc": "Profile fading",
     "transition_out": "fade_to_black", "fade_duration": 0.5},

    # =========================================================================
    # THE BLACK (16.5-17.163s) - 663ms of pure tension
    # =========================================================================

    {"start": 16.5,  "end": 17.163, "type": "black", "desc": "SILENCE - maximum tension"},

    # =========================================================================
    # ACT IV: РЕШЕНИЕ - DROP (17.163s) - SHE APPEARS
    # =========================================================================
    # СВЯЩЕННЫЙ MOMENT - глаза впервые!

    {"start": 17.163, "end": 17.2,  "type": "white_flash", "desc": "EXPLOSION - white flash 37ms"},
    {"start": 17.2,   "end": 17.9,  "video": "V6", "src_start": 14.2, "desc": "GREEN EYES - SHE IS HERE",
     "effect": "zoom_pulse", "eyes_reveal": True},
    {"start": 17.9,   "end": 18.25, "video": "V2", "src_start": 11.0, "desc": "Hands - HE PLAYS"},
    {"start": 18.25,  "end": 18.6,  "video": "V1", "src_start": 7.3, "desc": "Crowd eyes - all her"},
    {"start": 18.6,   "end": 18.95, "video": "V6", "src_start": 7.5, "desc": "Eyes again"},
    {"start": 18.95,  "end": 19.3,  "video": "V2", "src_start": 3.7, "desc": "Hands intensity"},
    {"start": 19.3,   "end": 19.65, "video": "V3", "src_start": 11.0, "desc": "Profile - she listens"},
    {"start": 19.65,  "end": 20.0,  "video": "V6", "src_start": 0.0, "desc": "Eyes - connection"},
    {"start": 20.0,   "end": 20.35, "video": "V1", "src_start": 0.0, "desc": "Crowd flash"},
    {"start": 20.35,  "end": 20.7,  "video": "V2", "src_start": 7.3, "desc": "Hands - passion"},
    {"start": 20.7,   "end": 21.05, "video": "V6", "src_start": 14.2, "desc": "Eyes - building"},
    {"start": 21.05,  "end": 21.451, "video": "V3", "src_start": 3.7, "desc": "Profile into climax"},

    # =========================================================================
    # CLIMAX (21.451s) - THE HOLD - 1.43s of eternity
    # =========================================================================

    {"start": 21.451, "end": 22.88, "video": "V6", "src_start": 14.2, "desc": "CLIMAX - eyes HOLD",
     "effect": "slow_zoom", "climax": True},

    # =========================================================================
    # ACT V: КАТАРСИС (22.88-30s) - Release, she fades
    # =========================================================================
    # Постепенное замедление, она уходит

    {"start": 22.88,  "end": 23.58, "video": "V2", "src_start": 0.0, "desc": "Hands - release"},
    {"start": 23.58,  "end": 24.28, "video": "V6", "src_start": 7.5, "desc": "Eyes - softer now"},
    {"start": 24.28,  "end": 25.0,  "video": "V3", "src_start": 11.0, "desc": "Profile - goodbye",
     "transition_out": "dissolve", "fade_duration": 0.3},
    {"start": 25.0,   "end": 26.0,  "video": "V5", "src_start": 7.5, "desc": "Silhouette - alone again",
     "transition_in": "dissolve", "fade_duration": 0.5},
    {"start": 26.0,   "end": 27.2,  "video": "V2", "src_start": 11.0, "desc": "Hands - slowing"},
    {"start": 27.2,   "end": 28.5,  "video": "V4", "src_start": 7.5, "desc": "Chair - she's gone"},
    {"start": 28.5,   "end": 30.0,  "video": "V5", "src_start": 0.0, "desc": "Silhouette - processing"},

    # =========================================================================
    # ACT VI: ОТПУСКАНИЕ (30-35s) - Letting go
    # =========================================================================

    {"start": 30.0,   "end": 31.5,  "video": "V2", "src_start": 3.7, "desc": "Hands - final notes"},
    {"start": 31.5,   "end": 33.0,  "video": "V4", "src_start": 0.0, "desc": "Chair - empty but okay",
     "transition_in": "dissolve", "fade_duration": 0.6},
    {"start": 33.0,   "end": 34.5,  "video": "V5", "src_start": 7.5, "desc": "Silhouette - peace"},
    {"start": 34.5,   "end": 35.0,  "video": "V4", "src_start": 7.5, "desc": "Chair final",
     "transition_out": "fade_to_black", "fade_duration": 0.5},

    # =========================================================================
    # ACT VII: ПРИНЯТИЕ (35-37s) - OUTRO with branding
    # =========================================================================

    {"start": 35.0,   "end": 37.0,  "type": "outro_card", "desc": "САЙМУРР - СМОТРЕЛА"},
]

# =============================================================================
# VFX FUNCTIONS
# =============================================================================

def cinematic_bw_with_green_isolation(frame, green_intensity=1.0):
    """
    Convert to cinematic B&W but preserve green eyes.
    Green isolation only works on frames with eyes.
    """
    if frame is None:
        return frame

    # Channel mixer B&W (cinema look)
    r, g, b = frame[:,:,0], frame[:,:,1], frame[:,:,2]
    bw = (0.4 * r + 0.35 * g + 0.25 * b).astype(np.uint8)

    # Create HSV for green detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Green mask (for eyes)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Dilate mask slightly
    kernel = np.ones((3, 3), np.uint8)
    green_mask = cv2.dilate(green_mask, kernel, iterations=1)
    green_mask = cv2.GaussianBlur(green_mask, (5, 5), 0)

    # Normalize mask
    mask_normalized = (green_mask / 255.0 * green_intensity).reshape(frame.shape[0], frame.shape[1], 1)

    # Create B&W frame
    bw_frame = np.stack([bw, bw, bw], axis=2)

    # Blend: B&W + green areas in color
    result = bw_frame * (1 - mask_normalized) + frame * mask_normalized

    # Boost green saturation in masked areas
    hsv_result = cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv_result[:,:,1] = np.where(green_mask > 50,
                                  np.minimum(hsv_result[:,:,1] * 1.3, 255),
                                  hsv_result[:,:,1] * 0.1)
    result = cv2.cvtColor(hsv_result.astype(np.uint8), cv2.COLOR_HSV2RGB)

    return result.astype(np.uint8)

def add_film_grain(frame, intensity=0.12, seed=None):
    """Add organic film grain"""
    if seed is not None:
        np.random.seed(seed)

    grain = np.random.normal(0, intensity * 255, frame.shape)
    result = np.clip(frame.astype(np.float32) + grain, 0, 255)
    return result.astype(np.uint8)

def add_vignette(frame, strength=0.4):
    """Add cinematic vignette"""
    rows, cols = frame.shape[:2]

    # Create radial gradient
    X = np.arange(0, cols)
    Y = np.arange(0, rows)
    X, Y = np.meshgrid(X, Y)

    centerX, centerY = cols / 2, rows / 2
    radius = np.sqrt((X - centerX)**2 + (Y - centerY)**2)

    max_radius = np.sqrt(centerX**2 + centerY**2)
    vignette = 1 - (radius / max_radius) ** 2 * strength
    vignette = np.clip(vignette, 0, 1)

    # Apply
    result = frame.astype(np.float32)
    for i in range(3):
        result[:,:,i] = result[:,:,i] * vignette

    return result.astype(np.uint8)

def add_letterbox(frame, bar_height=140):
    """Add 2.39:1 cinematic letterbox"""
    result = frame.copy()
    result[:bar_height, :] = NEAR_BLACK
    result[-bar_height:, :] = NEAR_BLACK
    return result

def create_white_flash(width, height):
    """Create white flash frame for DROP moment"""
    return np.full((height, width, 3), 255, dtype=np.uint8)

# =============================================================================
# PIL TYPOGRAPHY (КИРИЛЛИЦА РАБОТАЕТ!)
# =============================================================================

def create_intro_card_pil(duration=4.0, width=1920, height=1080):
    """
    Create intro card using PIL for proper Cyrillic rendering.
    Shows: ◉ symbol + САЙМУРР
    """
    def make_frame(t):
        # Create black background
        img = Image.new('RGB', (width, height), NEAR_BLACK)
        draw = ImageDraw.Draw(img)

        # Animation phases
        if t < 0.5:
            # Pure black
            alpha = 0.0
        elif t < 1.5:
            # Symbol ◉ fade in
            alpha = min(1.0, (t - 0.5) / 0.8)
        elif t < 2.0:
            # Name fade in
            alpha = 1.0
            name_alpha = min(1.0, (t - 1.5) / 0.5)
        elif t < 3.5:
            # Hold
            alpha = 1.0
            name_alpha = 1.0
        else:
            # Fade out
            fade_progress = (t - 3.5) / 0.5
            alpha = max(0, 1.0 - fade_progress)
            name_alpha = alpha

        if t >= 0.5:
            # Draw eye symbol ◉
            try:
                eye_font = ImageFont.truetype(FONT_PATH_BOLD, 50)
            except:
                eye_font = ImageFont.load_default()

            eye_color = tuple(int(c * alpha) for c in EMERALD_GREEN)

            # Eye position
            eye_x, eye_y = width // 2 - 15, height // 2 - 120
            draw.text((eye_x, eye_y), "◉", fill=eye_color, font=eye_font)

        if t >= 1.5:
            # Draw artist name САЙМУРР
            try:
                name_font = ImageFont.truetype(FONT_PATH_BOLD, 140)
                small_font = ImageFont.truetype(FONT_PATH_REGULAR, 20)
            except:
                name_font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            name_alpha_val = name_alpha if 'name_alpha' in dir() else alpha

            # First letter 'С' in green
            green_color = tuple(int(c * name_alpha_val) for c in EMERALD_GREEN)
            white_color = tuple(int(c * name_alpha_val) for c in OFF_WHITE)
            gray_color = tuple(int(c * name_alpha_val * 0.6) for c in GRAY)

            # Calculate positions for centered text
            # Wide tracking: draw each letter separately
            letters = list("САЙМУРР")
            letter_spacing = 54

            # Get total width
            total_width = 0
            for i, letter in enumerate(letters):
                bbox = draw.textbbox((0, 0), letter, font=name_font)
                total_width += bbox[2] - bbox[0] + letter_spacing
            total_width -= letter_spacing  # Remove last spacing

            start_x = (width - total_width) // 2
            y = height // 2 - 20

            current_x = start_x
            for i, letter in enumerate(letters):
                color = green_color if i == 0 else white_color
                draw.text((current_x, y), letter, fill=color, font=name_font)
                bbox = draw.textbbox((0, 0), letter, font=name_font)
                current_x += bbox[2] - bbox[0] + letter_spacing

            # Transliteration
            trans_text = "s a y m u r r"
            trans_bbox = draw.textbbox((0, 0), trans_text, font=small_font)
            trans_x = (width - (trans_bbox[2] - trans_bbox[0])) // 2
            trans_y = y + 160
            draw.text((trans_x, trans_y), trans_text, fill=gray_color, font=small_font)

        # Convert to numpy
        frame = np.array(img)

        # Add subtle grain
        frame = add_film_grain(frame, intensity=0.08)

        # Add letterbox
        frame = add_letterbox(frame)

        return frame

    return VideoClip(make_frame, duration=duration).with_fps(FPS)

def create_outro_card_pil(duration=2.0, width=1920, height=1080):
    """
    Create outro card using PIL for proper Cyrillic rendering.
    Shows: САЙМУРР / СМОТРЕЛА / look at me
    """
    def make_frame(t):
        # Create black background
        img = Image.new('RGB', (width, height), NEAR_BLACK)
        draw = ImageDraw.Draw(img)

        # Animation: fade in, hold, stay
        if t < 0.5:
            alpha = t / 0.5
        else:
            alpha = 1.0

        try:
            artist_font = ImageFont.truetype(FONT_PATH_BOLD, 90)
            track_font = ImageFont.truetype(FONT_PATH_BOLD, 55)
            sub_font = ImageFont.truetype(FONT_PATH_REGULAR, 22)
            small_font = ImageFont.truetype(FONT_PATH_REGULAR, 16)
        except:
            artist_font = ImageFont.load_default()
            track_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Colors with alpha
        green_color = tuple(int(c * alpha) for c in EMERALD_GREEN)
        white_color = tuple(int(c * alpha) for c in OFF_WHITE)
        gray_color = tuple(int(c * alpha * 0.6) for c in GRAY)

        # Artist name: САЙМУРР (with green С)
        artist_y = height // 2 - 80
        letters = list("САЙМУРР")
        letter_spacing = 35

        # Calculate width
        total_width = 0
        for letter in letters:
            bbox = draw.textbbox((0, 0), letter, font=artist_font)
            total_width += bbox[2] - bbox[0] + letter_spacing
        total_width -= letter_spacing

        start_x = (width - total_width) // 2
        current_x = start_x
        for i, letter in enumerate(letters):
            color = green_color if i == 0 else white_color
            draw.text((current_x, artist_y), letter, fill=color, font=artist_font)
            bbox = draw.textbbox((0, 0), letter, font=artist_font)
            current_x += bbox[2] - bbox[0] + letter_spacing

        # Small transliteration
        trans_text = "s a y m u r r"
        trans_bbox = draw.textbbox((0, 0), trans_text, font=small_font)
        trans_x = (width - (trans_bbox[2] - trans_bbox[0])) // 2
        draw.text((trans_x, artist_y + 100), trans_text, fill=gray_color, font=small_font)

        # Divider line
        line_y = artist_y + 135
        line_width = 80
        line_x = (width - line_width) // 2
        line_color = tuple(int(c * alpha * 0.5) for c in EMERALD_GREEN)
        draw.line([(line_x, line_y), (line_x + line_width, line_y)], fill=line_color, width=2)

        # Track name: СМОТРЕЛА
        track_bbox = draw.textbbox((0, 0), TRACK_NAME, font=track_font)
        track_x = (width - (track_bbox[2] - track_bbox[0])) // 2
        track_y = artist_y + 160
        draw.text((track_x, track_y), TRACK_NAME, fill=white_color, font=track_font)

        # English subtitle
        sub_bbox = draw.textbbox((0, 0), SUBTITLE_EN, font=sub_font)
        sub_x = (width - (sub_bbox[2] - sub_bbox[0])) // 2
        sub_y = track_y + 70
        draw.text((sub_x, sub_y), SUBTITLE_EN, fill=gray_color, font=sub_font)

        # Convert to numpy
        frame = np.array(img)

        # Add subtle grain
        frame = add_film_grain(frame, intensity=0.08)

        # Add letterbox
        frame = add_letterbox(frame)

        return frame

    return VideoClip(make_frame, duration=duration).with_fps(FPS)

# =============================================================================
# CLIP PROCESSING
# =============================================================================

def process_clip(video_key, src_start, duration, entry):
    """Process a single clip from EDL entry"""
    video_path = VIDEOS[video_key]

    try:
        clip = VideoFileClip(video_path)

        # Get subclip
        src_end = min(src_start + duration * 1.5, clip.duration)  # Extra for slow motion
        subclip = clip.subclipped(src_start, src_end)

        # Apply slow motion if specified
        if "slow_motion" in entry:
            speed = entry["slow_motion"]
            subclip = subclip.with_speed_scaled(speed)

        # Ensure correct duration
        if subclip.duration > duration:
            subclip = subclip.subclipped(0, duration)
        elif subclip.duration < duration:
            # Loop if needed
            loops_needed = int(np.ceil(duration / subclip.duration))
            subclip = concatenate_videoclips([subclip] * loops_needed).subclipped(0, duration)

        # Check if this is an eyes clip (after DROP)
        is_eyes_clip = video_key == "V6" or (video_key == "V1" and src_start >= 7.0)
        is_after_drop = entry["start"] >= DROP_TIME

        # Apply VFX using fl_image (frame-level filter)
        def apply_vfx(frame):
            if frame is None:
                return np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

            # Resize if needed
            if frame.shape[:2] != (HEIGHT, WIDTH):
                frame = cv2.resize(frame, (WIDTH, HEIGHT))

            # B&W with green isolation (only for eyes after DROP)
            if is_eyes_clip and is_after_drop:
                frame = cinematic_bw_with_green_isolation(frame, green_intensity=1.0)
            else:
                # Pure B&W for non-eye clips
                frame = cinematic_bw_with_green_isolation(frame, green_intensity=0.0)

            # Add vignette
            frame = add_vignette(frame, strength=0.35)

            # Add grain
            frame = add_film_grain(frame, intensity=0.10)

            # Add letterbox
            frame = add_letterbox(frame)

            return frame

        processed = subclip.image_transform(apply_vfx)

        return processed.with_duration(duration)

    except Exception as e:
        print(f"Error processing {video_key}: {e}")
        # Return black clip on error
        return ColorClip(size=(WIDTH, HEIGHT), color=NEAR_BLACK).with_duration(duration)

def create_black_clip(duration):
    """Create pure black clip"""
    def make_frame(t):
        frame = np.full((HEIGHT, WIDTH, 3), NEAR_BLACK, dtype=np.uint8)
        frame = add_letterbox(frame)
        return frame

    return VideoClip(make_frame, duration=duration).with_fps(FPS)

def create_white_flash_clip(duration=0.037):
    """Create white flash for DROP moment"""
    def make_frame(t):
        frame = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)
        # Quick fade
        if t > 0.02:
            intensity = 1.0 - ((t - 0.02) / 0.017)
            frame = (frame * max(0, intensity)).astype(np.uint8)
        frame = add_letterbox(frame)
        return frame

    return VideoClip(make_frame, duration=duration).with_fps(FPS)

# =============================================================================
# MAIN RENDER
# =============================================================================

def render_teaser():
    """Main render function"""
    print("=" * 80)
    print("  ◉ САЙМУРР — СМОТРЕЛА")
    print("  TEASER V4: \"37 СЕКУНД\"")
    print("=" * 80)
    print()
    print("  История: За 37 секунд он должен решить — отпустить или остаться в боли")
    print("  Правило: Глаза появляются ТОЛЬКО после 17.163s (DROP)")
    print()

    clips = []

    # Process each EDL entry
    for i, entry in enumerate(STORY_EDL):
        start = entry["start"]
        end = entry["end"]
        duration = end - start

        desc = entry.get("desc", "")
        print(f"  [{i+1:02d}/{len(STORY_EDL)}] {start:.3f}s - {end:.3f}s: {desc}")

        entry_type = entry.get("type", "video")

        if entry_type == "black":
            clip = create_black_clip(duration)
        elif entry_type == "white_flash":
            clip = create_white_flash_clip(duration)
        elif entry_type == "outro_card":
            clip = create_outro_card_pil(duration)
        else:
            # Video clip
            video_key = entry["video"]
            src_start = entry.get("src_start", 0.0)
            clip = process_clip(video_key, src_start, duration, entry)

        clips.append(clip)

    print()
    print("  Concatenating clips...")

    # Concatenate all clips
    final = concatenate_videoclips(clips, method="compose")

    # Create intro separately and composite at the beginning
    print("  Creating INTRO card with PIL (САЙМУРР)...")
    intro = create_intro_card_pil(duration=4.0)

    # The intro overlays the first 4 seconds
    # For simplicity, we'll replace the first 4 seconds with intro
    final = concatenate_videoclips([
        intro,
        final.subclipped(4.0, final.duration)
    ])

    # Add audio
    print("  Adding audio...")
    try:
        audio = AudioFileClip(AUDIO_FILE).subclipped(0, TOTAL_DURATION)
        final = final.with_audio(audio)
    except Exception as e:
        print(f"  Warning: Could not load audio: {e}")

    # Render
    print()
    print("  Rendering to:", OUTPUT_FILE)
    print("  This may take a few minutes...")
    print()

    final.write_videofile(
        OUTPUT_FILE,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        bitrate='15M',
        preset='medium',
        threads=4
    )

    print()
    print("=" * 80)
    print("  ✓ RENDER COMPLETE!")
    print(f"  Output: {OUTPUT_FILE}")
    print("=" * 80)

    # Cleanup
    final.close()
    for clip in clips:
        clip.close()

if __name__ == "__main__":
    render_teaser()
