import logging

from textblob import TextBlob
from textblob.exceptions import NotTranslated


class Translator:

    def __init__(self, to_lang, from_lang='en', _max_request_len=4500):
        """
        Uses Google Translations API with following restrictions:
            500 requests per minute
            5000 characters per request

        :param to_lang: required language
        :param from_lang: source language. Currently only English is supported due to ML limitations.
        :param _max_request_len: maximum length of a request (depends on api)
        """
        self.to_lang = to_lang
        self.MAX_REQUEST_LEN = _max_request_len

    def translate_dict(self, list_of_dicts, key):
        """
        Deprecated, translates without taking care of google limits
        :param list_of_dicts:
        :param key:
        :return:
        """
        for entry in list_of_dicts:
            entry[f"{key}_{self.to_lang}"] = self._translate_text(entry[key])
        return list_of_dicts

    def _translate_text(self, text):
        blob = TextBlob(text)
        translated = text
        try:
            translated = blob.translate(to=self.to_lang)
        except NotTranslated:
            logging.debug("There is a word the same as input " + text)
        return str(translated)

    def translate_sentences_dict(self, sentences_dict_list, split_symbol="\n"):
        """
        Adds translated sentences to sentences_dict_list
        :param sentences_dict_list:
        :param split_symbol:
        :return:  translated sentences dictionary
        """
        requests = []

        for entry in sentences_dict_list:
            if len(requests) == 0 or len(entry) + len(requests[-1]) > self.MAX_REQUEST_LEN:
                requests.append(entry['sentence'])
            else:
                requests[-1] += split_symbol + entry['sentence']

        respond = []
        for req in requests:
            respond.append(self._translate_text(req))

        index = 0
        for resp in respond:
            resp = resp.split(split_symbol)

            for sentence in resp:
                sentences_dict_list[index][f"sentence_{self.to_lang}"] = sentence
                index += 1
        return sentences_dict_list
