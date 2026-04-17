import ollama
from rich import print
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

# Ollama model to use
OLLAMA_MODEL = "nemotron-3-nano:30b-cloud"  # You can change this to any model available in Ollama

# List of functions that the bot will handle (added "vision")
funcs = [
    "exit", "general", "realtime", "vision", "open", "close", "play",
    "system", "content", "google", "youtube search", "reminder"
]

messages = []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, a 'vision' query (requiring an image from the camera), or is asking to perform any task or automation like 'open facebook, instagram', 'can you write an application and open it in notepad'.
*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general (query)' if a query can be answered by an LLM model (conversational AI chatbot) and doesn't require any up-to-date information.
    Examples:
    - "who was akbar?" → 'general who was akbar?'
    - "how can I study more effectively?" → 'general how can I study more effectively?'
    - "can you help me with this math problem?" → 'general can you help me with this math problem?'
    - "Thanks, I really liked it." → 'general thanks, I really liked it.'
    - "what is python programming language?" → 'general what is python programming language?'
    - "What is machine learning?" → 'general What is machine learning?'
    - "Who invented the telephone?" → 'general Who invented the telephone?'
    - "Can you tell me about the solar system?" → 'general Can you tell me about the solar system?'
    - "What is the capital of France?" → 'general What is the capital of France?'
    - "How does the internet work?" → 'general How does the internet work?'
    - "What is the meaning of life?" → 'general What is the meaning of life?'
    - "What is the largest planet in our solar system?" → 'general What is the largest planet in our solar system?'

-> Respond with 'realtime (query)' if a query requires real-time information or up-to-date data such as current events, weather, or time-sensitive events.
    Examples:
    - "what is the weather today?" → 'realtime what is the weather today?'
    - "who won the last cricket match?" → 'realtime who won the last cricket match?'
    - "what is the stock price of Apple?" → 'realtime what is the stock price of Apple?'
    - "tell me the latest news on climate change" → 'realtime tell me the latest news on climate change'
    - "What time is it now?" → 'realtime What time is it now?'
    - "What is the news today?" → 'realtime What is the news today?'
    - "How much is Bitcoin worth today?" → 'realtime How much is Bitcoin worth today?'

-> Respond with 'vision (query)' if a query requires seeing the user or the environment through the camera. This includes questions about who is in front of the camera, hand gestures (like counting fingers), facial expressions (emotion), or any visual recognition task.
    Examples:
    - "how many fingers am I showing?" → 'vision how many fingers am I showing?'
    - "what is my emotion?" → 'vision what is my emotion?'
    - "what do you see?" → 'vision what do you see?'
    - "can you see me?" → 'vision can you see me?'
    - "identify the person in front of the camera" → 'vision identify the person in front of the camera'
    - "what's in front of you?" → 'vision what's in front of you?'
    - "count my fingers" → 'vision count my fingers'
    - "how do I look?" → 'vision how do I look?'
    - "am I smiling?" → 'vision am I smiling?'
    - "what color is my shirt?" → 'vision what color is my shirt?'

-> Respond with 'task (query)' if a query asks the model to perform a task or automation (like opening applications, creating files, etc.).
    Examples:
    - "open facebook" → 'task open facebook'
    - "open instagram" → 'task open instagram'
    - "can you write a simple application and open it in notepad?" → 'task can you write a simple application and open it in notepad'
    - "remind me to call John at 3 PM" → 'task remind me to call John at 3 PM'
    - "open youtube and play a song" → 'task open youtube and play a song'
    - "Can you open Microsoft Word?" → 'task Can you open Microsoft Word?'

-> Respond with 'open (application name or website name)' if the query requests opening an application or website.
    Examples:
    - "open chrome" → 'open chrome'
    - "open google" → 'open google'
    - "open facebook" → 'open facebook'
    - "open instagram" → 'open instagram'

-> Respond with 'close (application name)' if the query requests closing an application.
    Examples:
    - "close chrome" → 'close chrome'
    - "close youtube" → 'close youtube'

-> Respond with 'play (song name)' if the query asks to play a song.
    Examples:
    - "play my favorite song" → 'play my favorite song'
    - "play the latest hit song" → 'play the latest hit song'

-> Respond with 'system' if the query is related to system-related tasks or information.
    Examples:
    - "show me system information" → 'system show me system information'
    - "check disk usage" → 'system check disk usage'

-> Respond with 'content (topic)' if the query is asking about content on a specific topic.
    Examples:
    - "content about AI" → 'content about AI'
    - "content on machine learning" → 'content on machine learning'

-> Respond with 'google search (topic)' if the query asks to search something on Google.
    Examples:
    - "google search python programming" → 'google search python programming'
    - "google latest news" → 'google search latest news'
    - "search for machine learning tutorials on Google" → 'google search machine learning tutorials'
    - "look up the latest AI developments on Google" → 'google search latest AI developments'

-> Respond with 'youtube search (topic)' if the query asks to search something on YouTube.
    Examples:
    - "youtube search python tutorial" → 'youtube search python tutorial'
    - "youtube search machine learning video" → 'youtube search machine learning video'

-> Respond with 'exit' if the user asks to exit or says goodbye.
    Examples:
    - "bye" → 'exit'
    - "goodbye" → 'exit'
    - "exit" → 'exit'
    - "see you later" → 'exit'
    - "take care" → 'exit'
    - "quit" → 'exit'
    - "stop" → 'exit'
    - "end" → 'exit'
    - "that's all" → 'exit'
    - "I'm done" → 'exit'

-> Do not answer the query, just classify it as one of the above categories.
"""

# Define the first layer DMM function
def FirstlayerDMM(prompt: str):
    # Prepare the messages for Ollama
    ollama_messages = [{"role": "system", "content": preamble}]
    
    # Add the current user message
    ollama_messages.append({"role": "user", "content": prompt})
    
    try:
        # Call Ollama API for response
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=ollama_messages,
            options={
                'temperature': 0.7,
                'num_predict': 512
            }
        )
        response_text = response['message']['content']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ["general " + prompt]  # Fallback to general if Ollama fails
    
    # Clean and split the response
    response_text = response_text.replace("\n", "")
    response = response_text.split(",")
    response = [i.strip() for i in response]
    
    temp = []
    
    # Filter response based on predefined tasks
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
    
    response = temp
    
    # If the query contains "(query)", process further
    if "(query)" in str(response):
        # Recursively call FirstlayerDMM
        newresponse = FirstlayerDMM(prompt=prompt)
        return newresponse
    else:
        return response

# Main loop to take input from the user
if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ["bye", "goodbye", "exit", "quit", "stop", "end", "that's all", "i'm done"]:
            print("Goodbye! Have a great day!")
            break
        response = FirstlayerDMM(user_input)
        print(response)