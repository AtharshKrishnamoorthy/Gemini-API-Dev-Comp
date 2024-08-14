from deepgram import (DeepgramClient,
                       SpeakOptions)
import logging


def text_to_speech(model, api_key, text, output_file_path):


    """
    Convert text to speech using the specified model.

    Args:
    model (str): The model to use for TTS.
    api_key (str): The API key for the TTS service.
    text (str): The text to convert to speech.
    output_file_path (str): The path to save the generated speech audio file.
    local_model_path (str): The path to the local model (if applicable).
    """
    
    SPEAK_OPTIONS = {"text" : text}
    if model=='deepgram':
          # STEP 1: Create a Deepgram client using the API key from environment variables
          deepgram = DeepgramClient(api_key=api_key)

          # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
          options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
          )

          # STEP 3: Call the save method on the speak property
          response = deepgram.speak.v("1").save(output_file_path, SPEAK_OPTIONS, options)
          print(response.to_json(indent=4))

    else:
        raise ValueError("Unsupported TTS model")

