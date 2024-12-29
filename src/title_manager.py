def get_title_and_remove(titles_file):
    """
    Pobiera pierwszą linię z pliku titles_file,
    usuwa ją z tego pliku, zwraca pobrany tytuł (string).
    Zwraca None, jeżeli plik jest pusty.
    """
    with open(titles_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return None  # plik pusty, brak tytułów

    title = lines[0].strip()  # pierwszy tytuł

    # Nadpisz plik, pomijając pierwszą linię
    with open(titles_file, "w", encoding="utf-8") as f:
        f.writelines(lines[1:])

    return title
