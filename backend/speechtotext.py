import os
import time
import logging
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import stranslate as mt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")

# HTML code for speech recognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>

    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); 
            recognition.lang = 'en-US';  // You can set the language here
            recognition.continuous = true;
            recognition.interimResults = false;  // Only capture final results

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript.trim();
                output.textContent = transcript;  // Overwrite instead of appending
            };

            recognition.onend = function() {
                recognition.start();
            };

            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML += '<br><strong>Recognition stopped.</strong>';
        }
    </script>
</body>
</html>
'''

# Create the necessary directories if they don't exist
output_dir = r"Data\voice"
os.makedirs(output_dir, exist_ok=True)

# Set the input language for speech recognition
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save the HTML file
with open(os.path.join(output_dir, "Voice.html"), "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()
Link = f"{current_dir}/Data/voice/Voice.html"

# Configure Chrome options
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.8.142.06 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

TempDirpath = rf"{current_dir}/Frontend/Files"

def SetAssistantStatus(Status):
    """Set the assistant's status."""
    with open(rf'{TempDirpath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    """Modify the query to ensure it ends with a proper punctuation mark."""
    new_query = Query.lower().strip()
    query_word = new_query.split()
    question_word = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's"]

    if any(word + " " in new_query for word in question_word):
        if query_word[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_word[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    """Translate the text to English if the input language is not English."""
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def CleanText(Text):
    """Clean and normalize the recognized text."""
    import re
    Text = re.sub(r'\s+', ' ', Text)  # Normalize spaces
    Text = re.sub(r'\b(\w+)( \1\b)+', r'\1', Text)  # Remove duplicate words
    Text = re.sub(r'[^\w\s.,?!]', '', Text)  # Remove special characters
    return Text.strip()

def SpeechRecognition():
    """Perform speech recognition using the HTML file and WebDriver."""
    driver.get("file:///" + Link)

    try:
        # Wait for the start button to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "start"))
        )

        # Start speech recognition by clicking the start button
        driver.find_element(by=By.ID, value="start").click()
        logging.info("Speech recognition started.")

        start_time = time.time()
        timeout = 30  # Timeout after 30 seconds of no speech

        while True:
            try:
                # Wait for the output to be populated
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "output"))
                )
                
                # Get the recognized text from the HTML element
                Text = driver.find_element(by=By.ID, value="output").text

                if Text:
                    # Stop speech recognition by clicking the end button
                    driver.find_element(by=By.ID, value="end").click()
                    logging.info("Speech recognition stopped.")

                    # Clean and process the recognized text
                    Text = CleanText(Text)

                    # If the input language is English, return the modified query
                    if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                        return QueryModifier(Text)
                    else:
                        SetAssistantStatus("Translating...")
                        return QueryModifier(UniversalTranslator(Text))

                # Check for timeout
                if time.time() - start_time > timeout:
                    logging.warning("Speech recognition timed out.")
                    driver.find_element(by=By.ID, value="end").click()
                    return None

            except Exception as e:
                logging.error(f"Error while recognizing text: {e}")
                break  # Exit the loop if an error occurs

    except Exception as e:
        logging.error(f"Error opening the HTML file or interacting with WebDriver: {e}")

def CommandHandler(command):
    """Handle multiple commands based on the recognized speech."""
    command = command.lower()

    if "open" in command:
        app_name = command.replace("open", "").strip()
        logging.info(f"Opening {app_name}...")
        # Add logic to open the application
        return f"Opening {app_name}..."

    elif "close" in command:
        app_name = command.replace("close", "").strip()
        logging.info(f"Closing {app_name}...")
        # Add logic to close the application
        return f"Closing {app_name}..."

    elif "play" in command:
        song_name = command.replace("play", "").strip()
        logging.info(f"Playing {song_name}...")
        # Add logic to play the song
        return f"Playing {song_name}..."

    elif "search" in command:
        query = command.replace("search", "").strip()
        logging.info(f"Searching for {query}...")
        # Add logic to perform a search
        return f"Searching for {query}..."

    elif "exit" in command or "quit" in command:
        logging.info("Exiting the program...")
        return "Exiting the program..."

    else:
        logging.info("Command not recognized.")
        return "Command not recognized."

# Main execution block
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        if Text:
            print(f"Recognized Text: {Text}")
            response = CommandHandler(Text)
            print(response)
            if "exit" in response.lower() or "quit" in response.lower():
                break
        else:
            print("No speech detected or an error occurred.")
