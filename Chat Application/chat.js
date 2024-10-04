// Connect to the WebSocket server
const socket = new WebSocket('ws://localhost:8000');

const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

// Display incoming messages in the chat window
socket.onmessage = function(event) {
    const message = document.createElement('div');
    message.classList.add('message');
    message.textContent = event.data;
    chatBox.appendChild(message);

    // Auto scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
};

// Send a message to the server when the button is clicked
sendBtn.onclick = function() {
    const message = messageInput.value;

    if (message.trim() !== "") {
        socket.send(message);
        messageInput.value = '';  // Clear the input field after sending
    }
};

// Send message by pressing the Enter key
messageInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendBtn.click();
    }
});
