from datetime import datetime
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from threading import Event
from threading import Thread
from time import sleep
from twitter import Twitter
import logging

# The duration of the smallest backoff step in seconds.
BACKOFF_STEP_S = 0.1

# The maximum number of retry steps, equivalent to 0.1 * (2^12 - 1) = 409.5
# seconds of total delay. This is the largest interval that one backoff
# sequence may take.
MAX_TRIES = 12

# The time in seconds after which to reset a backoff sequence. This is the
# smallest interval at which backoff sequences may repeat normally.
BACKOFF_RESET_S = 30 * 60

class Main:
    """A wrapper for the main application logic and retry loop."""

    def __init__(self):
        try:
                # self.twitter = Twitter()
            self.twitter = Twitter.for_local_streaming()
        except Exception as e:
            logging.error(f"Failed to initialize Twitter API: {e}")
            raise

    def twitter_callback(self, tweet):
        """Analyzes posts and tweets about it."""
        pass

    def run_session(self):
        """Runs a single streaming session. Logs and cleans up after
        exceptions.
        """

        logging.info('Starting new streaming session.')
        try:
            # self.twitter.stream_mentions()
            self.twitter.stream_mentions_local()
            logging.info('Streaming session started successfully, now stop the session.')
            self.twitter.strop_stream()
        except Exception as e:
            logging.error(f"Error in streaming session: {e}")
            self.twitter.strop_stream()
            logging.exception("Exception details:")

    def backoff(self, tries):
        """Sleeps an exponential number of seconds based on the number of
        tries.
        """

        delay = BACKOFF_STEP_S * pow(2, tries)
        logging.warning('Waiting for %.1f seconds.' % delay)
        sleep(delay)

    def run(self):
        """Runs the main retry loop with exponential backoff."""

        tries = 0
        while tries < 1:
            try:
                # The session blocks until an error occurs.
                self.run_session()
            except Exception as e:
                logging.error(f"Unexpected error in main loop: {e}")
                logging.exception("Exception details:")

            # Remember the first time a backoff sequence starts.
            now = datetime.now()
            if tries == 0:
                logging.debug('Starting first backoff sequence.')
                backoff_start = now

            # Reset the backoff sequence if the last error was long ago.
            if (now - backoff_start).total_seconds() > BACKOFF_RESET_S:
                logging.debug('Starting new backoff sequence.')
                tries = 0
                backoff_start = now

            # Give up after the maximum number of tries.
            if tries >= MAX_TRIES:
                logging.warning('Exceeded maximum retry count.')
                break

            # Wait according to the progression of the backoff sequence.
            self.backoff(tries)

            # Increment the number of tries for the next error.
            tries += 1


if __name__ == '__main__':
    try:
        Main().run()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.exception("Exception details:")
    finally:
        logging.info("Application has stopped.")