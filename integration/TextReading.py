from PIL import Image
import easyocr
import cv2
import pyttsx3
import numpy as np
from googletrans import Translator
reader = easyocr.Reader(['en'])
engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_HemantM")
translator = Translator()
cap = cv2.VideoCapture(0)
print("Press the 'Space' bar to capture a frame and extract text.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    cv2.imshow("Live Webcam", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        temp_image = Image.fromarray(rgb_frame)
        temp_image.save("temp_image.png")

        result = reader.readtext("temp_image.png")

        detected_texts = [detection[1] for detection in result]
        all_text = ' '.join(detected_texts)

        print("Detected Text:", all_text)
        all_text = translator.translate(all_text, dest='mr')
        print("Detected Text:", all_text.text)
        engine.say(all_text.text)
        engine.runAndWait()

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
