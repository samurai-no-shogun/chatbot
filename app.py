from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the ChatOpenAI model with the appropriate API key and model
api_key = os.getenv("OPENAI_API_KEY")
chat_model = ChatOpenAI(model="gpt-4", openai_api_key=api_key)

def generate_bot_response(user_input):
    # Create a list of messages, starting with the human message
    messages = [HumanMessage(content=user_input)]
    
    # Generate a response from the ChatOpenAI model
    try:
        bot_response = chat_model(messages)
        bot_response_content = bot_response.content
    except Exception as e:
        # Handle any exceptions that may occur during the API call
        print(f"Error occurred while generating bot response: {e}")
        bot_response_content = "Sorry, I encountered an error while processing your request."
    
    # Add the bot's response to the list of messages
    messages.append(AIMessage(content=bot_response_content))
    
    return bot_response_content

@app.route('/')
def home():
    # Render the home page with the chat interface
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Get user input from the request
    data = request.get_json()
    user_input = data['message'].strip()
    
    # Guard clause for empty user input
    if not user_input:
        return jsonify({'response': ''})
    
    # Generate a response from the model
    bot_response = generate_bot_response(user_input)
    
    # Return the bot's response as JSON
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)