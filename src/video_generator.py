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
    - 1 losowy obraz jako tło (ustawiony na długość audio).
    Zapisuje wynik w output_path.
    
    Dodatkowo tworzy i zwraca ścieżkę do pliku miniaturki (1280x720),
    wygenerowanego z tego samego obrazka.

    Zwraca (thumbnail_path, used_image_path).
    """

    # --- [1] Wybór i przygotowanie plików audio ---
    all_music_files = [
        f for f in os.listdir(music_folder)
        if f.lower().endswith(('.mp3', '.wav', '.ogg'))
    ]
    if len(all_music_files) < 20:
        raise ValueError(
            "W folderze 'music/' nie ma wystarczającej liczby plików audio (min. 20)."
        )

    # Losowo wybieramy 20 plików muzycznych
    random_music_files = random.sample(all_music_files, 20)

    audio_clips = []
    for music_file in random_music_files:
        file_path = os.path.join(music_folder, music_file)
        audio_clip = AudioFileClip(file_path)
        # Fade in/out
        audio_clip = audio_clip.audio_fadein(5).audio_fadeout(5)
        audio_clips.append(audio_clip)

    final_audio = concatenate_audioclips(audio_clips)

    # --- [2] Wybór losowego obrazka ---
    all_image_files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    ]
    if not all_image_files:
        raise ValueError("Brak plików graficznych w folderze 'images/'.")

    random_image_file = random.choice(all_image_files)
    used_image_path = os.path.join(image_folder, random_image_file)

    # Tworzymy ImageClip i ustawiamy czas trwania klipu = długość audio
    image_clip = ImageClip(used_image_path).set_duration(final_audio.duration)

    # --- [3] Tworzymy finalny klip wideo i łączymy go z audio ---
    final_video = image_clip.set_audio(final_audio)

    # --- [4] Zapis wideo ---
    final_video.write_videofile(output_path, fps=1)

    # --- [5] Przygotowanie pliku miniaturki (thumbnail) ---
    base_output_dir = os.path.dirname(output_path)
    thumbnail_path = os.path.join(base_output_dir, "thumbnail.jpg")

    # Wczytujemy oryginalny plik obrazka przez PIL
    with Image.open(used_image_path) as img:
        # 5a. Zmień rozmiar na 1280 x 720 (bez zachowania proporcji)
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)

        # 5b. Zapisz do pliku
        img.save(thumbnail_path, "JPEG", quality=90)

    # Zwracamy ścieżkę do wygenerowanej miniaturki oraz ścieżkę do użytego obrazka
    return thumbnail_path, used_image_path
