import datetime
import os.path
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def setup():
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
	login = input("Do you wish to login again? y/n (default: n)\n")
	no = "n" in login or "N" in login
	yes = "y" in login or "Y" in login
	if no and yes:
		print("write y/n, not both")
		sys.exit()
	stay_signed_in = input("Would you like to stay signed in? y/n (default: y)")
	if ("y" in stay_signed_in or "Y" in stay_signed_in) and ("n" in stay_signed_in or "N" in stay_signed_in):
		print("write y/n, not both")
		sys.exit()

	if yes and os.path.exists("token.json"):
		os.remove("token.json")
	stay_signed_in = not ("n" in stay_signed_in or "N" in stay_signed_in)


	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
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
		if stay_signed_in:
			with open("token.json", "w") as token:
				token.write(creds.to_json())

	try:
		service = build("calendar", "v3", credentials=creds)
		return service

	except HttpError as error:
		print(f"An error occurred: {error}")




service = setup()

# Call the Calendar API
now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
print("Getting the upcoming 10 events")
events_result = (
    service.events()
    .list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime",
    )
    .execute()
)
events = events_result.get("items", [])

if not events:
	print("No upcoming events found.")
	sys.exit()

# Prints the start and name of the next 10 events
for event in events:
	start = event["start"].get("dateTime", event["start"].get("date"))
	print(start, event["summary"])
