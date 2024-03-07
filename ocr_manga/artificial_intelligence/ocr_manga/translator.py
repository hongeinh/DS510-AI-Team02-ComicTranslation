# from google_trans_new import google_translator  
# translator = google_translator()
from google.cloud import translate_v2 as translate
credentials_path = "/home/hongeinh/Documents/School/CityU/Winter 2024/DS510/TP/DS510-AI-Team02-ComicTranslation/ocr_manga/Credentials/vision_key.json"
translator = translate.Client.from_service_account_json(credentials_path)
import os
import cv2

# TODO: add semantic translation
# After each dialogue, summarize it with the above summarized dialogue
class Translator:

    def translateText(self, fileName, textListDict, langCode):
        textList=textListDict[fileName]
        print("textList", textList)
        textList_trans=[]
        for text in textList:
            # use translator lib to translate the text
            # text_trans = translator.translate(text, lang_tgt=langCode,) if len(text)!=0 else "" 
            if len(text) != 0:

                result = translator.translate(text, target_language=langCode,) 
                textList_trans.append(result.get("translatedText"))
            # store it into the text list to draw back again to the inpained img
            else: textList_trans += [""]
        return textList_trans