import os
import requests
import json
from datetime import datetime


API_URL = "http://127.0.0.1:8000/chat"

def save_chat_log(history):
    if not history:
        return 
    
    #Creates log directory if it doesn't exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    #Save inside logs folder
    filename = os.path.join("logs",f"chat_log_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(history, f, indent=4)
        
    print(f"\nConversation saved to  {filename}")


def chat():
    print("---Gen AI Project (Type 'exit' to quit)---")

    # Local history Storage
    history = []

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit','quit']:
            save_chat_log(history)  #saving before leaving
            break

        #adding user_input to history
        history.append({"role": "user", "content": user_input})

        try:
            print("Assistant is thinking...", end = "\r")

            #Sending request with 60-second timeout
            response = requests.post(
                API_URL,
                json = {"message": history},
                timeout = 120
            )

            if response.status_code == 200:
                ai_message = response.json().get("response")
                print(f"Assistant: {ai_message}")

                #Adding assiatant reponse to history
                history.append({"role": "Assistant", "content": ai_message})

            else:
                error_detail = response.json.get("message","Unknown Error")
                print(f"\nError: {error_detail}")

        except requests.exceptions.Timeout:
            print("\nError: The Server took too long to respond. (Timeout)")
        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to the server. Is FastAPI running ?")

if __name__ == "__main__":
    chat()