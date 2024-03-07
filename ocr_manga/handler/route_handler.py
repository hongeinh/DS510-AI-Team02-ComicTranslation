import logging
import formencode as fe

from includes.utils import *
from const.message import *
from config import *
from errors import *
from artificial_intelligence.ocr_manga.handler import OCRMangaHandler
from aiohttp.web_request import Request

LOGGER = logging.getLogger(__name__)


class RouteHandler:

    def __init__(self):
        self.ocr_manga_translator = OCRMangaHandler()

    # async def translate(self, request: Request):
    def translate(self, url, lang, ocr, srclang):

        # translated_list = self.ocr_manga_translator.translate(data['url'], data['lang'], data['ocr'], data['srclang'])
        file_paths = self.ocr_manga_translator.translate(url, lang, ocr, srclang)
        return file_paths
