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

input_text = input('What would you like me to say?: ')

audio = client.generate(
    text=input_text,
    voice=aivoice
)

play(audio)

