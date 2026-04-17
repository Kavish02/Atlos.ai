# Atlos.ai
**Genius AI Assistant – Voice-Controlled Desktop Assistant with GUI**


Genius is a voice‑controlled AI assistant built in Python. It combines a modern PyQt5 graphical interface with advanced natural language understanding (via Ollama), real‑time web search, and desktop automation. You can talk to it, ask questions, give commands to open/close applications, search the web, play YouTube videos, and much more – all hands‑free.

✨ Features
🎤 Voice Interaction
Speech recognition using the browser’s Web Speech API (driven by Selenium). Supports multiple input languages with automatic translation to English.

🧠 Conversational AI
Powered by Ollama (configurable model). Handles general chit‑chat, remembers user details across sessions (chat history stored in ChatLog.json).

🌐 Real‑time Information
Performs Google searches on‑the‑fly and incorporates the results into answers – perfect for weather, news, stock prices, etc.

🖥️ Desktop Automation

Open/close applications (uses AppOpener).

Play songs on YouTube (pywhatkit).

Control system volume (keyboard shortcuts).

Generate and save content to text files.

Google and YouTube searches directly from voice commands.

🎨 Graphical User Interface
Built with PyQt5 – features a home screen with an animated GIF, a chat screen to display conversations, and a top bar with window controls (minimize, maximize, close).

🗣️ Text‑to‑Speech
Uses edge‑tts (Microsoft Edge’s TTS engine) for natural‑sounding speech output. Audio is played via pygame.

🧩 Extensible Decision Engine
A dedicated “first layer” model (model.py) classifies every query into categories: general, real‑time, task, open/close, play, system, content, etc. This makes the system modular and easy to extend.

🧱 Architecture Overview
Module	Responsibility
Main.py	Entry point; initialises the GUI and background threads for listening/responding.
GUI.py	PyQt5 interface – home screen, chat area, microphone toggle, status display.
model.py	First‑layer decision model (Ollama) – classifies user intent.
chatbot.py	Handles general conversation (Ollama) and maintains chat history.
RealtimeSearchEngine.py	Performs Google searches and returns AI‑generated answers using search results.
automation.py	Executes system commands: opening/closing apps, YouTube playback, volume control, etc.
speechtotext.py	Speech recognition via Selenium‑controlled HTML page (Web Speech API).
TextToSpeech.py	Converts text to speech using edge‑tts and plays it with pygame.
Data/	Stores chat logs, temporary files, and generated content.
🛠️ Technologies Used
Python 3.9+

Ollama – Local LLM inference

PyQt5 – GUI framework

Selenium + ChromeDriver – Speech recognition interface

edge‑tts – Microsoft Edge TTS engine

pygame – Audio playback

googlesearch‑python – Google search results

pywhatkit – YouTube playback

AppOpener – Cross‑platform app control

keyboard – System volume control

python‑dotenv – Environment variable management

rich – Pretty console output

🚀 Installation & Setup
1. Clone the repository
bash
git clone https://github.com/yourusername/genius-ai-assistant.git
cd genius-ai-assistant
2. Create and activate a virtual environment (recommended)
bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
3. Install dependencies
bash
pip install -r requirements.txt
Note: If you don’t have a requirements.txt, manually install the packages listed in the code:

bash
pip install PyQt5 selenium webdriver-manager edge-tts pygame googlesearch-python pywhatkit AppOpener keyboard rich python-dotenv ollama
4. Install Ollama and pull a model
Download and install Ollama from ollama.com

Pull a model (the code uses minimax-m2:cloud – you can change it in the .env or directly in the code)

bash
ollama pull minimax-m2:cloud
If you prefer a different model, update the OLLAMA_MODEL variable in chatbot.py, model.py, and RealtimeSearchEngine.py accordingly.

5. Configure environment variables
Create a .env file in the project root with the following keys:

ini
Username=Arjun
Assistantname=Genius
InputLanguage=en-US          # Language code for speech recognition (e.g., hi-IN, en-US)
AssistantVoice=en-US-EmmaNeural   # Edge‑TTS voice (run `edge-tts --list-voices` to see options)
6. Prepare the file structure
The program expects the following directories (they will be created automatically, but ensure write permissions):

