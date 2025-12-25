#!/usr/bin/env python3
"""
СМОТРЕЛА - Teaser Video Renderer
Кинематографический монтаж с синхронизацией по битам
"""

import os
import numpy as np
from moviepy import *
from moviepy.video.fx import BlackAndWhite, MultiplyColor, CrossFadeIn, CrossFadeOut
import cv2

# Paths
PROJECT_DIR = "/home/user/look-at-me"
AUDIO_PATH = os.path.join(PROJECT_DIR, "СМОТРЕЛА_teaser.wav")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "SMOTRELA_teaser_FINAL.mp4")

# Video files mapping
VIDEOS = {
    'V1': os.path.join(PROJECT_DIR, "20251226_0026_01kdbpca1rfxjtx3zddgv48gjh.mp4"),
    'V2': os.path.join(PROJECT_DIR, "20251226_0130_01kdbr9ggwft8sr8k143r5xfs0.mp4"),
    'V3': os.path.join(PROJECT_DIR, "20251226_0130_01kdbrazryf8wtabs5kk6kvmqx.mp4"),
    'V4': os.path.join(PROJECT_DIR, "20251226_0130_01kdbsc29wehvbem5ertshqfed.mp4"),
    'V5': os.path.join(PROJECT_DIR, "20251226_0131_01kdbsdwn8epg9amf3qtp17qsb.mp4"),
    'V6': os.path.join(PROJECT_DIR, "20251226_0131_01kdbspmg9egv833wj0ngh944a.mp4"),
}

# Track parameters
BPM = 170.5
BEAT_INTERVAL = 60.0 / BPM  # ~0.352s
TOTAL_DURATION = 37.0

print("=" * 60)
print("СМОТРЕЛА - TEASER RENDERER")
print("=" * 60)
print(f"BPM: {BPM}")
print(f"Beat interval: {BEAT_INTERVAL:.3f}s")
print(f"Total duration: {TOTAL_DURATION}s")


# ============================================================
# EFFECTS
# ============================================================

def apply_bw_high_contrast(clip):
    """Apply B&W with high contrast"""
    def process_frame(frame):
        # Convert to grayscale
        gray = np.dot(frame[..., :3], [0.2989, 0.5870, 0.1140])

        # Increase contrast
        contrast = 1.4
        gray = (gray - 128) * contrast + 128
        gray = np.clip(gray, 0, 255)

        # Stack to RGB
        result = np.stack([gray, gray, gray], axis=-1).astype(np.uint8)
        return result

    return clip.image_transform(process_frame)


def apply_green_eyes_effect(clip, intensity=0.85):
    """Keep only green channel in highlights (for eyes effect)"""
    def process_frame(frame):
        # Convert to grayscale for base
        gray = np.dot(frame[..., :3], [0.2989, 0.5870, 0.1140])

        # Detect green-ish areas (eyes)
        hsv = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_RGB2HSV)

        # Green hue range (broader for AI-generated content)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])

        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_mask = cv2.GaussianBlur(green_mask, (5, 5), 0)
        green_mask = green_mask.astype(float) / 255.0

        # Create B&W base
        bw = np.stack([gray, gray, gray], axis=-1)

        # Create green-tinted version
        green_tint = frame.copy().astype(float)
        green_tint[:, :, 0] *= 0.3  # Reduce red
        green_tint[:, :, 1] *= 1.3  # Boost green
        green_tint[:, :, 2] *= 0.3  # Reduce blue
        green_tint = np.clip(green_tint, 0, 255)

        # Blend based on mask
        mask_3d = np.stack([green_mask] * 3, axis=-1)
        result = bw * (1 - mask_3d * intensity) + green_tint * mask_3d * intensity

        return result.astype(np.uint8)

    return clip.image_transform(process_frame)


def add_film_grain(clip, intensity=0.12):
    """Add film grain effect"""
    def process_frame(frame):
        noise = np.random.normal(0, intensity * 255, frame.shape)
        result = frame.astype(float) + noise
        return np.clip(result, 0, 255).astype(np.uint8)

    return clip.image_transform(process_frame)


def add_vignette(clip, strength=0.3):
    """Add vignette effect"""
    def process_frame(frame):
        h, w = frame.shape[:2]

        # Create vignette mask
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h / 2, w / 2

        # Distance from center, normalized
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        dist = dist / max_dist

        # Vignette falloff
        vignette = 1 - (dist ** 2) * strength
        vignette = np.clip(vignette, 0, 1)

        # Apply
        result = frame.astype(float) * vignette[:, :, np.newaxis]
        return result.astype(np.uint8)

    return clip.image_transform(process_frame)


def create_flash_frame(duration=0.05, size=(1920, 1080)):
    """Create white flash frame"""
    return ColorClip(size=size, color=(255, 255, 255), duration=duration)


