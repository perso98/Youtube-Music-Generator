import os
import re
import sys

def force_rename_images(images_folder):
    """
    Próbuje 'na siłę' zmienić nazwy plików w folderze images_folder,
    używając prefixu '\\\\?\\' na Windows i nadając krótką nazwę
    1.webp, 2.webp, itd. (z zachowaniem oryginalnego rozszerzenia).
    """

    valid_extensions = ('.webp', '.jpg', '.jpeg', '.png')
    # Pobierz listę plików
    all_files = os.listdir(images_folder)

    # Filtrowanie tylko z dozwolonym rozszerzeniem
    image_files = []
    for f in all_files:
        ext = os.path.splitext(f)[1].lower()
        if ext in valid_extensions:
            image_files.append(f)

    image_files.sort()  # posortuj, by mieć przewidywalną kolejność

    counter = 1
    for old_name in image_files:
        _, ext = os.path.splitext(old_name)
        new_name = f"{counter}{ext.lower()}"

        old_path = os.path.join(images_folder, old_name)
        new_path = os.path.join(images_folder, new_name)

        # Jeśli jesteś na Windows, spróbuj użyć long path prefix
        # (UWAGA: w Pythonie 3.6+ i Windows 10+ z włączonym 'LongPathsEnabled' w rejestrze)
        if os.name == 'nt':
            old_path = r"\\?\\" + os.path.abspath(old_path)
            new_path = r"\\?\\" + os.path.abspath(new_path)

        try:
            os.rename(old_path, new_path)
            print(f"OK: {old_name} -> {new_name}")
        except Exception as e:
            print(f"ERR: Nie mogę zmienić nazwy '{old_name}': {e}")

        counter += 1
