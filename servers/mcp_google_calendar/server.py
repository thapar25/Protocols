import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Google Calendar")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@mcp.tool()
def get_events_today() -> str:
    """
    Get today's events from the user's Google Calendar.
    
    Returns:
        str: A formatted string of today's events.
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
        """Format the datetime string to a more readable format."""
        if "T" in dt_str:
            dt = datetime.datetime.fromisoformat(dt_str)
            # Show timezone name if available, else offset
            tz = dt.tzname() if dt.tzname() else dt.strftime('%z')
            return dt.strftime("%A, %d %B %Y %I:%M %p") + f" ({tz})"
        return dt_str

    try:
        service = build("calendar", "v3", credentials=creds)

         # Call the Calendar API
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
        ist_offset = datetime.timedelta(hours=5, minutes=30)
        ist = datetime.timezone(ist_offset)
        now_ist = now_utc.astimezone(ist)
        today_ist = now_ist.date()
        end_of_day_ist = datetime.datetime.combine(
            today_ist,
            datetime.time(hour=23, minute=59, second=59, microsecond=999999, tzinfo=ist)
        )
        now_iso = now_ist.isoformat()
        end_of_day_iso = end_of_day_ist.isoformat()
        print("Getting the upcoming events for today...")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now_iso,
                timeMax=end_of_day_iso,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )


        events = events_result.get("items", [])

        if not events:
            return "No upcoming events found."

        response = []
        for event in events:
            start_time = event["start"].get("dateTime", event["start"].get("date"))
            end_time = event["end"].get("dateTime", event["end"].get("date"))
            title = event.get("summary", "Untitled Event")
            location = event.get("location", "No Location specified")
            description = event.get("description", "No Description provided")
            hangout_link = event.get("hangoutLink", "No meeting link provided")
            start = format_dt(start_time)
            end = format_dt(end_time)
            response.append(f"Event: {title}\nDescription: {description}\nStart: {start}\nEnd: {end}\nLocation: {location}\nMeeting Link: {hangout_link}\n")
        return "\n".join(response)

    except HttpError as error:
        return(f"An error occurred: {error}")    
    
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')