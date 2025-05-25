import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the upcoming events on current date, on the user's calendar.
  """
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  def format_dt(dt_str):
    if "T" in dt_str:
        dt = datetime.datetime.fromisoformat(dt_str)
        # Show timezone name if available, else offset
        tz = dt.tzname() if dt.tzname() else dt.strftime('%z')
        return dt.strftime("%A, %d %B %Y %I:%M %p") + f" ({tz})"
    return dt_str

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    end_of_day = datetime.datetime.now(tz=datetime.timezone.utc).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()
    print("Getting the upcoming events for today...")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    for event in events:
      start_time = event["start"].get("dateTime", event["start"].get("date"))
      end_time = event["end"].get("dateTime", event["end"].get("date"))
      title = event.get("summary", "Untitled Event")
      location = event.get("location", "No Location specified")

      start = format_dt(start_time)
      end = format_dt(end_time)
      
      print(f"Event: {title}\nStart: {start}\nEnd: {end}\nLocation: {location}\n")


  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()