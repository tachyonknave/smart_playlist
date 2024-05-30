import os
import pickle
import logging

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError


def get_credentials(pickle_file='token.pickle', client_secrets_file='YtSmartPlaylist_client_secrets.json'):
    credentials = None

    if os.path.exists(pickle_file):
        logging.info("Loading credentials from file...")
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)

    if credentials:
        logging.debug(f"Token expiration: {credentials.expiry}")

    # token expires after 1 hour

    if not credentials or not credentials.valid:
        fetch_new_token = False
        if credentials and credentials.expired and credentials.refresh_token:
            logging.info("Refreshing token...")
            # TODO the refresh token may not work because it is too old
            try:
                credentials.refresh(Request())
            except RefreshError as re:
                logging.error("Refresh Error")
                fetch_new_token = True

        if fetch_new_token:
            logging.info("Fetching new token...")
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file,
                scopes=['https://www.googleapis.com/auth/youtube']
            )

            flow.run_local_server(port=8080, prompt='consent')

            credentials = flow.credentials

        with open(pickle_file, 'wb') as token:
            logging.info("Saving credentials...")
            pickle.dump(credentials, token)

    return credentials
