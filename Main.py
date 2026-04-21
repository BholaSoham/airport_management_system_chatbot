from nlp_brain import spacy_intent_extraction
from core_logic import handle_intent
from menu_system import menu_loop
from modules.crud_passengers import *

def chatbot():
    print(r"""
                
        __    __   _______     ___   .___________. __    __  
        |  |  |  | |   ____|   /   \  |           ||  |  |  | 
        |  |__|  | |  |__     /  ^  \ `---|  |----`|  |__|  | 
        |   __   | |   __|   /  /_\  \    |  |     |   __   | 
        |  |  |  | |  |____ /  _____  \   |  |     |  |  |  | 
        |__|  |__| |_______/__/     \__\  |__|     |__|  |__| 
                                                            

    """)
    print("\n🛫 Welcome to Heath — Your Airport Assistant Chatbot ✈️")
    print("------------------------------------------------------")
    print("💬 You can ask me to manage flights, passengers, security checks, and more.")
    print("🧠 You can type natural commands or simply say 'menu' to use the full feature list.")
    print("❌ Type 'exit' anytime to quit.")
    print("~ Built by Soham Bhola ")
    print("------------------------------------------------------\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit','quit','bye','goodbye']:
            print("Heath: Goodbye! Have a safe and happy journey ahead.")
            print("Thanks for using Heath ✈️")
            print("~ Built by Soham Bhola ")
            break
        if user_input.lower() == "menu":
            menu_loop()
            continue
        intent = spacy_intent_extraction(user_input)
        response = handle_intent(intent, user_input)
        print(f"Heath: {response}")

if __name__ == "__main__":
    chatbot()