import logging
import os
import shutil
import time
import uuid

import ffmpeg
import whisper

from util import delete_file

LANGUAGE = os.getenv("LANGUAGE", "en")
MODEL_NAME = os.getenv("WHISPER_MODEL", "base")
model = None



async def transcribe(audio):
    start_time = time.time()
    initial_filepath = f"/tmp/{uuid.uuid4()}{audio.filename}"

    with open(initial_filepath, "wb+") as file_object:
        shutil.copyfileobj(audio.file, file_object)

    converted_filepath = f"/tmp/ffmpeg-{uuid.uuid4()}{audio.filename}"

    logging.debug("running through ffmpeg")
    (
        ffmpeg
        .input(initial_filepath)
        .output(converted_filepath, loglevel="error")
        .run()
    )
    logging.debug("ffmpeg done")

    delete_file(initial_filepath)

                 global model
        if model is None:
            logging.debug("loading whisper model %s", MODEL_NAME)
            model = whisper.load_model(MODEL_NAME)
        logging.debug("transcribing audio with local whisper")
        result = model.transcribe(converted_filepath, language=LANGUAGE)
        transcription = result["text"]
        logging.info("STT response received from local whisper in %s seconds", time.time() - start_time)
        logging.info('user prompt: %s', transcription)
        delete_file(converted_filepath)
        return transcriptionion
