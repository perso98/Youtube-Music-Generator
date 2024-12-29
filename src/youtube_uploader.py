import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube(client_secret_file="client_secret.json", token_file="token.pickle"):
    """
    Uwierzytelnia w YouTube Data API, zwraca obiekt `youtube`.
    """
    creds = None

    # Wczytanie istniejącego tokena, jeśli istnieje
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)

    # Odśwież token lub przeprowadź ponowną autoryzację
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Błąd podczas odświeżania tokena: {e}")
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_file,
                    SCOPES
                )
                creds = flow.run_local_server(port=8080)
            except Exception as e:
                print(f"Błąd podczas autoryzacji: {e}")
                return None

        # Zapisanie nowego tokena
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)

    try:
        youtube = build("youtube", "v3", credentials=creds)
        return youtube
    except Exception as e:
        print(f"Błąd tworzenia obiektu YouTube API: {e}")
        return None

def upload_to_youtube(
    video_file,
    title,
    description=None,
    tags=None,
    privacy_status="private",
    category_id="10",
    publish_at=None
):
    """
    Uploaduje video_file na kanał YouTube z podanym tytułem, opisem i tagami.
    Zwraca ID opublikowanego filmu (video_id).
    """

    youtube = authenticate_youtube()
    if not youtube:
        print("Autoryzacja YouTube API nie powiodła się.")
        return None

    # Domyślny opis
    if not description:
        description = (
            "Immerse yourself in the soothing fusion of lo-fi, ambient, and jazz in this slow and chill musical journey. "
            "This blend of smooth jazz melodies, mellow saxophone tones, and subtle lo-fi beats creates the perfect atmosphere "
            "for relaxation, focus, or late-night introspection. The gentle rhythms and calming ambiance make it ideal for studying, "
            "unwinding after a long day, or simply setting the mood for a quiet evening. With its warm, soulful textures and dreamy "
            "soundscapes, this playlist is crafted to transport you to a serene world where time slows down and your mind can find peace. "
            "Whether you're working, reading, or enjoying a moment of solitude, these tracks provide a comforting and immersive background "
            "that soothes the soul and calms the heart. Perfect for those seeking tranquility, creativity, and inspiration in every note."
        )

    # Domyślne tagi
    if not tags:
        tags = [
            "lo-fi ambient jazz",
            "slow chill vibes",
            "relaxing jazz melodies",
            "soothing ambient sounds",
            "chill beats for study",
            "nighttime jazz ambiance",
            "calming music for sleep",
            "smooth lo-fi tunes",
            "jazz-infused lo-fi",
            "mellow jazz atmosphere",
            "relaxing background music",
            "peaceful music for work",
            "slow relaxing jazz",
            "lo-fi beats with saxophone",
            "instrumental chill music",
            "ambient lo-fi grooves",
            "soulful lo-fi jazz",
            "tranquil evening music",
            "soft jazz vibes",
            "dreamy lo-fi soundscape"
        ]

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    # Dodaj zaplanowany czas publikacji, jeśli został ustawiony
    if publish_at and privacy_status == "private":
        request_body["status"]["publishAt"] = publish_at

    try:
        media_file = MediaFileUpload(video_file, chunksize=-1, resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Przesyłanie: {int(status.progress() * 100)}%")

        print("Upload zakończony. Odpowiedź serwera:")
        print(response)

        video_id = response.get("id")
        if not video_id:
            print("UWAGA: Nie udało się pobrać video_id z odpowiedzi!")
        else:
            print(f"Opublikowano wideo o ID: {video_id}")

        return video_id
    except Exception as e:
        print(f"Błąd podczas przesyłania filmu: {e}")
        return None

def set_thumbnail(video_id, thumbnail_path):
    """
    Ustawia miniaturkę (thumbnail) dla filmu o danym video_id,
    wykorzystując plik thumbnail_path.
    """
    youtube = authenticate_youtube()
    if not youtube:
        print("Autoryzacja YouTube API nie powiodła się.")
        return

    try:
        media_body = MediaFileUpload(thumbnail_path, chunksize=-1, resumable=True)

        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=media_body
        )

        response = request.execute()
        print("Miniaturka została ustawiona. Odpowiedź serwera:")
        print(response)
    except Exception as e:
        print(f"Błąd podczas ustawiania miniaturki: {e}")
