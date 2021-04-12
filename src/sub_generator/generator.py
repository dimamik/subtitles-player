#!/usr/bin/env python3

import logging
import os
import sys
import wave
from datetime import datetime
from pathlib import Path

from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel


def convert_sound_to_mono(sound, out_path) -> bool:
    if sound is None:
        logging.error("Sound can't be None")
        return False
    converted_wav = sound.set_channels(1)
    file = converted_wav.export(out_path, format="wav")
    file.close()
    return True


def remove_tmp_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        logging.debug("File does not exist: " + file_path)


def enable_logs(vosk_logs):
    if vosk_logs:
        SetLogLevel(0)  # Vosk logs
    logging.basicConfig(level=logging.DEBUG)


def convert_to_mono_wav(file_path, out_path):
    """
    Takes any supported format and converts it to mono wav
    :param file_path: Path to converted file.
    :param out_path: Path to out directory
    :return: Returns information whether file was converted.
    """

    ext = (".mp3", ".mp4", ".wav")
    if not file_path.endswith(ext):
        logging.error("File extension not supported.")
        return None

    # check if file exists.
    try:
        with open(file_path, "r"):
            pass
    except IOError:
        logging.error("File not found: " + file_path)
        return None

    # create out directory if does not exists
    Path(out_path).mkdir(parents=True, exist_ok=True)

    created_file_path = out_path + "/" + subtract_filename(file_path) + "-tmp-" + str(datetime.now()).replace(
        ":", "-") + ".wav"

    sound = AudioSegment.from_file(file_path)
    convert_sound_to_mono(sound, created_file_path)
    return created_file_path


def generate_subtitles(path_to_wav):
    if path_to_wav is None:
        logging.error("Path to wav is None!")
        exit(1)
    # TODO Download model if not exists
    if not os.path.exists("../../model"):
        print(
            "Please download the model from https://alphacephei.com/vosk/models and unpack as "
            "'model' in the current folder.")
        exit(1)

    wf = wave.open(path_to_wav, "rb")

    model = Model("../../model")
    rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
    return rec.FinalResult()


def write_to_txt(result, out_path, input_file_name):
    Path(out_path).mkdir(parents=True, exist_ok=True)
    new_path = out_path + f"/{input_file_name}-sub-" + str(datetime.now()).replace(":", "-") + ".txt"
    with open(new_path, "w") as file:
        file.write(result)
    return new_path


def subtract_filename(string):
    return string.split("/")[-1].split(".")[0]


def create_subtitles(path_to_file):
    enable_logs(True)
    new_path = convert_to_mono_wav(path_to_file, "../../res/tmp")
    if new_path is None:
        return None
    result = generate_subtitles(new_path)
    remove_tmp_file(new_path)
    return write_to_txt(result, "../../res/subtitles", subtract_filename(path_to_file))


if __name__ == '__main__':
    create_subtitles(sys.argv[1])
