import datetime
import time
from functools import wraps
from typing import Callable

from pythontextnow import Client
from pythontextnow.util.ConfigReader import ConfigReader
from pythontextnow.util.CustomLogger import CustomLogger


def enforce_cooldown(function: Callable) -> Callable:
    """
    This will enforce a scaling cooldown on the method it wraps.
    Currently, this is set up to work for API call methods only.
    If in the future this function needs to be used for non-API methods, some refactoring can be done.
    """

    @wraps(function)
    def wrapFunction(*args, **kwargs):
        cooldown_seconds = ConfigReader.get("api", "api_call_cooldown_seconds", as_type=float)
        client_config = Client.get_client_config()
        now = datetime.datetime.now()
        difference_seconds = (now - client_config.last_call_time).total_seconds()
        if difference_seconds < cooldown_seconds:
            # enforce cooldown
            CustomLogger.getLogger().warning(
                f"ENFORCING COOLDOWN FOR {cooldown_seconds} SECONDS..."
            )
            time.sleep(cooldown_seconds)
        Client.update(last_call_time=now)
        return function(*args, **kwargs)

    return wrapFunction
