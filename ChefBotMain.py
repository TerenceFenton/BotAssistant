import TTS_Segment
import STT_Segment
import OpenAI_Codsworth
import os
from pynput import keyboard
import threading


# Api-key & Region setup for third-party system permissions (sourced as environment variables)
azure_talkingstick = os.getenv('AZ_TALKINGSTICK')
azure_serviceregion = os.getenv('AZ_REGION')
elevenlabs_talkingstick = os.getenv('EL_TALKINGSTICK')
chatgpt_talkingstick = os.getenv('GPT_TALKINGSTICK')


# Global Objects
mic_thread_running = False


# Audio Input & AI Output Main
def communicator_func(azure_talkingstick, azure_serviceregion, chatgpt_talkingstick, elevenlabs_talkingstick):
    text = STT_Segment.azure_speech_to_text(azure_talkingstick, azure_serviceregion)
    reply = OpenAI_Codsworth.chatgpt_main(text, chatgpt_talkingstick)
    print(reply)
    TTS_Segment.text_input_speech_output(reply, elevenlabs_talkingstick)


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


mic_input = threading.Thread(target=communicator_func)


print('Press Spacebar')
with keyboard.Listener(on_press=spacebar_checker) as listener:
    listener.join()
 