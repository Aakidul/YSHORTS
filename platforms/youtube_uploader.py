import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# --- CONFIG ---
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "/home/aaki/TRAPPIST-1E/platforms/client_secrets.json"
TOKEN_FILE = "/home/aaki/TRAPPIST-1E/platforms/token.json"

def get_authenticated_service():
    creds = None

    # Load saved credentials
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            # If the file is corrupted, delete and force reauth below
            try:
                os.remove(TOKEN_FILE)
            except OSError:
                pass
            creds = None

    # If credentials exist and are expired but have refresh token -> refresh them
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed tokens
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            print("Refreshed access token and updated token file.")
        except RefreshError:
            # Refresh failed (revoked/invalid). Delete token to force reauth.
            print("Refresh failed (token revoked/invalid). Removing token file and re-authorizing.")
            try:
                os.remove(TOKEN_FILE)
            except OSError:
                pass
            creds = None

    # If no valid creds, run local server flow to obtain them
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        # Important: request offline access; if you've already authorized before, use prompt='consent'
        # so Google issues a refresh token again.
        creds = flow.run_local_server(
            port=56789,
            open_browser=True,
            access_type="offline",   # request refresh token
            prompt="consent"         # force consent if previously authorized (to get refresh token)
        )
        # Save the credentials (access + refresh token) for future runs
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        print("Authorization complete. Credentials saved to token file.")

    return build("youtube", "v3", credentials=creds)

# --- Example upload function (unchanged logic) ---
def upload_video(video_path: str,
                 title: str,
                 description: str = "",
                 tags: list = None,
                 category_id: str = "25",
                 privacy_status: str = "public"):
    if tags is None:
        tags = []
    youtube = get_authenticated_service()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {"privacyStatus": privacy_status}
        },
        media_body=MediaFileUpload(video_path)
    )
    response = request.execute()
    print("Uploaded Video ID:", response["id"])
    return response["id"]
