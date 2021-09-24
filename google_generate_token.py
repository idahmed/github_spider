""" This script is designed to assist in obtaining authentication token for google services
"""
from __future__ import print_function

import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
# Note
IG_SPREADSHEET_ID = os.getenv(
    "IG_SPREADSHEET_ID", "1kAIgRoBEXj192SIY0pTsBX1wt3tmthqXAe4HjRgtuT0"
)
IG_SPREADSHEET_SHEET = "SOURCE"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(
                host="localhost",
                port=8088,
                authorization_prompt_message="Please visit this URL: {url}",
                success_message="The auth flow is complete; you may close this window.",
                open_browser=True,
            )
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


if __name__ == "__main__":
    main()
