import ollama
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

# Retrieve variables from .env file
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
InputLanguage = env_vars.get("InputLanguage")
AssistantVoice = env_vars.get("AssistantVoice")

# Ollama model to use
OLLAMA_MODEL = "nemotron-3-nano:30b-cloud"  # You can change this to any model available in Ollama

messages = []

# System message and preamble
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi convert it in English, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***

Current time: {datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")}
"""

# Try to load the chat log, create if not found
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to fetch real-time information
def RealtimeInformation():
    current_data_time = datetime.datetime.now()
    day = current_data_time.strftime("%A")
    date = current_data_time.strftime("%d")
    month = current_data_time.strftime("%B")
    year = current_data_time.strftime("%Y")
    hour = current_data_time.strftime("%H")
    minute = current_data_time.strftime("%M")
    second = current_data_time.strftime("%S")

    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours {minute} minutes {second} seconds\n"
    return data

# Function to modify the answer
def AnswerModifier(Answer):
    line = Answer.split('\n')
    non_empty_lines = [line for line in line if line.strip()]
    return non_empty_lines

# Main chatbot function
def Chatbot(query):
    """This function sends the user's query to the chatbot and returns the AI's response."""
    
    # Load previous messages
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        # Append user message to chat history
        messages.append({"role": "user", "content": f"{query}"})

        # Fetch real-time information
        real_time_info = RealtimeInformation()

        # Prepare the messages for Ollama
        ollama_messages = [{"role": "system", "content": System + real_time_info}]
        for msg in messages:
            ollama_messages.append({"role": msg["role"], "content": msg["content"]})

        # Call Ollama API for response
        try:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=ollama_messages,
                options={
                    'temperature': 0.7,
                    'num_predict': 1024
                }
            )
            Answer = response['message']['content']
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            Answer = "I'm sorry, I'm having trouble processing your request right now."

        # Clean the answer
        Answer = Answer.replace("</s>", "").strip()

        # Append AI's answer to the messages
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return Answer
    
    except Exception as e:
        return f"Error: {e}"

# Main loop to take input from the user
if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        response = Chatbot(user_input)
        print(response)