def create_black_frame(duration, size=(1920, 1080)):
    """Create black frame"""
    return ColorClip(size=size, color=(0, 0, 0), duration=duration)


# ============================================================
# CLIP HELPERS
# ============================================================

def load_and_prepare(video_key, start_time, duration, with_green_eyes=False):
    """Load a video segment and apply base effects"""
    path = VIDEOS[video_key]

    # Load video
    video = VideoFileClip(path)

    # Ensure we don't exceed video duration
    end_time = min(start_time + duration, video.duration - 0.1)
    actual_duration = end_time - start_time

    if actual_duration <= 0:
        # Fallback: use last available segment
        start_time = max(0, video.duration - duration - 0.1)
        end_time = video.duration - 0.1
        actual_duration = end_time - start_time

    # Cut segment
    clip = video.subclipped(start_time, end_time)

    # Resize to 1080p
    clip = clip.resized(height=1080)

    # Center crop to 1920x1080 if needed
    if clip.w > 1920:
        x_center = clip.w // 2
        clip = clip.cropped(x1=x_center - 960, x2=x_center + 960)

    # Apply effects
    if with_green_eyes:
        clip = apply_green_eyes_effect(clip)
    else:
        clip = apply_bw_high_contrast(clip)

    clip = add_vignette(clip, 0.25)
    clip = add_film_grain(clip, 0.08)

    return clip


# ============================================================
# EDL - EDIT DECISION LIST
# ============================================================

def build_edit_list():
    """Build the complete edit decision list"""

    edl = []

    # СЕКЦИЯ 1: INTRO (0.0 - 4.32s)
    edl.append(('black', 0.0, 0.35, {}))
    edl.append(('V4', 0.35, 1.45, {'src_start': 7.5, 'zoom': 1.05}))  # Пустой стул
    edl.append(('V2', 1.45, 2.93, {'src_start': 0.0}))  # Руки на пианино
    edl.append(('V5', 2.93, 4.32, {'src_start': 7.5}))  # Силуэт

    # СЕКЦИЯ 2: BUILD-UP (4.32 - 10.0s)
    edl.append(('V1', 4.32, 5.02, {'src_start': 0.0}))  # Толпа
    edl.append(('V3', 5.02, 5.73, {'src_start': 0.0}))  # Руки blur
    edl.append(('V1', 5.73, 6.43, {'src_start': 3.7}))  # Толпа ближе
    edl.append(('V4', 6.43, 7.18, {'src_start': 0.0}))  # Руки клавиши
    edl.append(('V3', 7.18, 8.62, {'src_start': 3.7}))  # Экспрессия
    edl.append(('V6', 8.62, 9.31, {'src_start': 0.0}))  # Руки интенсивно
    edl.append(('V2', 9.31, 10.0, {'src_start': 7.3}))  # Арка

    # СЕКЦИЯ 3: PRE-DROP (10.0 - 17.16s)
    edl.append(('V4', 10.0, 11.41, {'src_start': 7.5, 'slow': 0.7}))  # Стул slow
    edl.append(('V5', 11.41, 12.78, {'src_start': 14.0}))  # Профиль
    edl.append(('V3', 12.78, 14.27, {'src_start': 7.3}))  # Стул штора
    edl.append(('V6', 14.27, 15.82, {'src_start': 7.5, 'zoom': 1.1}))  # Стул прожектор
    edl.append(('V4', 15.82, 16.50, {'src_start': 14.0}))  # Глаз
    edl.append(('black', 16.50, 17.16, {}))  # Тишина перед DROP

    # СЕКЦИЯ 4: DROP (17.16 - 25.0s) - ГЛАВНАЯ ЧАСТЬ!
    edl.append(('V1', 17.16, 17.51, {'src_start': 7.3, 'green_eyes': True, 'flash': True}))  # ГЛАЗА #1
    edl.append(('V6', 17.51, 17.87, {'src_start': 0.0}))  # Руки удар
    edl.append(('V3', 17.87, 18.51, {'src_start': 11.0, 'green_eyes': True}))  # ГЛАЗА #2
    edl.append(('V1', 18.51, 19.2, {'src_start': 0.0}))  # Толпа
    edl.append(('V4', 19.2, 19.89, {'src_start': 0.0}))  # Руки
    edl.append(('flash', 19.89, 20.02, {}))  # Белая вспышка
    edl.append(('V6', 20.02, 20.73, {'src_start': 14.0, 'green_eyes': True, 'slow': 0.6}))  # ГЛАЗА прямо
    edl.append(('V1', 20.73, 21.45, {'src_start': 3.7}))  # Толпа
    edl.append(('V6', 21.45, 22.88, {'src_start': 14.0, 'green_eyes': True, 'zoom': 1.15}))  # КУЛЬМИНАЦИЯ
    edl.append(('V3', 22.88, 23.58, {'src_start': 0.0}))  # Движение
    edl.append(('V1', 23.58, 24.3, {'src_start': 7.3, 'green_eyes': True}))  # Глаза
    edl.append(('V4', 24.3, 25.0, {'src_start': 11.0}))  # Руки сверху

    # СЕКЦИЯ 5: PEAK (25.0 - 34.3s)
    edl.append(('V5', 25.0, 25.71, {'src_start': 0.0}))  # Руки blur
    edl.append(('V3', 25.71, 26.41, {'src_start': 11.0, 'green_eyes': True}))  # Глаза
    edl.append(('V1', 26.41, 27.16, {'src_start': 0.0}))  # Толпа
    edl.append(('V4', 27.16, 28.58, {'src_start': 7.5}))  # Стул + пианист
    edl.append(('V6', 28.58, 29.28, {'src_start': 11.0}))  # Руки мягко
    edl.append(('V1', 29.28, 30.0, {'src_start': 7.3, 'green_eyes': True}))  # Глаза
    edl.append(('V6', 30.0, 31.4, {'src_start': 14.0, 'green_eyes': True, 'slow': 0.7}))  # Взгляд slow
    edl.append(('V5', 31.4, 32.85, {'src_start': 7.5}))  # Силуэт
    edl.append(('V2', 32.85, 34.29, {'src_start': 0.0, 'slow': 0.8}))  # Руки финал

    # СЕКЦИЯ 6: OUTRO (34.29 - 37.0s)
    edl.append(('V4', 34.29, 35.72, {'src_start': 7.5, 'zoom': 0.95}))  # Стул финал
    edl.append(('V6', 35.72, 36.5, {'src_start': 14.0, 'green_eyes': True, 'fade': True}))  # Последний взгляд
    edl.append(('black', 36.5, 37.0, {}))  # Финал

    return edl


