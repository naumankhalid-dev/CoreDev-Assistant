# src/gui_chatgpt_hybrid.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import json
import os
from response import get_response
from datetime import datetime

# ---------------- settings ----------------
BG = "#0b0c0e"
PANEL = "#0f1113"
USER_BUBBLE = "#1f2226"
BOT_BUBBLE = "#246b74"  # calm teal
USER_TEXT = "#e6e6e6"
BOT_TEXT = "#eaf7f6"
FONT = ("Segoe UI", 11)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(BASE_DIR, "chat_history.json")

# -------------- window --------------
root = tk.Tk()
root.title("CoreDev Assistant (Hybrid)")
root.geometry("1000x680")
root.configure(bg=BG)

# -------------- left sidebar --------------
left_frame = tk.Frame(root, bg=PANEL, width=260)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

title = tk.Label(
    left_frame,
    text="CoreDev Assistant",
    bg=PANEL,
    fg="#fff",
    font=("Segoe UI", 14, "bold"),
)
title.pack(pady=12)

history_label = tk.Label(
    left_frame, text="Conversations", bg=PANEL, fg="#bfc5c7", font=FONT
)
history_label.pack(anchor="w", padx=12)

history_list = tk.Listbox(
    left_frame, bg=PANEL, fg="#fff", bd=0, highlightthickness=0, activestyle="none"
)
history_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

btn_frame = tk.Frame(left_frame, bg=PANEL)
btn_frame.pack(fill=tk.X, pady=6, padx=10)

new_btn = tk.Button(btn_frame, text="New", bg="#2e3336", fg="#fff", relief=tk.FLAT)
new_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
save_btn = tk.Button(btn_frame, text="Save", bg="#2e3336", fg="#fff", relief=tk.FLAT)
save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

restart_btn = tk.Button(
    left_frame, text="Restart Conversation", bg="#2e3336", fg="#fff", relief=tk.FLAT
)
restart_btn.pack(fill=tk.X, padx=10, pady=(6, 12))

# -------------- right main area --------------
right_frame = tk.Frame(root, bg=BG)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas_frame = tk.Frame(right_frame, bg=BG)
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=(12, 12), pady=(12, 8))

canvas = tk.Canvas(canvas_frame, bg=BG, highlightthickness=0)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollable = tk.Frame(canvas, bg=BG)

scrollable.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# -------------- input area --------------
input_frame = tk.Frame(right_frame, bg=BG)
input_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

entry = tk.Entry(
    input_frame,
    bg="#0e1011",
    fg="#fff",
    insertbackground="#fff",
    font=FONT,
    relief=tk.FLAT,
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))

send_btn = tk.Button(
    input_frame, text="Send", bg=BOT_BUBBLE, fg=BOT_TEXT, relief=tk.FLAT
)
send_btn.pack(side=tk.RIGHT)

typing_label = tk.Label(right_frame, text="", bg=BG, fg="#9aa7a7", font=("Segoe UI", 9))
typing_label.pack(anchor="w", padx=14, pady=(0, 6))

# -------------- conversation store --------------
conversations = []
current_idx = None


def new_conversation():
    global current_idx
    conv = {"title": f"Conversation {len(conversations) + 1}", "messages": []}
    conversations.insert(0, conv)
    current_idx = 0
    refresh_history()
    load_conversation(0)


