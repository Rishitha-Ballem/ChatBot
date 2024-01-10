import json
from difflib import get_close_matches
from typing import List

def load_knowledgebase(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
    except FileNotFoundError:
        data = {"questions": []}
    return data

def save_knowledgebase(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> str | None:
    matches: List = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def greet_user():
    print("Bot : Hello! I'm your friendly bot. Let's get to know each other.You can ask me basic questions and if i don't know the answer you can as well train me!")
    user_name = input("Bot : What's your name? ")
    return user_name

def ask_basic_questions(user_name):
    print(f"\nBot : Great to meet you, {user_name}!")
    print("Now, I'll ask you three basic questions.")

    question_1 = input("1. Where are you from? ")
    question_2 = input("2. What's your favorite hobby? ")
    question_3 = input("3. Any exciting plans for the day? ")

    return question_1, question_2, question_3

def print_user_introduction(user_name, answers):
    print(f"\nBot : Nice to learn more about you, {user_name}!")
    print(f"Here's a brief introduction:")
    print(f"- You are from {answers[0]}")
    print(f"- Your favorite hobby is {answers[1]}")
    print(f"- You have exciting plans for the day: {answers[2]}")

def handle_basic_questions(user_input, basic_questions, knowledge_base):
    response = get_answer_for_question(user_input, basic_questions)
    if response:
        return response
    else:
        # Check knowledge base for an answer
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            # If no match, prompt user for an answer and add to knowledge base
            print("Bot: I'm afraid I don't know the answer. Do you mind training me?")
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowledgebase('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I have learned a new response!')
                return new_answer

            return ""

def simple_bot():
    user_name = greet_user()
    answers = ask_basic_questions(user_name)
    print_user_introduction(user_name, answers)

    basic_questions = load_knowledgebase('basic_questions.json')
    knowledge_base = load_knowledgebase('knowledge_base.json')

    while True:
        user_input = input("\nBot : Ask me anything(EX. Name,Purpose etc), or type 'quit' or 'bye' to end: ")

        if user_input.lower() in ['quit', 'bye']:
            print("\nBot : Goodbye! It was nice chatting with you.")
            break
        else:
            # Handle basic questions from predefined set
            response = handle_basic_questions(user_input, basic_questions, knowledge_base)
            if response:
                print(f'Bot: {response}')
            
if __name__ == "__main__":
    simple_bot()
