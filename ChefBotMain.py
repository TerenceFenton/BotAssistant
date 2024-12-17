import TTS_Segment
import time

text = input('Speaketh and I shall repeat: ')
time.sleep(1)
while text != 'quit':
    TTS_Segment.Text_input_Speech_output(text)
    text = input('Speaketh and I shall repeat: ')
    time.sleep(1)
else:
    text = 'Goodbye you sexy sexy man'
    TTS_Segment.Text_input_Speech_output(text)