def save_conversation():
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(conversations, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Save", "Conversations saved to chat_history.json")
    except Exception as e:
        messagebox.showerror("Save error", str(e))


def refresh_history():
    history_list.delete(0, tk.END)
    for conv in conversations:
        history_list.insert(tk.END, conv["title"])


def load_conversation(index):
    global current_idx
    if index < 0 or index >= len(conversations):
        return
    current_idx = index
    clear_chat_area()
    conv = conversations[index]
    for m in conv["messages"]:
        if m["role"] == "user":
            add_user_bubble(m["text"], timestamp=m.get("ts"))
        else:
            add_bot_bubble(m["text"], timestamp=m.get("ts"))
    root.after(50, lambda: canvas.yview_moveto(1.0))


def append_message(role, text):
    if current_idx is None:
        new_conversation()
    conversations[current_idx]["messages"].append(
        {"role": role, "text": text, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    )


# -------------- UI bubble helpers --------------
def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Message copied to clipboard.")


def make_right_click_copy(widget, text):
    def on_copy(event=None):
        copy_to_clipboard(text)

    widget.bind("<Button-3>", lambda e: on_copy())


def add_user_bubble(text, timestamp=None):
    frame = tk.Frame(scrollable, bg=BG)
    frame.pack(fill=tk.X, pady=6, padx=8, anchor="e")
    bubble = tk.Label(
        frame,
        text=text,
        bg=USER_BUBBLE,
        fg=USER_TEXT,
        font=FONT,
        justify="left",
        wraplength=540,
        padx=12,
        pady=8,
    )
    bubble.pack(anchor="e")
    ts = timestamp or datetime.now().strftime("%H:%M")
    timestamp_label = tk.Label(
        frame, text=ts, bg=BG, fg="#8f9999", font=("Segoe UI", 8)
    )
    timestamp_label.pack(anchor="e", padx=(0, 6))
    make_right_click_copy(bubble, text)
    scroll_to_bottom()


def add_bot_bubble(text, timestamp=None):
    frame = tk.Frame(scrollable, bg=BG)
    frame.pack(fill=tk.X, pady=6, padx=8, anchor="w")
    bubble = tk.Label(
        frame,
        text=text,
        bg=BOT_BUBBLE,
        fg=BOT_TEXT,
        font=FONT,
        justify="left",
        wraplength=640,
        padx=12,
        pady=8,
    )
    bubble.pack(anchor="w")
    ts = timestamp or datetime.now().strftime("%H:%M")
    timestamp_label = tk.Label(
        frame, text=ts, bg=BG, fg="#8f9999", font=("Segoe UI", 8)
    )
    timestamp_label.pack(anchor="w", padx=(8, 0))
    make_right_click_copy(bubble, text)
    scroll_to_bottom()


def clear_chat_area():
    for w in scrollable.winfo_children():
        w.destroy()


# -------------- scrolling helper --------------
def scroll_to_bottom():
    # ensure UI updates then scroll to bottom
    root.update_idletasks()
    canvas.yview_moveto(1.0)


# -------------- typing animation --------------
typing_running = False


def start_typing_anim():
    global typing_running
    typing_running = True

    def anim():
        dots = 0
        while typing_running:
            dots = (dots + 1) % 4
            label = "CoreDev Assistant is typing" + ("." * dots)
            typing_label.config(text=label)
            threading.Event().wait(0.5)
        typing_label.config(text="")

    threading.Thread(target=anim, daemon=True).start()


def stop_typing_anim():
    global typing_running
    typing_running = False
    typing_label.config(text="")


# -------------- hybrid send / worker --------------
def handle_send():
    user_text = entry.get().strip()
    if not user_text:
        return
    entry.delete(0, tk.END)
    add_user_bubble(user_text)
    append_message("user", user_text)
    start_typing_anim()

    def worker():
        try:
            reply = get_response(user_text)
        except Exception as e:
            reply = "Something went wrong. Check console."
            print("get_response error:", e)
        append_message("bot", reply)
        root.after(10, lambda: add_bot_bubble(reply))
        root.after(10, stop_typing_anim)

    threading.Thread(target=worker, daemon=True).start()


# -------------- bindings and controls --------------
send_btn.config(command=handle_send)
entry.bind("<Return>", lambda e: handle_send())
new_btn.config(command=new_conversation)
save_btn.config(command=save_conversation)
restart_btn.config(
    command=lambda: (conversations.clear(), refresh_history(), new_conversation())
)

# -------------- history load/save --------------
if os.path.exists(HISTORY_PATH):
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            conversations = json.load(f)
        refresh_history()
        if conversations:
            load_conversation(0)
    except Exception as e:
        print("Failed to load history:", e)
        conversations = []
        new_conversation()
else:
    new_conversation()

# -------------- start --------------
root.mainloop()
