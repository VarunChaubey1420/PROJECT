# ai_chat_assistant/app.py
"""
Simple terminal AI Chat Assistant (rule-based).
Run: python app.py
"""

import random
import time
import json
import os

HISTORY_FILE = "chat_history.json"

# Basic patterns/responses
RESPONSES = {
    "hello": ["Hey! 👋 How can I help?", "Hello! What's up?", "Hi there!"],
    "how are you": ["I'm a program — always ready 😄", "Good! Ready to help you."],
    "name": ["You can call me SimpleBot.", "I'm SimpleBot, your mini assistant."],
    "bye": ["Bye! Good luck 😊", "See ya — crush that hackathon!"],
    "thanks": ["You're welcome!", "Anytime!"],
}

DEFAULT_RESPONSES = [
    "Nice! Tell me more.",
    "Interesting — can you elaborate?",
    "I don't quite get that, but I can help with commands: (help)",
]

def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print("Could not save history:", e)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def find_response(user):
    u = user.lower()
    # direct commands
    if u in ("help", "commands"):
        return ("Commands:\n"
                "- help / commands: show this\n"
                "- joke: hear a joke\n"
                "- time: current time\n"
                "- history: show chat history\n"
                "- bye / exit: quit")
    if u == "joke":
        return random.choice([
            "Why do programmers prefer dark mode? Because light attracts bugs 😅",
            "I would tell you a UDP joke, but you might not get it."
        ])
    if u == "time":
        return time.strftime("Current time: %Y-%m-%d %H:%M:%S")

    # check keywords
    for key in RESPONSES:
        if key in u:
            return random.choice(RESPONSES[key])
    # if user inputs a math expression like "2+2"
    try:
        # NOT using eval directly on raw input for safety, but a small allowed check:
        if all(ch in "0123456789+-*/(). " for ch in u):
            result = eval(u)
            return f"The answer is: {result}"
    except:
        pass

    return random.choice(DEFAULT_RESPONSES)

def main():
    history = load_history()
    print("SimpleBot v1.0 — type 'help' for commands. Type 'bye' or 'exit' to quit.")
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        history.append({"you": user})
        if user.lower() in ("bye", "exit", "quit"):
            resp = find_response(user)
            print("Bot:", resp)
            history.append({"bot": resp})
            save_history(history)
            break
        if user.lower() == "history":
            print("--- Chat history ---")
            for item in history[-20:]:
                if "you" in item:
                    print("You:", item["you"])
                else:
                    print("Bot:", item["bot"])
            continue

        resp = find_response(user)
        print("Bot:", resp)
        history.append({"bot": resp})

    print("Goodbye!")

if __name__ == "__main__":
    main()
    