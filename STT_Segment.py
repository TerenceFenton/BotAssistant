# Libraries
import azure.cognitiveservices.speech as azuresystem
from azure.cognitiveservices.speech import AudioConfig
import time

# Response text
final_text = ''

# Recognizer Events
def recognized_handler(event_args):
    global final_text
    print(f'Recognized: {event_args.result.text}')
    final_text = event_args.result.text

def recognizing_handler(event_args):
    global final_text
    print(f'Recognizing: {event_args.result.text}')

def cancelation_handler(event_args):
    print(f'Canceled: {event_args.reason}')
    if event_args.reason == azuresystem.CancellationReason.Error:
        print(f"Error: {event_args.error_details}")

# Main function:
def azure_speech_to_text(azure_talkingstick, azure_serviceregion):
    # Setup
    global final_text
    audio_config = AudioConfig(use_default_microphone=True)
    speech_config = azuresystem.SpeechConfig(subscription=azure_talkingstick, region=azure_serviceregion)
    speech_config.speech_recognition_language = 'en-US'
    recognizer = azuresystem.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Attach Recognition Events
    recognizer.recognized.connect(recognized_handler)
    recognizer.recognizing.connect(recognizing_handler)
    recognizer.canceled.connect(cancelation_handler)
      
    # Process  
    global mic_thread_running
    print('Listening...')
    recognizer.start_continuous_recognition()   
    try:
        time.sleep(5)
    finally:
        recognizer.stop_continuous_recognition()
        print('Generating...')
        return final_text


