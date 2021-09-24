import datetime
import os
import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class IGSheet(object):
    """IGSheet class represent interface for reading/writing
    from google sheet for instgram accounts"""

    IG_SPREADSHEET_ID = os.getenv(
        "IG_SPREADSHEET_ID", "1kAIgRoBEXj192SIY0pTsBX1wt3tmthqXAe4HjRgtuT0"
    )
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, spreadsheet_name):
        # Open Credentials for Google Service
        self.spreadsheet_name = spreadsheet_name
        self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        self.service = build("sheets", "v4", credentials=self.creds)
        self.sheet_range = None
        self.valueInputOption = "RAW"

    def get_values(self, insta_spider_row_no=None):
        """Return sheet from 1 to 10K rows"""
        sheet_range = None
        if not insta_spider_row_no:
            sheet_range = f"{self.spreadsheet_name}!A1:I100000"

        if not sheet_range:
            sheet_range = (
                f"{self.spreadsheet_name}!A{insta_spider_row_no}:I{insta_spider_row_no}"
            )

        sheet = self.service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=self.IG_SPREADSHEET_ID, range=sheet_range)
            .execute()
        )
        start_range = re.search(r"\d+", result["range"]).group()
        return result.get("values", []), int(start_range)

    def mark_cell(
        self,
        index,
        value,
        direct_competitors=None,
        indirect_competitors=None,
        aggregators=None,
        external_website=None,
        external_website_status=None,
    ):
        """ mark_cell used to update the google sheet
        status field and last updated date
        """
        batch_update_values_request_body = {
            "valueInputOption": "RAW",
            "data": [
                {"range": f"{self.spreadsheet_name}!D{index}", "values": [[value]]},
                {
                    "range": f"{self.spreadsheet_name}!E{index}",
                    "values": [[datetime.date.today().__str__()]],
                },
            ],
        }
        batch_clear_values_request_body = {
            "ranges": [
                f"{self.spreadsheet_name}!F{index}",
                f"{self.spreadsheet_name}!G{index}",
                f"{self.spreadsheet_name}!H{index}",
                f"{self.spreadsheet_name}!I{index}",
                f"{self.spreadsheet_name}!G{index}",
            ],
        }

        if direct_competitors:
            batch_update_values_request_body["data"].append(
                {
                    "range": f"{self.spreadsheet_name}!F{index}",
                    "values": [[direct_competitors]],
                }
            )

        if indirect_competitors:
            batch_update_values_request_body["data"].append(
                {
                    "range": f"{self.spreadsheet_name}!H{index}",
                    "values": [[indirect_competitors]],
                }
            )

        if aggregators:
            batch_update_values_request_body["data"].append(
                {
                    "range": f"{self.spreadsheet_name}!G{index}",
                    "values": [[aggregators]],
                }
            )

        if external_website:
            batch_update_values_request_body["data"].append(
                {
                    "range": f"{self.spreadsheet_name}!I{index}",
                    "values": [[external_website]],
                }
            )

        if external_website_status:
            batch_update_values_request_body["data"].append(
                {
                    "range": f"{self.spreadsheet_name}!J{index}",
                    "values": [[external_website_status]],
                }
            )

        self.service.spreadsheets().values().batchClear(
            spreadsheetId=self.IG_SPREADSHEET_ID, body=batch_clear_values_request_body
        ).execute()
        self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.IG_SPREADSHEET_ID, body=batch_update_values_request_body
        ).execute()
