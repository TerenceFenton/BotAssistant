import OpenAI_Character
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
    # Global Objects
    global history

    # Api-key & Region setup for third-party system permissions (sourced as environment variables)
    azure_talkingstick = os.getenv('AZ_TALKINGSTICK')
    azure_serviceregion = os.getenv('AZ_REGION')
    chatgpt_talkingstick = os.getenv('GPT_TALKINGSTICK')

    # Main Process
    text = azure_speech_to_text(azure_talkingstick, azure_serviceregion)
    reply, history = OpenAI_Character.chatgpt_main(text, history, chatgpt_talkingstick)
    print(reply)
    azure_text_to_speech(azure_talkingstick, azure_serviceregion, reply)


# Global Objects
mic_thread_running = False
final_text = ''
history = ''


# Main Thread
mic_input = thread.Thread(target=communicator_func)


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


# Azure Speech-to-Text:
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


# Azure Text-to-Speech 
def azure_text_to_speech(azure_talkingstick, azure_serviceregion, text):
    # Setup
    speech_config = azuresystem.SpeechConfig(subscription=azure_talkingstick, region=azure_serviceregion)
    speech_config.speech_synthesis_voice_name = "en-ZA-LukeNeural"
    synthesizer = azuresystem.SpeechSynthesizer(speech_config=speech_config)

    # Conver Text to Speech
    result = synthesizer.speak_text_async(text).get()

    # Result Error Checker
    if result.reason != result.Reason.SynthesizingAudioCompleted:
        print(f"Error: {result.reason}")
        print(f"Error details: {result.error_details}")


# Pynput & Thread Listener
def spacebar_checker(key):
    # Global Objects
    global mic_thread_running 

    # Key Checker
    if key == keyboard.Key.space:
        if mic_thread_running is False:
            # Start Thread
            mic_thread_running = True 
            mic_input.start()

        elif mic_thread_running is True:
            # End Thread
            mic_thread_running = False
            thread_resetter()
            print('Press Spacebar or esc')

    elif key == keyboard.Key.esc:
        # End Operation
        return False  


# Reset Main Thread
def thread_resetter():
    global mic_input
    mic_input = thread.Thread(target=communicator_func)


# Main
print('Press Spacebar')
with keyboard.Listener(on_press=spacebar_checker) as listener:
    listener.join()
