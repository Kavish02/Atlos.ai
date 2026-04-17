import pygame
import random
import asyncio
import edge_tts
import os
import dotenv

# Load environment variables
dotenv.load_dotenv(".env")
AssistantVoice = os.getenv("AssistantVoice")  # Get the voice from .env

async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    # Delete existing audio file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    try:
        # Convert text to speech and save as audio file
        communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+10%')
        await communicate.save(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to generate speech: {e}")

def TTS(text, func=lambda r=None: True):
    try:
        # Run the async function to convert text to speech
        asyncio.run(TextToAudioFile(text))

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        # Play the audio while checking if the function allows it to continue
        while pygame.mixer.music.get_busy():
            if not func():  # Check if the function indicates to stop
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        # Ensure pygame mixer is properly stopped and quit
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            func(False)
        except Exception as stop_e:
            print(f"Error in finally block: {stop_e}")

def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "I've displayed the remaining information on the chat interface for your convenience.",
        "Please check the chat screen for the complete response.",
        "The full answer is available in the chat window.",
        "I've sent the remaining details to the chat screen for your review.",
        "The rest of the information is now visible in the chat interface.",
        "Kindly refer to the chat screen for the complete answer.",
        "I've posted the remaining content to the chat window for your reference."
    ]

    if len(Data) > 4 and len(Text) > 250:
        TTS("".join(Text.split(".")[0:2]) + "." + random.choice(responses), func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        try:
            TextToSpeech(input("Enter the text: "))
        except KeyboardInterrupt:
            print("Exiting program.")
            break
