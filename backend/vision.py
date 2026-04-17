import cv2
import os
import ollama
from datetime import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

OLLAMA_MODEL = "qwen3-vl:235b-instruct-cloud"  # multimodal model

# Temporary directory for captured images
TEMP_IMAGE_DIR = r"Data\vision_temp"
os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)

def capture_image():
    """
    Captures an image from the default camera and saves it as a timestamped file.
    Returns the file path if successful, else None.
    """
    try:
        # Initialize camera
        cap = cv2.VideoCapture(0)  # 0 is usually the built-in webcam
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return None

        # Allow camera to warm up
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            cap.release()
            return None

        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(TEMP_IMAGE_DIR, f"capture_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        cap.release()
        return image_path

    except Exception as e:
        print(f"Camera capture error: {e}")
        return None

def VisionChatbot(query, image_path):
    """
    Sends the query and image to the multimodal model and returns the answer.
    """
    # Prepare the messages with image
    # According to Ollama API, images can be passed as a list of base64 strings or file paths.
    # We'll pass the file path as a string in a "images" field.
    messages = [
        {
            "role": "user",
            "content": query,
            "images": [image_path]  # Ollama accepts file paths
        }
    ]

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            options={
                'temperature': 0.7,
                'num_predict': 1024
            }
        )
        answer = response['message']['content']
        return answer.strip()
    except Exception as e:
        print(f"Error in VisionChatbot: {e}")
        return "Sorry, I had trouble processing the image."

# Example usage (for testing)
if __name__ == "__main__":
    img = capture_image()
    if img:
        print(VisionChatbot("Who is in this image?", img))
        # Optionally delete the image after use
        os.remove(img)