from ultralytics import YOLO
import cv2
import pyttsx3
model = YOLO("../yolo11n.pt")
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_HemantM")

FOCAL_LENGTH = 500
REAL_OBJECT_HEIGHT = 1.7
PROXIMITY_THRESHOLD = 0.8
ROI = (200, 150, 400, 300)

def calculate_proximity_percentage(focal_length, real_height, pixel_height):
    distance = (focal_length * real_height) / pixel_height
    proximity_percentage = (real_height / distance) * 100
    return proximity_percentage

def speak(text):
    """Give audio output."""
    engine.say(text)
    engine.runAndWait()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    x, y, w, h = ROI
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame,"", (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            obj_class = int(box.cls[0])
            obj_name = result.names[obj_class]

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            pixel_height = abs(y2 - y1)

            proximity_percentage = calculate_proximity_percentage(FOCAL_LENGTH, REAL_OBJECT_HEIGHT, pixel_height)

            if x <= center_x <= x + w and y <= center_y <= y + h:
                if proximity_percentage >= PROXIMITY_THRESHOLD * 100:
                    if center_x < x + w // 2:
                        speak("ऊजविकडे चला")
                        cv2.putText(frame, "Move right", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    else:
                        speak("डावीकडून चला")
                        cv2.putText(frame, "Move left", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f"{obj_name} {proximity_percentage:.2f}%", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 0, 0), 2)

    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
