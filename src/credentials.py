import os
import pickle
import logging

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError

logger = logging.getLogger(__name__)


def should_get_new_token(credentials):
    should = False

    if not credentials:
        should = True
    elif not credentials.valid:
        should = True

    return should


def get_new_token(secrets_file):

    logging.info("Fetching new token...")
    flow = InstalledAppFlow.from_client_secrets_file(
        secrets_file, scopes=["https://www.googleapis.com/auth/youtube"]
    )

    flow.run_local_server(port=8080, prompt="consent")

    return flow.credentials


def creds_can_be_refreshed(credentials):
    should_be_refreshed = False

    # TODO the refresh token may not work because it is too old
    # TODO use expiry instead of expired?

    if credentials.expired and credentials.refresh_token:
        should_be_refreshed = True

    return should_be_refreshed


def refresh_credentials(credentials):

    return credentials


def get_credentials(
    pickle_file="token.pickle",
    client_secrets_file="YtSmartPlaylist_client_secrets.json",
):

    credentials = None

    if os.path.exists(pickle_file):
        logger.info("Loading credentials from file...")
        with open(pickle_file, "rb") as token:
            credentials = pickle.load(token)

    if should_get_new_token(credentials):

        # Refresh or get new token
        if should_get_new_token(credentials):
            if creds_can_be_refreshed(credentials):
                logger.info("Refreshing token...")
                try:
                    credentials.refresh(Request())
                except RefreshError as re:
                    logging.error("Refresh Error")
            else:
                credentials = get_new_token(client_secrets_file)

        if credentials and credentials.valid:
            logger.debug(f"Token expiration: {credentials.expiry}")
            logger.info("Saving new token...")
            with open(pickle_file, "wb") as token:
                logger.info("Saving credentials...")
                pickle.dump(credentials, token)

    return credentials
