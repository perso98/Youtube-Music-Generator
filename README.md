# Youtube-Music-Generator

## Przegląd

YouTube Music Generator to zautomatyzowane narzędzie do tworzenia i przesyłania filmów muzycznych na YouTube. Program łączy grafikę z dźwiękami, tworząc unikalne filmy z miniaturkami. Dodatkowo planuje publikację filmów na podstawie określonej daty początkowej i liczby filmów do opublikowania.

## Funkcje

- **Losowe tworzenie treści**: Program wybiera losowo obrazki i nuty do generowania filmów.
- **Automatyczne planowanie**: Publikacja 2 filmów dziennie o 7:00 i 19:00, począwszy od wybranej daty.
- **Tworzenie miniaturek**: Generowanie miniaturek z wybranych obrazów dla każdego filmu.
- **Przetwarzanie wsadowe**: Obsługa masowego generowania i przesyłania filmów na podstawie zadanej liczby.
- **Tytuł**: Dodawanie tytułu dla filmu z pliku.

## Struktura folderów

```
resources/
├── images/      # Folder przechowujący pliki graficzne
├── music/       # Folder przechowujący pliki z nutami
data/            # Folder przechowujący plik z tytułami
src/             # Folder zawierający funkcje
```

![image](https://github.com/user-attachments/assets/5cc88fa8-9d58-4fb6-a0d0-e09207444f1e)


## Jak to działa

1. **Parametry wejściowe**: Uruchom program, a następnie podaj datę początkową oraz liczbę filmów do wygenerowania zgodnie z instrukcjami wyświetlanymi przez program.
   
   ![image](https://github.com/user-attachments/assets/4de24c36-00a0-4155-8be3-db83cd5abf4f)

3. **Generowanie filmów**: Program losowo wybiera obraz z folderu `images` i łączy go z 20 losowymi nutami z folderu `music`.
4. **Tworzenie miniaturek**: Tworzy miniaturkę z wybranego obrazu.
5. **Planowanie**: Rozkłada filmy równomiernie na dni, publikując 2 filmy dziennie o 7:00 i 19:00.
6. **Przesyłanie**: Automatycznie przesyła filmy na YouTube wraz z wygenerowanymi miniaturkami i tytułem pobranym z folderu data plik titles.txt.

**Wynik**:

![image](https://github.com/user-attachments/assets/656a9d00-1301-403a-9d05-9ffb7b565879)


## Wymagania

- Python 3.x
- Biblioteki wymienione w pliku `requirements.txt`
- Włączone i skonfigurowane API danych YouTube z odpowiednimi poświadczeniami

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   gh repo clone perso98/Youtube-Music-Generator
   ```
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Skonfiguruj poświadczenia API YouTube.

## Uwagi

- Upewnij się, że foldery `images` i `music` zawierają wystarczającą liczbę plików do wygenerowania żądanej liczby filmów.
- Sprawdź limity API, aby uniknąć przekroczenia dostępnych zasobów podczas masowego przesyłania.


