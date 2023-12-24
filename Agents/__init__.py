# Agents/__init__.py

from .UserAgent import UserAgent
from .CoderAgent import CoderAgent
from .QaAgent import QaAgent
from .CulinaryAgent import CulinaryAgent
from .SprAgent import SprAgent

agent_classes = {
    "UserAgent": UserAgent,
    "CoderAgent": CoderAgent,
    "QaAgent": QaAgent,
    "CulinaryAgent": CulinaryAgent,
    "SprAgent": SprAgent
}