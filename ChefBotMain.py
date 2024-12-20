import TTS_Segment
import STT_Segment
import OpenAI_Codsworth
import os


# Api-key & Region setup for third-party system permissions (sourced as environment variables)
azure_talkingstick = os.getenv('AZ_TALKINGSTICK')
azure_serviceregion = os.getenv('AZ_REGION')
elevenlabs_talkingstick = os.getenv('EL_TALKINGSTICK')
chatgpt_talkingstick = os.getenv('GPT_TALKINGSTICK')


# Test code to see if all moving parts are functional
input('Press enter: ')
text = STT_Segment.azure_speech_to_text(azure_talkingstick, azure_serviceregion)

reply = OpenAI_Codsworth.chatgpt_main(text, chatgpt_talkingstick)
print(reply)
TTS_Segment.text_input_speech_output(reply, elevenlabs_talkingstick)


