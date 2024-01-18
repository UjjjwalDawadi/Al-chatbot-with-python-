import json
import random
import re

def load_patterns():
    with open('Patterns.json', 'r') as file:
        patterns = json.load(file)
    return patterns

def load_knowledge_base():
    try:
        with open('KnowledgeBase.json', 'r') as file:
            knowledge_base = json.load(file)
        return knowledge_base
    except FileNotFoundError:
        return {}

def save_knowledge_base(knowledge_base):
    with open('KnowledgeBase.json', 'w') as file:
        json.dump(knowledge_base, file, indent=2)

def update_knowledge_base(knowledge_base, user_input, new_response):
    user_input_lower = user_input.lower()
    knowledge_base[user_input_lower] = new_response

    # Update or initialize the user interactions list
    user_interactions = knowledge_base.get("_user_interactions", [])
    user_interactions.append({"input": user_input_lower, "response": new_response})
    knowledge_base["_user_interactions"] = user_interactions

    # Save the updated knowledge base
    save_knowledge_base(knowledge_base)

def get_chatbot_response(user_input, patterns, knowledge_base):
    user_input_lower = user_input.lower()

    # Check the knowledge base for a predefined response
    if user_input_lower in knowledge_base:
        return knowledge_base[user_input_lower]

    # Check if the user input is a single word and not in the patterns
    if len(user_input.split()) == 1 and user_input_lower not in [word.lower() for pattern_set in patterns for word in pattern_set["pattern"]]:
        return "I'm not sure how to respond. Could you provide more context or ask a question?"

    # Check if any two or more words from patterns match the user input
    matching_patterns = [pattern_set for pattern_set in patterns if any(re.search(r'\b' + re.escape(word.lower()) + r'\b', user_input_lower) for word in pattern_set["pattern"])]
    if len(matching_patterns) >= 2:
        # If multiple patterns match, ask for more detailed context
        return "It seems multiple patterns match your input. Could you provide more details or be more specific?"

    for pattern_set in matching_patterns:
        responses_list = pattern_set["responses"]

        # If any word from the pattern matches, return a random response
        return random.choice(responses_list)

    # If no suitable response, ask the user to provide another question
    return "I couldn't find a response. Can you ask another question or provide more context?"

def main():
    patterns = load_patterns()
    knowledge_base = load_knowledge_base()

    print("Chatbot: Hi! I'm your chatbot. Type 'bye' to exit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye!")
            break

        chatbot_response = get_chatbot_response(user_input, patterns, knowledge_base)
        
        if chatbot_response.startswith("I couldn't find a response."):
            print(f"Chatbot: {chatbot_response}")
        else:
            print("Chatbot:", chatbot_response)


