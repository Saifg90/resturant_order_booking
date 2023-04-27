class Twillo:
    openai_resp = 'None'

    @classmethod
    def set_openai_resp(cls,text_data):
        cls.openai_resp = text_data
        return cls.openai_resp