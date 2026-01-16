#This file will handle everything from user input, it will parse the input, classify it, and fix prompt to be better for querying the model


def get_user_prompt():
    prompt = input("What can I help you with today?: ")
    return prompt


