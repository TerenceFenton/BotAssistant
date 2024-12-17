import TTS_Segment
import STT_Segment
import os


# Api-key & Region setup for third-party system permissions (sourced as environment variables)
azure_talkingstick = os.getenv('AZ_TALKINGSTICK')
azure_serviceregion = os.getenv('AZ_REGION')
elevenlabs_talkingstick = os.getenv('EL_TALKINGSTICK')


# Test code to see if all moving parts are functional

input('Press enter: ')
text = STT_Segment.Azure_Speech_to_Text(azure_talkingstick, azure_serviceregion)

TTS_Segment.Text_input_Speech_output(text, elevenlabs_talkingstick)


