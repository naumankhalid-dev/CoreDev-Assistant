from response import get_response


def start_terminal_chat():
    print("\n🚀 Welcome to CoreDev Assistant (Terminal Version)")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        user_input = input("You: ")

        # Exit logic
        if user_input.lower() in ["exit", "quit", "close", "bye"]:
            print("Bot: Goodbye! Happy coding! 🚀")
            break

        # Generate response
        bot_reply = get_response(user_input)
        print(f"Bot: {bot_reply}\n")


if __name__ == "__main__":
    start_terminal_chat()
