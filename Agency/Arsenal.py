# /Agency/Arsenal.py

from Tools.ReadFile import ReadFile
from Tools.CreateFile import CreateFile
from Tools.DownloadFile import DownloadFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Tools.GetDirectoryContents import GetDirectoryContents
from Tools.Plan import Plan
from Tools.Delegate import Delegate
from Tools.Inquire import Inquire
from Tools.RecipeScraper.RecipeScraper import RecipeScraper

INTERNAL_TOOLS = [Plan, Delegate, Inquire, RecipeScraper]
ARSENAL = [
    ReadFile,
    CreateFile,
    DownloadFile,
    MoveFile,
    ExecutePyFile,
    GetDirectoryContents,
] + INTERNAL_TOOLS