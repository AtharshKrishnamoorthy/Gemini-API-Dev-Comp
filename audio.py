import speech_recognition as sr
import pygame
import time
import logging

def record_audio(file_path, timeout=5, phrase_time_limit=30, retries=3):
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info("Recording started")
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete")
                with open(file_path, "wb") as audio_file:
                    audio_file.write(audio_data.get_wav_data())
                return
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            break
    else:
        logging.error("Recording failed after all retries")

def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        pygame.mixer.init()
    except pygame.error as e:
        logging.error(f"Failed to play audio : {e}")
    except Exception as e:
        logging.error(f"An Unexexted error occured while playing audio : {e}")
