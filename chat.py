import requests  # Import the library for making HTTP requests
import json      # Import the library for working with JSON data

def get_response(prompt):
    """
    Sends a prompt to the Ollama API and returns the response.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        The generated text response from the model, or an error message.
    """
    url = "http://localhost:11434/api/generate"  # The URL of the Ollama API
    headers = {"Content-Type": "application/json"}  # Set the content type for the request
    data = {
        "model": "gemma2:2b",  # The name of the Ollama model to use
        "prompt": prompt,      # The prompt to send to the model
        "stream": False # Disable streaming for easier processing
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10) # Send POST request with timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()['response'] # Return the generated text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Error: Could not get response."
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.text}") # Print raw response for debugging
        return "Error: Could not parse response."

if __name__ == "__main__": # this ensures that the code below only runs when the script is executed directly (not when imported as a module).
    print("Witaj na chatcie GDG!")
    while True: # Start an infinite loop for the chat
        user_input = input("You: ") # Get input from the user
        if user_input.lower() in ["exit", "quit"]: # Check if the user wants to exit
            break # Exit the loop if the user types "exit" or "quit"
        if not user_input.strip(): #if user input is empty string - continue
            continue
        ai_response = get_response(user_input) # Get the AI's response
        print("AI:", ai_response) # Print the AI's response
    print("Do Zobaczenia!")
