from googletrans import Translator


async def translate(text,src,dest):
    try: 
        translator = Translator()
        translate_text = translator.translate(text, dest=dest, src=src)
        return translate_text.text
    except:
        return 'data not found'
