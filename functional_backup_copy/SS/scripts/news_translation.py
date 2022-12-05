from googletrans import Translator, constants

def get_translation(pt_text):
    # init the Google API translator
    translator = Translator()   
    # translate a spanish text to english text (by default)
    translation = (translator.translate(pt_text)).text
    return translation