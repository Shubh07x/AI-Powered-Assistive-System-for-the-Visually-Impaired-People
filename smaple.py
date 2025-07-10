import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

print(voices)
# # Print details of each voice
# for voice in voices:
#     # print(f"Voice {index}:")
#     print(f" - ID: {voice.id}")
#     print(f" - Name: {voice.name}")
#     print(f" - Languages: {voice.languages}")
#     print(f" - Gender: {voice.gender}")
#     print(f" - Age: {voice.age}")
#     print()
