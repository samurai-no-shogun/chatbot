// Add event listener to the chat form
document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();
    sendMessage();
});

// Function to send user message and receive bot response
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const userMessage = messageInput.value.trim();

    if (userMessage !== '') {
        displayMessage(userMessage, 'user');
        messageInput.value = '';

        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response;
            displayMessage(botResponse, 'bot');
            if (botResponse.includes('Thank you for providing your information.')) {
                showLoadingMessage();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('Sorry, something went wrong. Please try again.', 'bot');
        });
    }
}

// Function to display a message in the chatbox
function displayMessage(message, sender) {
    const chatbox = document.getElementById('chatbox');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);
    messageElement.innerText = message;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Function to show the loading message
function showLoadingMessage() {
    document.querySelector('.loading-message').style.display = 'block';
}