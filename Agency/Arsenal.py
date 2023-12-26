# /Agency/Arsenal.py

from Tools.FileManagement.ReadFile import ReadFile
from Tools.FileManagement.CreateFile import CreateFile
from Tools.FileManagement.MoveFile import MoveFile
from Tools.FileManagement.GetDirectoryContents import GetDirectoryContents
from Tools.Programming.DownloadFile import DownloadFile
from Tools.Programming.ExecutePyFile import ExecutePyFile
from Tools.Organizational.Plan import Plan
from Tools.Organizational.Delegate import Delegate
from Tools.Organizational.Inquire import Inquire
from Tools.RecipeScraper.RecipeScraper import RecipeScraper

ORGANIZATIONAL = [Plan, Delegate, Inquire]
FILE_MANAGEMENT = [ReadFile, CreateFile, MoveFile, GetDirectoryContents]
PROGRAMMING = [ExecutePyFile, DownloadFile]

SHARED_TOOLS = PROGRAMMING + ORGANIZATIONAL + FILE_MANAGEMENT
CUSTOM_TOOLS = [RecipeScraper]

ARSENAL = SHARED_TOOLS + CUSTOM_TOOLS