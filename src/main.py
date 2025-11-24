from response import get_response


def main():
    print("\n🚀 Welcome to CoreDev Assistant (Terminal Version)")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() in ["exit", "quit"]:
            print("Bot: Goodbye! Have a productive coding day! 👋")
            break

        bot_response = get_response(user_msg)
        print(f"Bot: {bot_response}\n")


if __name__ == "__main__":
    main()
