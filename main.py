import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

history = []


def get_response(user_input):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)
    return response.text


def game():
    is_question_relevant = True
    while is_question_relevant:
        question_topic = input("What topic would you like a quiz on? ")
        relevant_question = get_response(f"is {question_topic} a relevant and okay topic for a quiz? Answer yes or no on a dictionary")

        data2 = json.loads(relevant_question)

        if data2['answer'] == 'yes':
            is_question_relevant = False
            running = True
            while running:
                try:

                    no_of_questions = int(input("How many questions would you like? 5, 10, 15 or 20? "))
                    if no_of_questions in (5, 10, 15, 20):

                        print(f"Here are your {no_of_questions} questions!")
                        question = f"give me {no_of_questions}  questions concerning {question_topic}, include the letters A,B,C or D in front of the options, and the answer i.e A,B,C OR D"
                        response_text = get_response(question)

                        # Safely load JSON data
                        try:
                            data = json.loads(response_text)
                            # print(data)
                        except json.JSONDecodeError:
                            print("Error: Response is not in valid JSON format.")
                            return

                        if 'questions' not in data:
                            print("Try again")
                            return

                        score = 0
                        for i in range(int(no_of_questions)):
                            while True:
                                question_text = data['questions'][i]['question']
                                options = data['questions'][i]['options']
                                correct_answer = data['questions'][i]['answer']

                                # Present question and capture answer
                                answer_input = input(f"{i + 1}. {question_text}\n{options}\nAnswer with either A, B, C, or D: ")
                                answer = answer_input.strip().upper()

                                if answer in ('A', 'B', 'C', 'D'):
                                    if answer == correct_answer:
                                        score += 1
                                    break
                                else:
                                    print("Please select A, B, C, or D.")

                        print(f"Congrats, you've completed the quiz! You scored {score}/{no_of_questions}.")
                        running = False

                except ValueError:
                    print("Invalid input. Please enter a number (5, 10, 15, or 20).")

        else:
            print("Pleae enter a valid topic")


# Main game loop
print("Welcome to the quiz chatbot!")

game()
while True:
    play_again = input("Would you like to play again? (Yes or No): ")
    if play_again.strip().lower() == "no":
        print("Thanks for playing!")
        break
    elif play_again.strip().lower() == "yes":
        game()
    else:
        print("Please choose Yes or No.")
