import json
import logging
import os.path
import statistics


class ParseSubtitlesJson:
    def __init__(self, path_to_json, lazy_mode=False, pause_factor=3, interval_decrement=0.1):
        """
        Class takes path to generated by ml json file (.txt) and
        creates dictionary of word chunks (based on pauses between words)
        :return: {
            "end": None,
            "start": start,
            "sentence": "Some example sentence"
        }
        :param path_to_json: path to subtitles file
        :param lazy_mode: determines whether subtitles should be generated during initialization
        :param pause_factor: Pause detection parameter. The greater the value the longer interval has
            to be to be classified as pause.
        :param interval_decrement: Pause detection parameter. Increases the pause detection chance with every next
            word in sentence to prevent too long sentences. The sentence cannot be longer than 1 / interval_decrement.

        """
        self.lazy_mode = lazy_mode
        self._words_dict = []
        self._sentences_dict = []
        self.path_to_json = path_to_json
        self.pause_factor = pause_factor
        self.interval_decrement = interval_decrement
        if not lazy_mode:
            self._initialize_table(path_to_json)
            self.get_sentences()

    def word_dict(self):
        if not self._words_dict:
            self._initialize_table(self.path_to_json)
        return self._words_dict

    def _initialize_table(self, path_to_json, path_to_json_result='result'):
        """
        Generates dict from json file representing subtitles
        :param path_to_json:
        :param path_to_json_result: name of filed in json representing words to translate
        :return:
        """
        if not os.path.isfile(path_to_json):
            logging.error("File to json in prep translation does not exist: " + path_to_json)
            exit(-1)
        with open(path_to_json) as json_file:
            data = json.load(json_file)
            print("Type:", type(data))
            self._words_dict = data[path_to_json_result]

    @property
    def sentences_dict(self):
        if not self._sentences_dict:
            self.get_sentences()
        else:
            return self._sentences_dict

    def get_sentences(self):
        def create_start_dict(start):
            return {
                "end": None,
                "start": start,
                "sentence": ""
            }

        intervals = []
        for entry in self._words_dict:
            intervals.append(entry['end'] - entry['start'])

        std = statistics.stdev(intervals)
        mean = statistics.mean(intervals)
        pause = mean + std * self.pause_factor
        logging.debug("Mean of intervals in seconds: " + str(mean))
        logging.debug("Pause time in seconds" + str(pause))
        sentences = [create_start_dict(self._words_dict[0]['start'])]

        word_counter = 0
        for i, entry in enumerate(self._words_dict):
            if i == len(self._words_dict) - 1:
                sentences[-1]['end'] = entry['end']
                sentences[-1]['sentence'] += f" {entry['word']}"
            else:
                logging.debug(str(self._words_dict[i + 1]['start'] - entry['end']) + ">?? " + str(
                    pause * (1 - self.interval_decrement * word_counter)) + "\n And words: ")
                if (self._words_dict[i + 1]['start'] - entry['end'] >
                        pause * (1 - self.interval_decrement * word_counter)):
                    sentences[-1]['sentence'] += f" {entry['word']}"
                    sentences[-1]['end'] = entry['end']
                    sentences.append(create_start_dict(self._words_dict[i + 1]['start']))
                    word_counter = 0
                else:
                    sentences[-1]['sentence'] += f" {entry['word']}"
                    word_counter += 1
        self._sentences_dict = sentences
        return sentences

    def __str__(self):
        string_to_ret = ""
        for i, entry in enumerate(self._sentences_dict):
            string_to_ret += f"{i} : {format(round(entry['start'], 2), '.2f')} | " \
                             f"{format(round(entry['end'], 2), '.2f')} : {entry['sentence']} \n"
        return string_to_ret


if __name__ == '__main__':
    parseClass = ParseSubtitlesJson("../../resources/subtitles/small_record-sub-2021-05-10-21-47-41.txt")
    print(parseClass)
