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
        logger.debug("No credentials found. Should get a new token")
        should = True
    elif not credentials.valid:
        logger.debug("Credentials found but not valid. Should get a new token")
        should = True

    return should


def get_new_token(secrets_file):

    logger.info("Fetching new token...")
    logger.debug(f"Loading secrets from file: {secrets_file}")
    flow = InstalledAppFlow.from_client_secrets_file(
        secrets_file, scopes=["https://www.googleapis.com/auth/youtube"]
    )

    logger.debug("Running local server to get credentials...")
    flow.run_local_server(port=8080, prompt="consent")

    return flow.credentials


def creds_can_be_refreshed(credentials):
    should_be_refreshed = False

    # TODO use expiry instead of expired?
    if credentials and credentials.expired and credentials.refresh_token:
        logger.debug("Token should be refreshed")
        should_be_refreshed = True

    return should_be_refreshed


def refresh_credentials(credentials):

    logger.info("Refreshing token...")
    try:
        credentials.refresh(Request())
    except RefreshError as re:
        logging.error("Refresh Error")
        credentials = None

    return credentials


def get_credentials(
    pickle_file="token.pickle",
    client_secrets_file="YtSmartPlaylist_client_secrets.json",
):

    credentials = None

    # Try loading cached credentials from pickle file
    if os.path.exists(pickle_file):
        logger.info(f"Loading credentials from file {pickle_file}...")
        with open(pickle_file, "rb") as token:
            credentials = pickle.load(token)

    # If token is expired but has a refresh token, attempt a refresh
    if creds_can_be_refreshed(credentials):
        credentials = refresh_credentials(credentials)

    # If still no valid credentials (no pickle, refresh failed, etc.), do full re-auth
    if should_get_new_token(credentials):
        credentials = get_new_token(client_secrets_file)

    # Persist valid credentials to pickle for next run
    if credentials and credentials.valid:
        logger.debug(f"Token expiration: {credentials.expiry}")
        with open(pickle_file, "wb") as token:
            logger.info("Saving credentials...")
            pickle.dump(credentials, token)

    return credentials
