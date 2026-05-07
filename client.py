import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# load the key from .env
load_dotenv()
API_KEY = os.getenv("API_SECRET_KEY")
API_URL = "http://127.0.0.1:8000/chat"


def save_chat_log(history, selected_mode):
    if not history:
        return 
    
    #Creates log directory if it doesn't exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    #Save inside logs folder
    filename = os.path.join("logs",f"{selected_mode}_chat_log_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(history, f, indent=4)
        
    print(f"\nConversation saved to  {filename}")


def chat():
    print()
    print("---Gen AI Project (Type 'exit' to quit)---")
    print()
    print("Available Modes: mentor, sql, coder")
    print()

    #Simple mode selection
    selected_mode = input("Select mode (default=mentor): ").strip().lower()
    if selected_mode not in ["mentor","sql","coder"]:
        selected_mode = "mentor"

    print(f"-----Active Mode: {selected_mode.upper()}-----")

    # Local history Storage
    history = []

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit','quit']:
            save_chat_log(history, selected_mode)  #saving before leaving
            break

        #adding user_input to history
        history.append({"role": "user", "content": user_input})

        try:

            # We add the "access_tokem" to the headers
            headers = {"access_token": API_KEY}
            
            print("Assistant: ", end = "", flush = True)

            #Sending request with 60-second timeout
            response = requests.post(
                API_URL,
                json = {"message": history,
                        "mode" : selected_mode
                    },
                headers = headers,
                stream=True,
                timeout = 120
            )

            if response.status_code == 403:
                print("\nError: API Key is invalid or missing")
                break

            full_response_content = ""

            #Iterating over chunk of text coming form the server.
            for chunk in response.iter_content(decode_unicode=True):
                if chunk:
                    print(chunk, end="", flush=True)    #printing word by word
                    full_response_content += chunk

            print() #Move to next line after finished

            if response.status_code == 200:
                history.append({"role": "Assistant", "content": full_response_content})

            else:
                print(f"\nError: {response.status_code}")

        except Exception as e:
            print(f"\nConnectino Error: {e}")

if __name__ == "__main__":
    chat()