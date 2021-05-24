from src.translation.prep_translation import ParseSubtitlesJson
from src.translation.translation import Translator


class SubtitlesVM:
    def __init__(self, subtitles_view):
        """
        Works on initialized Subtitles View and run_parse_and_translate
        needs to be run in new thread
        :param subtitles_view: previously generated view
        """
        self.subtitles_view = subtitles_view

    def run_parse_and_translate(self):
        self.subtitles_view.parseClass = ParseSubtitlesJson(self.subtitles_view.subs_path)
        self.subtitles_view.translator = Translator(self.subtitles_view.to_lang)
        self.subtitles_view.dictionary = self.subtitles_view.parseClass.sentences_dict
        self.subtitles_view.dictionary = self.subtitles_view.translator.translate_sentences_dict(
            self.subtitles_view.dictionary)