# ============================================================
# MAIN RENDER
# ============================================================

def render_teaser():
    print("\n[1/4] Loading EDL...")
    edl = build_edit_list()
    print(f"      {len(edl)} cuts defined")

    print("\n[2/4] Building clips...")
    clips = []

    for i, entry in enumerate(edl):
        source = entry[0]
        start = entry[1]
        end = entry[2]
        opts = entry[3] if len(entry) > 3 else {}

        duration = end - start

        print(f"      [{i+1:02d}/{len(edl)}] {source} @ {start:.2f}s - {end:.2f}s ({duration:.2f}s)")

        if source == 'black':
            clip = create_black_frame(duration)
        elif source == 'flash':
            clip = create_flash_frame(duration)
        else:
            src_start = opts.get('src_start', 0.0)
            with_green = opts.get('green_eyes', False)

            clip = load_and_prepare(source, src_start, duration * 1.5, with_green_eyes=with_green)

            # Trim to exact duration
            if clip.duration > duration:
                clip = clip.subclipped(0, duration)

            # Apply slow motion if specified
            if 'slow' in opts:
                # For slow motion, we need more source material
                speed = opts['slow']
                clip = clip.with_speed_scaled(speed)
                if clip.duration > duration:
                    clip = clip.subclipped(0, duration)

            # Apply zoom if specified
            if 'zoom' in opts:
                zoom_factor = opts['zoom']
                clip = clip.resized(zoom_factor)
                # Re-crop to 1920x1080
                if clip.w > 1920 or clip.h > 1080:
                    clip = clip.cropped(
                        x1=(clip.w - 1920) // 2,
                        x2=(clip.w + 1920) // 2,
                        y1=(clip.h - 1080) // 2,
                        y2=(clip.h + 1080) // 2
                    )

        # Ensure exact duration
        if hasattr(clip, 'duration') and clip.duration != duration:
            clip = clip.with_duration(duration)

        # Add flash before green eyes clips on DROP
        if opts.get('flash', False):
            flash = create_flash_frame(0.03)
            clips.append(flash)

        clips.append(clip)

    print("\n[3/4] Concatenating clips...")
    final_video = concatenate_videoclips(clips, method="compose")

    # Trim to exact duration
    if final_video.duration > TOTAL_DURATION:
        final_video = final_video.subclipped(0, TOTAL_DURATION)

    print(f"      Video duration: {final_video.duration:.2f}s")

    print("\n[4/4] Adding audio and rendering...")
    audio = AudioFileClip(AUDIO_PATH)
    if audio.duration > TOTAL_DURATION:
        audio = audio.subclipped(0, TOTAL_DURATION)

    final_video = final_video.with_audio(audio)

    # Render
    final_video.write_videofile(
        OUTPUT_PATH,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        bitrate='8000k',
        preset='medium',
        threads=4
    )

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    render_teaser()
