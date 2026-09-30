
from config import client, MODEL, QUESTIONS, banner

def main():
    banner("SYSTEM 1 - BASIC CHATBOT")

    for question in QUESTIONS:
        print("\nYou:", question)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful college assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content
        print("Bot:", answer)

if __name__ == "__main__":
    main()