Data/ – for chat logs and temporary files

frountend/Files/ – for status and response files

frountend/Graphics/ – for images/GIFs (you need to place your own graphics there; the code references GENE.gif, Mic_on.png, Mic_off.png, Home.png, Chats.png, Minimize2.png, Maximize.jpg, close.jpg).
Place suitable icons or modify the paths in GUI.py.

7. Run the assistant
bash
python Main.py
The GUI will appear. Click the microphone icon to start speaking, or use the “Chat” button to view the conversation history.

🎙️ How to Use
Wake / Listen – Click the microphone icon on the home screen. The icon toggles between on (green) and off (red).

Speak your command – After clicking the mic, say something like:

“What is the weather today?”

“Open Chrome”

“Play Shape of You”

“Who is Elon Musk?”

“Remind me to call John at 3 PM” (reminder functionality is a placeholder; you can extend it)

“Goodbye” (exits the program)

The assistant will process your speech, show the recognised text on the chat screen, and respond both in text and speech.

📁 File Structure (Simplified)
text
.
├── Main.py                      # Entry point
├── GUI.py                        # PyQt5 interface
├── model.py                      # Intent classification
├── chatbot.py                    # General conversation
├── RealtimeSearchEngine.py        # Google search + answer synthesis
├── automation.py                 # App control & system commands
├── speechtotext.py               # Speech recognition via Selenium
├── TextToSpeech.py               # Text‑to‑speech (edge‑tts + pygame)
├── .env                           # Environment variables
├── Data/                          # Chat logs, generated content
│   ├── ChatLog.json
│   └── voice/                     # HTML file for speech recognition
├── frountend/                     # Frontend resources
│   ├── Files/                     # Temporary status files
│   └── Graphics/                   # Images and GIFs (user‑supplied)
└── requirements.txt               # Python dependencies
⚙️ Configuration & Customisation
Change the LLM model – In the three files mentioned above, replace OLLAMA_MODEL with any model you have pulled via Ollama.

Voice – Set AssistantVoice in .env to any Edge‑TTS voice (e.g., en-GB-SoniaNeural). List all voices with edge-tts --list-voices.

Input language – InputLanguage controls the speech recogniser’s language. If not English, speech is automatically translated to English before processing.

Graphics – Replace the GIFs and icons in frountend/Graphics/ with your own (keeping the same filenames or updating the paths in GUI.py).

🐛 Troubleshooting
Selenium / ChromeDriver issues – webdriver-manager should automatically download the correct driver. If problems persist, install ChromeDriver manually and update the path in speechtotext.py.

Ollama not responding – Ensure the Ollama service is running (ollama serve). Check that the model name is correct.

Microphone not working – The speech recognition uses the browser’s API; make sure your browser (Chrome) has microphone permissions enabled.

Audio not playing – Verify that speech.mp3 is generated in Data/. Install required codecs if necessary.

📌 Future Improvements
Add support for reminders and alarms.

Integrate email and messaging.

Implement more robust wake‑word detection.

Allow customisable hotkeys.

Package as a standalone executable.

📄 License
This project is open source and available under the MIT License.

🙏 Acknowledgements
Ollama for making local LLMs easy.

Microsoft Edge‑TTS for high‑quality voices.

The creators of PyQt5, Selenium, and all other libraries used.

🌱 **Sustainability & Green‑Code Practices**
- **Eco‑Mode**: Set `ECO_MODE=1` in `.env` to skip heavyweight operations (Google search, speech recognition, TTS) when low‑power or battery‑saving is needed.
- **Caching**: Re‑used results and audio files are cached on disk; old cache entries are pruned automatically.
- **Resource Limits**: Message history is truncated (`max_length=15`) to keep memory usage low.
- **Lazy Loading**: External services (search, TTS, speech recognition) are only invoked when necessary.
- **Environment‑Driven Configuration**: All tunable parameters are stored in `.env`, allowing easy adjustment without code changes.
- **Profiling**: `@profile` decorator measures execution time, helping identify and eliminate inefficient code paths.
- **Dependency Minimisation**: Only essential libraries are imported; heavy optional features are guarded by `ECO_MODE`.
