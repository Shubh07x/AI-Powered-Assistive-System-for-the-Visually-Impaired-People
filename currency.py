import time
from inference import get_model
import supervision as sv
import cv2
import pyttsx3
import numpy as np

engine = pyttsx3.init()
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_HemantM")

def speak_detected_notes(detections):
    if 'class_name' in detections.data and len(detections.confidence) > 0:
        detected_notes = detections.data['class_name']
        confidence_scores = detections.confidence

        max_confidence_index = np.argmax(confidence_scores)

        note_with_highest_confidence = detected_notes[max_confidence_index]

        if note_with_highest_confidence=="3- 50 Rupees":
            note_with_highest_confidence="पन्नास रुपये"
        elif note_with_highest_confidence=="1- 10 Rupees":
            note_with_highest_confidence = "दहा रुपये"
        elif note_with_highest_confidence=="2- 20 Rupees":
            note_with_highest_confidence = "वीस रुपये"
        elif note_with_highest_confidence=="4- 100 Rupees":
            note_with_highest_confidence = "शंभर रुपये"
        elif note_with_highest_confidence=="5- 200 Rupees":
            note_with_highest_confidence = "दोनशे रुपये"
        elif note_with_highest_confidence=="6- 500 Rupees":
            note_with_highest_confidence = "पाचशे रुपये"

        engine.say(note_with_highest_confidence)
        engine.runAndWait()
    else:
        print("No valid detections found.")

model = get_model(model_id="currency-detection-cgpjn/2", api_key="82sO0Pmt3qC4qc7RQy6K")

bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

cap = cv2.VideoCapture(0)  # Use 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    results = model.infer(frame)

    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
    annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections)
    cv2.imshow("Currency Detection - Real Time", annotated_frame)
    time.sleep(3)
    speak_detected_notes(detections)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

