import logging
import os
import sys
import wave
from pathlib import Path
from typing import Optional

from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel

from resources.res_manager import ResourcesManager
from src.name_generator import GenerateName

SUPPORTED_EXTENSIONS = (".mp3", ".mp4", ".wav")


class SubtitlesGenerator:
    @classmethod
    def create_subtitles(cls, path_to_file) -> Optional[str]:
        """
        Creates subtitles to given file,
        if file extension is not in SUPPORTED_EXTENSIONS
        :param path_to_file: path to file to which subtitles should be generated
        :return: path to subtitles with txt extension or None in case of failure
        """
        if not path_to_file.endswith(SUPPORTED_EXTENSIONS):
            logging.error("File extension not supported.")
            return None

        SubtitlesGenerator._enable_logs(True)
        new_path = SubtitlesGenerator._convert_to_mono_wav(path_to_file, ResourcesManager.get_resource('tmp'))
        if new_path is None:
            return None
        result = SubtitlesGenerator._generate_subtitles(new_path)
        SubtitlesGenerator._remove_tmp_file(new_path)
        # return SubtitlesGenerator.write_to_txt(result, "../../res/subtitles", path_to_file)
        return SubtitlesGenerator.write_to_txt(result, ResourcesManager.get_resource('subtitles'), path_to_file)

    @classmethod
    def _convert_sound_to_mono(cls, sound, out_path) -> bool:
        if sound is None:
            logging.error("Sound can't be None")
            return False
        converted_wav = sound.set_channels(1)
        file = converted_wav.export(out_path, format="wav")
        file.close()
        return True

    @classmethod
    def _remove_tmp_file(cls, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            logging.debug("File does not exist: " + file_path)

    @classmethod
    def _enable_logs(cls, vosk_logs):
        if vosk_logs:
            SetLogLevel(0)  # Vosk logs
        logging.basicConfig(level=logging.DEBUG)

    @classmethod
    def _convert_to_mono_wav(cls, file_path, out_path) -> Optional[str]:
        # check if file exists.
        try:
            with open(file_path, "r"):
                pass
        except IOError:
            logging.error("File not found: " + file_path)
            return None

        # create out directory if does not exists
        Path(out_path).mkdir(parents=True, exist_ok=True)

        created_file_path = GenerateName.generate_name(".wav", out_path + "/",
                                                       GenerateName.extract_filename_from_path(file_path) + "-tmp-")

        sound = AudioSegment.from_file(file_path)
        SubtitlesGenerator._convert_sound_to_mono(sound, created_file_path)
        return created_file_path

    @classmethod
    def _generate_subtitles(cls, path_to_wav):
        if path_to_wav is None:
            logging.error("Path to wav is None!")
            exit(1)
        if not os.path.exists(ResourcesManager.get_resource('model')):
            logging.error(
                "Please download the model from https://alphacephei.com/vosk/models and unpack as "
                "'model' in the resources folder.")
            exit(1)

        wf = wave.open(path_to_wav, "rb")

        model = Model(ResourcesManager.get_resource('model'))
        rec = KaldiRecognizer(model, wf.getframerate())
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)
        return rec.FinalResult()

    @classmethod
    def write_to_txt(cls, result, out_path, path_to_file):
        Path(out_path).mkdir(parents=True, exist_ok=True)
        input_file_name = GenerateName.extract_filename_from_path(path_to_file)
        new_path = GenerateName.generate_name(".txt", out_path, f"/{input_file_name}-sub-")
        with open(new_path, "w") as file:
            file.write(result)
        return new_path


if __name__ == '__main__':
    string = sys.argv[1].replace("\\", "/")
    SubtitlesGenerator.create_subtitles(string)
