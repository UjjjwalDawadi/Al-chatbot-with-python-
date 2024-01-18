import json
from Functions import load_knowledge_base, save_knowledge_base, update_knowledge_base

def train_chatbot():
    knowledge_base = load_knowledge_base()

    print("Chatbot Training: Type 'bye' to finish training.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'bye':
            print("Training completed. Goodbye!")
            break

        new_response = input("Chatbot: What's the appropriate response for that?  \n")
        update_knowledge_base(knowledge_base, user_input, new_response)

    # Save the updated knowledge base
    save_knowledge_base(knowledge_base)

if __name__ == "__main__":
    train_chatbot()
