import random
import re
from typing import Optional

from random_user_agent.params import OperatingSystem, SoftwareName
from random_user_agent.user_agent import UserAgent


def replace_newlines(text: str):
    return re.sub(r"(?<!\\)\n", r"\\n", text)


def get_random_user_agent(seed: Optional[int] = None) -> str:
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100
    )

    if seed is not None:
        random.seed(seed)

    return random.choice(user_agent_rotator.get_user_agents())["user_agent"]
