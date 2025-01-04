import TTS_Segment
import OpenAI_Codsworth
import azure.cognitiveservices.speech as azuresystem
from azure.cognitiveservices.speech import AudioConfig
import time
from pynput import keyboard
import thread
import os


# Api-key & Region setup for third-party system permissions (sourced as environment variables)
azure_talkingstick = os.getenv('AZ_TALKINGSTICK')
azure_serviceregion = os.getenv('AZ_REGION')
elevenlabs_talkingstick = os.getenv('EL_TALKINGSTICK')
chatgpt_talkingstick = os.getenv('GPT_TALKINGSTICK')


# Audio Input & AI Output Main
def communicator_func():

    # Api-key & Region setup for third-party system permissions (sourced as environment variables)
    azure_talkingstick = os.getenv('AZ_TALKINGSTICK')
    azure_serviceregion = os.getenv('AZ_REGION')
    elevenlabs_talkingstick = os.getenv('EL_TALKINGSTICK')
    chatgpt_talkingstick = os.getenv('GPT_TALKINGSTICK')

    # Main Process
    text = azure_speech_to_text(azure_talkingstick, azure_serviceregion)
    reply = OpenAI_Codsworth.chatgpt_main(text, chatgpt_talkingstick)
    print(reply)
    TTS_Segment.text_input_speech_output(reply, elevenlabs_talkingstick)


# Global Objects
mic_thread_running = False
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

# Main Azure function:
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
        while mic_thread_running is True:
            time.sleep(1)
    finally:
        recognizer.stop_continuous_recognition()
        print('Generating...')
        return final_text


# Pynput & Thread Listener
def spacebar_checker(key):
    global mic_thread_running  
    if key == keyboard.Key.space:
        if mic_thread_running is False:
            mic_thread_running = True 
            mic_input.start() 
        else:
            mic_thread_running = False
            mic_input.join() 
            return False  

mic_input = thread.Thread(target=communicator_func)

print('Press Spacebar')
with keyboard.Listener(on_press=spacebar_checker) as listener:
    listener.join()
