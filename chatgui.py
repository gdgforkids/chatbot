import requests
import json
import tkinter as tk
from tkinter import scrolledtext

def get_response(prompt):
    """Sends a prompt to the Ollama API and returns the response."""
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma2:2b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Error: Could not get response."
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {e}")
        return "Error: Could not parse response."

def send_message():
    """Sends the user's message and displays the AI's response."""
    user_message = user_input.get("1.0", tk.END).strip()
    if not user_message:
        return  # Don't send empty messages

    chat_log.config(state=tk.NORMAL) # Enable editing
    chat_log.insert(tk.END, "You: " + user_message + "\n")
    chat_log.config(state=tk.DISABLED) # Disable editing

    user_input.delete("1.0", tk.END) # Clear input field

    ai_response = get_response(user_message)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "AI: " + ai_response + "\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END) # Autoscroll to the bottom


root = tk.Tk()
root.title("Gemma2:2b Chat")

# Chat Log (Scrolled Text)
chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# User Input (Text Area)
user_input = tk.Text(root, height=3)
user_input.pack(padx=10, pady=(0, 10), fill=tk.X)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=(0,10))

root.bind('<Return>', lambda event=None: send_button.invoke()) # Bind Enter key to send button

root.mainloop()
