import os
from openai import OpenAI
from chatbot1.src.response import FAQRetriever

# Initialize the new OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class HybridChatbot:
    def __init__(self, faq_file):
        self.retriever = FAQRetriever(faq_file)

    def get_response(self, user_input):
        # 1. Check FAQ first
        answer = self.retriever.get_answer(user_input)
        if answer:
            return answer

        # 2. If no FAQ match, call OpenAI Responses API (new)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"Answer this question clearly: {user_input}",
            max_output_tokens=150,
        )

        return response.output_text


def main():
    faq_file = os.path.join(os.path.dirname(__file__), "../data/faqs.json")
    faq_file = os.path.abspath(faq_file)

    bot = HybridChatbot(faq_file)
    print("Hybrid FAQ Chatbot (type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = bot.get_response(user_input)
        print("Bot:", response)


if __name__ == "__main__":
    main()
