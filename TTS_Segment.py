# Libraries
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play
import os

talking_stick = os.getenv('TALKINGSTICK')

client = ElevenLabs(api_key=talking_stick)

aivoice = Voice(
    voice_id='tTZ0TVc9Q1bbWngiduLK', 
    settings=VoiceSettings(
        stability=0.43, 
        similarity_boost=0.25, 
        style=0, 
        use_speaker_boost=True
    )
)

def Text_input_Speech_output(input_text):
    global client
    global aivoice
    audio = client.generate(
    text=input_text,
    voice=aivoice
    )
    play(audio)

