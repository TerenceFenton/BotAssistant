# Libraries
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play

def text_input_speech_output(input_text, elevenlabs_talkingstick):
    # API-Key insert
    client = ElevenLabs(api_key=elevenlabs_talkingstick)
    # Voice Customisation
    aivoice = Voice(
        voice_id='GBv7mTt0atIp3Br8iCZE', 
        settings=VoiceSettings(
            stability=0.70, 
            similarity_boost=0.25, 
            style=0, 
            use_speaker_boost=True
        )
    )
    # Audio Generation
    audio = client.generate(
    text=input_text,
    voice=aivoice
    )
    play(audio)

