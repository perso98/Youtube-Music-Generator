import os
from datetime import datetime, timedelta

from src.video_generator import create_final_video
from src.title_manager import get_title_and_remove
from src.youtube_uploader import upload_to_youtube, set_thumbnail
from src.file_manager import force_rename_images

def main():
    # 1. Wczytaj dane od użytkownika
    start_date_str = input("Podaj datę początkową w formacie YYYY-MM-DD (np. 2024-01-15): ")
    num_videos = int(input("Ile filmów chcesz wygenerować i zaplanować? "))

    # 2. Konwersja do obiektu datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    # 3. Ścieżki do folderów
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder, gdzie jest main.py
    images_folder = os.path.join(BASE_DIR, "resources", "images")
    music_folder = os.path.join(BASE_DIR, "resources", "music")
    titles_file = os.path.join(BASE_DIR, "data", "titles.txt")
    output_dir = os.path.join(BASE_DIR, "output")

    # Najpierw zmień nazwy plików w folderze images (aby uniknąć dziwnych znaków itd.)
    print("\n==> Oczyszczanie nazw plików w folderze images...")
    force_rename_images(images_folder)

    # 4. Generuj i uploaduj w pętli
    for i in range(num_videos):
        # Wylicz datę publikacji: start_date + i dni
        publish_date = start_date + timedelta(days=i)
        # Konwersja na format RFC3339, np. "2024-12-31T12:00:00.000Z"
        publish_date_str = publish_date.strftime("%Y-%m-%dT12:00:00.000Z")

        # Przygotuj ścieżkę do pliku wyjściowego
        output_filename = f"final_output_{i+1}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        # 4a. Generowanie wideo
        print(f"\n[{i+1}/{num_videos}] Generuję wideo: {output_filename}")
        # Jeśli Twoja funkcja create_final_video zwraca ścieżkę do miniaturki, odbierz ją tutaj:
        thumbnail_path = create_final_video(
            music_folder=music_folder,
            image_folder=images_folder,
            output_path=output_path
        )
        print(f"Wideo {output_filename} wygenerowane.")

        # 4b. Pobierz tytuł z pliku
        title = get_title_and_remove(titles_file)
        if not title:
            print("Brak tytułów w titles.txt! Przerywam dalsze generowanie.")
            break
        print(f"Użyty tytuł: {title}")

        # 4c. Upload na YouTube – planowana publikacja = publish_date_str
        print("Rozpoczynam upload na YouTube...")
        video_id = upload_to_youtube(
            video_file=output_path,
            title=title,
            # UWAGA: nie przekazujemy opisu,
            # żeby użyć domyślnego (zdefiniowanego w youtube_uploader).
            privacy_status="private",  
            category_id="10",          # 10 = Music
            publish_at=publish_date_str
        )
        print(f"Upload zakończony. Data publikacji (zaplanujesz w YT): {publish_date_str}")

        # 4d. Ustaw miniaturkę, jeśli mamy video_id i thumbnail_path
        if video_id and thumbnail_path and os.path.exists(thumbnail_path):
            set_thumbnail(video_id, thumbnail_path)
            print("Miniaturka ustawiona.")
            # (opcjonalnie) usuń miniaturkę
            os.remove(thumbnail_path)
            print(f"Usunięto lokalny plik miniaturki: {thumbnail_path}")

        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"Usunięto lokalny plik wideo: {output_path}")

if __name__ == "__main__":
    main()
