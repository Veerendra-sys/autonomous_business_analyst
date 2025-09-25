# researcher/utils.py
import urllib.robotparser
from urllib.parse import urlparse
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def is_allowed_by_robots(url, user_agent="*"):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        logger.warning("Couldn't read robots.txt for %s", parsed.netloc)
        return True  # conservative: allow if robots inaccessible

def polite_wait(seconds=1.0):
    time.sleep(seconds)

