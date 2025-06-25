import os
from openai import OpenAI
from config import api_key  # Make sure this is your actual API key

# Initialize the client
client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))

def generate_response(prompt_style, user_input):
    """Handle all OpenAI requests with current API"""
    styles = {
        "1": ("2nd Grade Summary", 
              "Rephrase this for a second grader in simple language:"),
        "2": ("TLDR", 
              "Create a very short summary (tl;dr):"),
        "3": ("One-Line Summary", 
              "Summarize this in one sentence:")
    }
    
    if prompt_style not in styles:
        return None
        
    title, instruction = styles[prompt_style]
    print(f"\nYou have chosen {title}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful text simplifier."},
                {"role": "user", "content": f"{instruction}\n\n{user_input}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return None

def main():
    print("What would you like to dumbify?")
    user_input = input("> ")
    
    print("\nChoose a simplification style:")
    print("1. 2nd Grade Summary")
    print("2. TLDR")
    print("3. One-Line Summary")
    
    choice = input("Enter your choice (1-3): ")
    
    result = generate_response(choice, user_input)
    if result:
        print("\nSimplified Result:")
        print(result)
    else:
        print("Invalid choice or error occurred")

if __name__ == "__main__":
    main()