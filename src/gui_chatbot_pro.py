import tkinter as tk
from tkinter import scrolledtext, END, messagebox
from response import get_response
from datetime import datetime
import os

# --------------------------
# Paths
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "chat_history.txt")

# --------------------------
# Main Window Setup
# --------------------------
root = tk.Tk()
root.title("CoreDev Assistant")
root.geometry("650x550")
root.resizable(False, False)

# --------------------------
# Chat Display
# --------------------------
chat_display = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, state="disabled", font=("Helvetica", 12), bg="#f5f5f5"
)
chat_display.pack(padx=10, pady=(40, 10), fill=tk.BOTH, expand=True)

# --------------------------
# User Input Frame
# --------------------------
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5, fill=tk.X)

user_input = tk.Entry(input_frame, font=("Helvetica", 12))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
user_input.focus()


# --------------------------
# Chat Logging
# --------------------------
def log_message(sender, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {sender}: {message}\n")


# --------------------------
# Clear Chat
# --------------------------
def clear_chat():
    if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat?"):
        chat_display.config(state="normal")
        chat_display.delete("1.0", END)
        chat_display.config(state="disabled")


clear_button = tk.Button(
    root,
    text="Clear Chat",
    command=clear_chat,
    bg="#f44336",
    fg="white",
    font=("Helvetica", 10, "bold"),
)
clear_button.place(x=550, y=5, width=90, height=30)


# --------------------------
# Send Message
# --------------------------
def send_message(event=None):
    msg = user_input.get().strip()
    if msg == "":
        return

    # Display user message
    timestamp = datetime.now().strftime("%H:%M")
    chat_display.config(state="normal")
    chat_display.insert(END, f"You ({timestamp}): {msg}\n", "user")
    chat_display.config(state="disabled")
    chat_display.yview(END)
    log_message("User", msg)
    user_input.delete(0, END)

    # Bot typing indicator
    chat_display.config(state="normal")
    chat_display.insert(END, "Bot is typing...\n", "typing")
    chat_display.config(state="disabled")
    chat_display.yview(END)
    root.update()

    # Get bot response
    response = get_response(msg)

    # Replace typing indicator with response
    chat_display.config(state="normal")
    chat_display.delete("end-2l", "end-1l")  # remove "Bot is typing..."
    chat_display.insert(END, f"Bot ({timestamp}): {response}\n\n", "bot")
    chat_display.config(state="disabled")
    chat_display.yview(END)
    log_message("Bot", response)


user_input.bind("<Return>", send_message)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    width=10,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 10, "bold"),
)
send_button.pack(side=tk.RIGHT)

# --------------------------
# Text Styles
# --------------------------
chat_display.tag_config("user", foreground="blue", font=("Helvetica", 12, "bold"))
chat_display.tag_config("bot", foreground="green", font=("Helvetica", 12))
chat_display.tag_config("typing", foreground="orange", font=("Helvetica", 12, "italic"))

# --------------------------
# Header
# --------------------------
header = tk.Label(
    root,
    text="🚀 CoreDev Assistant",
    font=("Helvetica", 16, "bold"),
    bg="#222",
    fg="white",
)
header.place(x=0, y=0, width=650, height=30)

# --------------------------
# Start GUI
# --------------------------
chat_display.config(state="normal")
chat_display.insert(
    END, "CoreDev Assistant is ready! Ask me anything about programming.\n\n", "bot"
)
chat_display.config(state="disabled")

root.mainloop()
