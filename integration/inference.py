import torch
import cv2
from PIL import Image
from models.blip import blip_decoder
import numpy as np
import utils
import pyttsx3
from googletrans import Translator
def init_model(device):
    print("Loading checkpoint...")
    model = blip_decoder(
        pretrained="./checkpoints/model_large_caption.pth", image_size=384, vit="large"
    )
    model.eval()
    model = model.to(device)
    print(f"Model loaded to {device}")
    return model


def preprocess_webcam_image(frame, device):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)

    transformed_image = utils.prep_images([pil_image], device)[0]
    return transformed_image


def capture_and_caption(model, device):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'Space' to capture an image and generate a caption.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        cv2.imshow("Webcam Feed - Press Space to Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            print("Processing image...")
            image_tensor = preprocess_webcam_image(frame, device)

            with torch.no_grad():
                caption = model.generate(
                    image_tensor, sample=False, num_beams=3, max_length=20, min_length=5
                )
                engine=pyttsx3.init()
                engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_HemantM")
                t=Translator()
                newText=caption[0]
                newText=t.translate(newText,dest='mr')
                print("Generated Caption:", caption[0])
                print("Generated Caption:", newText.text)
                engine.say(newText.text)
                engine.runAndWait()
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    model = init_model(device)
    capture_and_caption(model, device)

