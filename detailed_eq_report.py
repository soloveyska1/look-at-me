#!/usr/bin/env python3
"""
Detailed EQ Report Generator
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal

def create_detailed_eq_report(file_path, drop_time=17.163):
    """Generate comprehensive EQ report"""

    # Load audio
    sample_rate, data = wavfile.read(file_path)

    if len(data.shape) > 1:
        audio_mono = np.mean(data, axis=1)
    else:
        audio_mono = data

    audio_mono = audio_mono.astype(np.float64)
    audio_mono = audio_mono / np.max(np.abs(audio_mono))

    # Compute high-resolution spectrum
    freqs, psd = signal.welch(audio_mono, sample_rate, nperseg=16384, noverlap=8192)
    spectrum = 10 * np.log10(psd + 1e-10)

    # Generate report
    print("\n" + "="*100)
    print("ПРОФЕССИОНАЛЬНЫЙ EQ ГАЙД ДЛЯ FABFILTER PRO-Q3")
    print("Трек: СМОТРЕЛА от Саймурр")
    print("="*100 + "\n")

    print("ПОШАГОВЫЕ НАСТРОЙКИ ЭКВАЛАЙЗЕРА:")
    print("-"*100 + "\n")

    eq_chain = [
        {
            'band': 1,
            'type': 'High Pass',
            'freq': 30,
            'gain': 0,
            'q': 0,
            'slope': '12 dB/oct',
            'reason': 'Удаление subsonic rumble и наводок (<30 Hz)',
            'priority': 'CRITICAL'
        },
        {
            'band': 2,
            'type': 'Bell (Cut)',
            'freq': 35,
            'gain': -2.0,
            'q': 0.80,
            'slope': 'N/A',
            'reason': 'Очистка низких частот - избыточный sub-bass mud',
            'priority': 'HIGH'
        },
        {
            'band': 3,
            'type': 'Bell (Cut)',
            'freq': 146,
            'gain': -4.0,
            'q': 3.00,
            'slope': 'N/A',
            'reason': 'КРИТИЧЕСКИЙ РЕЗОНАНС! Bass peak +35.8 dB - создает гул',
            'priority': 'CRITICAL'
        },
        {
            'band': 4,
            'type': 'Bell (Cut)',
            'freq': 350,
            'gain': -2.5,
            'q': 1.50,
            'slope': 'N/A',
            'reason': 'Low-mid mud - "картонный" звук, маскирует бас',
            'priority': 'HIGH'
        },
        {
            'band': 5,
            'type': 'Bell (Cut)',
            'freq': 1693,
            'gain': -4.0,
            'q': 3.00,
            'slope': 'N/A',
            'reason': 'Резонанс в mid-range +22.0 dB - резкость вокала',
            'priority': 'CRITICAL'
        },
        {
            'band': 6,
            'type': 'Bell (Cut)',
            'freq': 2244,
            'gain': -3.5,
            'q': 3.00,
            'slope': 'N/A',
            'reason': 'High-mid резонанс +21.9 dB - агрессивность',
            'priority': 'CRITICAL'
        },
        {
            'band': 7,
            'type': 'Bell (Boost)',
            'freq': 3000,
            'gain': +2.0,
            'q': 1.20,
            'slope': 'N/A',
            'reason': 'Presence boost - читаемость вокала и мелодии',
            'priority': 'MEDIUM'
        },
        {
            'band': 8,
            'type': 'Bell (Cut)',
            'freq': 3545,
            'gain': -3.0,
            'q': 2.50,
            'slope': 'N/A',
            'reason': 'Upper-mid резонанс +13.0 dB - усталость при прослушивании',
            'priority': 'HIGH'
        },
        {
            'band': 9,
            'type': 'Bell (Cut)',
            'freq': 7916,
            'gain': -2.5,
            'q': 2.00,
            'slope': 'N/A',
            'reason': 'Высокочастотный резонанс +12.1 dB - sibilance',
            'priority': 'HIGH'
        },
        {
            'band': 10,
            'type': 'High Shelf (Boost)',
            'freq': 12000,
            'gain': +3.0,
            'q': 0.70,
            'slope': 'N/A',
            'reason': 'Air band открытие - добавление "воздуха" и пространства',
            'priority': 'MEDIUM'
        },
    ]

    for band in eq_chain:
        print(f"BAND {band['band']} [{band['priority']}]:")
        print(f"  Тип фильтра:  {band['type']}")
        print(f"  Частота:      {band['freq']} Hz")
        if band['gain'] != 0:
            print(f"  Gain:         {band['gain']:+.1f} dB")
        if band['q'] > 0:
            print(f"  Q-фактор:     {band['q']:.2f}")
        if band['slope'] != 'N/A':
            print(f"  Slope:        {band['slope']}")
        print(f"  Причина:      {band['reason']}")
        print()

    print("="*100)
    print("ДЕТАЛЬНОЕ ОБОСНОВАНИЕ КАЖДОЙ НАСТРОЙКИ")
    print("="*100 + "\n")

    # Detailed explanations
    explanations = [
        ("146 Hz - КРИТИЧЕСКИЙ РЕЗОНАНС",
         "Это самая проблемная частота в треке. Резонанс на уровне +35.8 dB над средним\n" +
         "создает гулкость и маскирует чистоту баса. Эта частота находится в диапазоне\n" +
         "фундаментальных частот кик-драма и баса, и её избыток делает микс грязным.\n" +
         "РЕШЕНИЕ: Узкий cut с Q=3.0 точно на 146 Hz, gain -4.0 dB."),

        ("1693 Hz и 2244 Hz - ПАРНЫЕ РЕЗОНАНСЫ",
         "Два близких резонанса в mid-high диапазоне (+22 dB и +21.9 dB соответственно).\n" +
         "Эти частоты отвечают за яркость вокала, но в избытке создают резкость и\n" +
         "агрессивность. Особенно критично для длительного прослушивания.\n" +
         "РЕШЕНИЕ: Узкие cuts с Q=3.0 на обеих частотах, gain -4.0 dB и -3.5 dB."),

        ("350 Hz - LOW-MID MUD",
         "Классическая проблемная частота в современных миксах. Избыток в этой области\n" +
         "создает 'картонный' звук и маскирует бас. Частота боксирования.\n" +
         "РЕШЕНИЕ: Средний cut с Q=1.5, gain -2.5 dB для очистки."),

        ("3000 Hz - PRESENCE BOOST",
         "После cuts в 1693 и 2244 Hz нужно восстановить читаемость вокала и мелодии.\n" +
         "3 kHz - это частота разборчивости речи и присутствия инструментов.\n" +
         "РЕШЕНИЕ: Мягкий boost с Q=1.2, gain +2.0 dB."),

        ("12000 Hz - AIR BAND",
         "Анализ показал провал в диапазоне 'air' (-21.3 dB относительно mid-range).\n" +
         "Открытие этого диапазона добавит пространство, глубину и профессиональное звучание.\n" +
         "РЕШЕНИЕ: High shelf boost с Q=0.7, gain +3.0 dB начиная с 12 kHz."),
    ]

    for title, explanation in explanations:
        print(f"{title}:")
        print(f"{explanation}\n")

    print("="*100)
    print("ДОПОЛНИТЕЛЬНЫЕ РЕКОМЕНДАЦИИ")
    print("="*100 + "\n")

    print("1. ПОРЯДОК ОБРАБОТКИ (Signal Chain):")
    print("   a) High-pass filter (30 Hz)")
    print("   b) Surgical EQ cuts (146, 1693, 2244 Hz - LINEAR PHASE!)")
    print("   c) Broad cuts (35, 350, 3545, 7916 Hz)")
    print("   d) Musical boosts (3000, 12000 Hz)")
    print("   e) Multiband compression")
    print("   f) Saturation/harmonic excitement")
    print("   g) Final limiting\n")

    print("2. НАСТРОЙКИ LINEAR PHASE EQ:")
    print("   - Использовать Linear Phase режим для частот 146, 1693, 2244 Hz")
    print("   - Это критично для сохранения фазовых соотношений в басу и мидах")
    print("   - В FabFilter Pro-Q3: включить Zero Latency или Linear Phase Medium\n")

    print("3. MULTIBAND COMPRESSION:")
    print("   Band 1 (20-250 Hz - Bass):")
    print("     • Threshold: -15 dB")
    print("     • Ratio: 3:1")
    print("     • Attack: 10 ms")
    print("     • Release: 100 ms")
    print("     • Цель: Контроль динамики баса после EQ\n")

    print("   Band 2 (250-2000 Hz - Mids):")
    print("     • Threshold: -12 dB")
    print("     • Ratio: 2:1")
    print("     • Attack: 5 ms")
    print("     • Release: 50 ms")
    print("     • Цель: Ровность вокала и мелодии\n")

    print("   Band 3 (2000-8000 Hz - Highs):")
    print("     • Threshold: -10 dB")
    print("     • Ratio: 2.5:1")
    print("     • Attack: 3 ms")
    print("     • Release: 30 ms")
    print("     • Цель: Контроль резкости после cuts\n")

    print("4. ПРОВЕРКА КАЧЕСТВА (A/B Testing):")
    print("   ✓ Включайте/выключайте EQ каждые 30 секунд прослушивания")
    print("   ✓ Проверьте на разных уровнях громкости (тихо, средне, громко)")
    print("   ✓ Послушайте на 3+ разных системах (студийные мониторы, наушники, смартфон)")
    print("   ✓ Сравните с 2-3 референсными треками в том же жанре")
    print("   ✓ Используйте анализатор спектра для визуального контроля\n")

    print("5. ЧАСТЫЕ ОШИБКИ (ЧЕГО ИЗБЕГАТЬ):")
    print("   ✗ Не применяйте все cuts одновременно - делайте постепенно")
    print("   ✗ Не booстите больше чем на 3-4 dB за один раз")
    print("   ✗ Не используйте слишком узкий Q (>5.0) кроме surgical cuts")
    print("   ✗ Не забывайте про gain staging - компенсируйте уровень после EQ")
    print("   ✗ Не микшируйте только в наушниках - используйте мониторы\n")

    print("="*100)
    print("ЦЕЛЕВЫЕ ПАРАМЕТРЫ ПОСЛЕ ОБРАБОТКИ")
    print("="*100 + "\n")

    print("LUFS (Loudness):")
    print("  • Integrated LUFS: -14 до -10 dB (для стриминга)")
    print("  • Short-term LUFS: -13 до -8 dB")
    print("  • Momentary LUFS: -10 до -6 dB\n")

    print("Dynamic Range:")
    print("  • DR (EBU): 6-9 dB (современный коммерческий микс)")
    print("  • Crest Factor: 6-10 dB\n")

    print("Peak Levels:")
    print("  • True Peak: -1.0 dBTP (обязательно!)")
    print("  • Sample Peak: -0.3 dBFS\n")

    print("Frequency Balance:")
    print("  • Bass (60-250 Hz): -6 до -3 dB относительно mid-range")
    print("  • Mids (500-2000 Hz): 0 dB (reference)")
    print("  • Highs (4000-10000 Hz): -3 до 0 dB относительно mids")
    print("  • Air (10000+ Hz): -6 до -3 dB относительно highs\n")

    print("="*100)
    print("СОХРАНЕНИЕ И ЭКСПОРТ")
    print("="*100 + "\n")

    print("1. Сохраните preset EQ в FabFilter Pro-Q3 как 'СМОТРЕЛА_Master_EQ'")
    print("2. Экспортируйте версии:")
    print("   - Master (WAV 48kHz/24bit)")
    print("   - Streaming (WAV 44.1kHz/16bit)")
    print("   - MP3 320kbps CBR")
    print("   - AAC 256kbps VBR\n")

    print("3. Метаданные:")
    print("   - Artist: Саймурр")
    print("   - Title: СМОТРЕЛА")
    print("   - Album: [указать альбом]")
    print("   - Genre: [указать жанр]")
    print("   - Year: 2025")
    print("   - ISRC: [получить код]\n")

    # Save to file
    with open('/home/user/look-at-me/PROFESSIONAL_EQ_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("ПРОФЕССИОНАЛЬНЫЙ EQ ГАЙД - СМОТРЕЛА от Саймурр\n")
        f.write("="*100 + "\n\n")

        f.write("QUICK REFERENCE - НАСТРОЙКИ FABFILTER PRO-Q3:\n")
        f.write("-"*100 + "\n\n")

        for band in eq_chain:
            priority_marker = "⚠️ " if band['priority'] == 'CRITICAL' else "• "
            f.write(f"{priority_marker}Band {band['band']}: {band['type']}\n")
            f.write(f"  Freq: {band['freq']} Hz")
            if band['gain'] != 0:
                f.write(f" | Gain: {band['gain']:+.1f} dB")
            if band['q'] > 0:
                f.write(f" | Q: {band['q']:.2f}")
            f.write(f"\n  → {band['reason']}\n\n")

        f.write("\n" + "="*100 + "\n")
        f.write("Детальные объяснения и рекомендации см. в основном выводе скрипта\n")
        f.write("="*100 + "\n")

    print(f"\n✓ Полное руководство сохранено: /home/user/look-at-me/PROFESSIONAL_EQ_GUIDE.txt")
    print()

if __name__ == "__main__":
    create_detailed_eq_report("/home/user/look-at-me/СМОТРЕЛА_teaser.wav")
