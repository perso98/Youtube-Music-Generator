import os
import random
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    concatenate_audioclips
)
from moviepy.video.fx import all as vfx
from PIL import Image, ImageEnhance

def create_final_video(music_folder, image_folder, output_path):
    """
    Generuje finalny plik wideo (output.mp4), łącząc:
    - 20 losowych utworów muzycznych (z 5s fade in/out),
    - 1 losowy obraz jako tło (lekko przyciemniony i z dodanym kontrastem).
    Zapisuje wynik w output_path.
    
    Dodatkowo tworzy i zwraca ścieżkę do pliku miniaturki (1280x720),
    wygenerowanego z tego samego obrazka z przybliżonymi tymi samymi efektami.
    """

    # --- [1] Wybór i przygotowanie plików audio ---
    all_music_files = [
        f for f in os.listdir(music_folder)
        if f.lower().endswith(('.mp3', '.wav', '.ogg'))
    ]
    if len(all_music_files) < 20:
        raise ValueError("W folderze 'music/' nie ma wystarczającej liczby plików audio (min. 20).")

    random_music_files = random.sample(all_music_files, 20)

    audio_clips = []
    for music_file in random_music_files:
        file_path = os.path.join(music_folder, music_file)
        audio_clip = AudioFileClip(file_path)
        # Fade in/out
        audio_clip = audio_clip.audio_fadein(5).audio_fadeout(5)
        audio_clips.append(audio_clip)

    final_audio = concatenate_audioclips(audio_clips)

    # --- [2] Wybór losowego obrazka + obróbka (MoviePy) ---
    all_image_files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    ]
    if not all_image_files:
        raise ValueError("Brak plików graficznych w folderze 'images/'.")

    random_image_file = random.choice(all_image_files)
    image_path = os.path.join(image_folder, random_image_file)

    # Tworzymy ImageClip
    image_clip = ImageClip(image_path)

    # Przyciemnianie i zwiększenie kontrastu (MoviePy)
    image_clip = image_clip.fx(vfx.colorx, 0.9)  # ~10% ciemniej
    image_clip = image_clip.fx(vfx.lum_contrast, lum=0, contrast=1.2, contrast_thr=128)

    # Ustawiamy czas trwania klipu graficznego = długość audio
    image_clip = image_clip.set_duration(final_audio.duration)

    # --- [3] Tworzymy finalny klip wideo ---
    final_video = image_clip.set_audio(final_audio)

    # --- [4] Zapis wideo ---
    final_video.write_videofile(output_path, fps=1)

    # --- [5] Przygotowanie pliku miniaturki (thumbnail) ---
    #    Tu używamy PIL (Pillow), by:
    #     1) Załadować oryginalny obraz
    #     2) Zastosować przyciemnianie i kontrast
    #     3) Zmienić rozmiar na 1280x720
    #     4) Zapisać jako thumbnail.jpg

    base_output_dir = os.path.dirname(output_path)  # folder, gdzie powstał finalny mp4
    thumbnail_path = os.path.join(base_output_dir, "thumbnail.jpg")

    # Wczytujemy oryginalny plik obrazka przez PIL
    with Image.open(image_path) as img:
        # 5a. Przyciemnianie (np. współczynnik 0.9)
        brightness_enhancer = ImageEnhance.Brightness(img)
        img = brightness_enhancer.enhance(0.9)

        # 5b. Zwiększenie kontrastu (np. współczynnik 1.2)
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(1.2)

        # 5c. Zmień rozmiar na 1280 x 720 (bez zachowania proporcji)
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)

        # 5d. Zapisz do pliku
        img.save(thumbnail_path, "JPEG", quality=90)

    # Zwracamy ścieżkę do wygenerowanej miniaturki, by użyć jej np. w uploadzie YouTube
    return thumbnail_path
