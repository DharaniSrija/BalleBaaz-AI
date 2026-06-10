'use strict';

/* DOM */
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const chipRow = document.getElementById('chip-row');

/* Greeting Time */
const initTime = document.getElementById('init-time');

function now() {
    return new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}

if (initTime) {
    initTime.textContent = now();
}

/* Scroll */
function scrollDown() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* Loading */
function setLoading(flag) {
    sendBtn.disabled = flag;
    userInput.disabled = flag;
}

/* Hide Chips */
function hideChips() {
    if (!chipRow) return;

    chipRow.style.opacity = '0';
    chipRow.style.maxHeight = '0';
    chipRow.style.overflow = 'hidden';
}

/* User Message */
function addUserMessage(text) {

    const wrapper = document.createElement('div');
    wrapper.className = 'user-message';

    wrapper.innerHTML = `
        <div class="bubble-wrap">
            <div class="bubble">${text}</div>
            <span class="msg-time">${now()}</span>
        </div>
    `;

    chatBox.appendChild(wrapper);
    scrollDown();
}

/* Bot Message */
function addBotMessage(text) {

    const wrapper = document.createElement('div');
    wrapper.className = 'bot-message';

    wrapper.innerHTML = `
        <div class="avatar-sm">🏏</div>

        <div class="bubble-wrap">
            <div class="bubble">${text}</div>
            <span class="msg-time">${now()}</span>
        </div>
    `;

    chatBox.appendChild(wrapper);
    scrollDown();
}

/* Typing */
function showTyping() {

    const typing = document.createElement('div');

    typing.className = 'bot-message';
    typing.id = 'typing-indicator';

    typing.innerHTML = `
        <div class="avatar-sm">🏏</div>

        <div class="bubble-wrap">
            <div class="bubble">
                Typing...
            </div>
        </div>
    `;

    chatBox.appendChild(typing);
    scrollDown();
}

function removeTyping() {

    const typing = document.getElementById('typing-indicator');

    if (typing) {
        typing.remove();
    }
}

/* Send Message */
async function sendMessage(customMessage = null) {

    const message = (
        customMessage ||
        userInput.value
    ).trim();

    if (!message) return;

    addUserMessage(message);

    userInput.value = '';

    hideChips();

    setLoading(true);

    showTyping();

    try {

        const response = await fetch('/chat', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        console.log("SERVER RESPONSE:", data);

        removeTyping();

        addBotMessage(
            data.answer ||
            "Sorry, I could not find that information in the BalleBaaz Arena knowledge base."
        );

    } catch (error) {

        console.error(error);

        removeTyping();

        addBotMessage(
            "⚠️ Server connection failed."
        );

    } finally {

        setLoading(false);

        userInput.focus();

        scrollDown();
    }
}

/* Send Button */
sendBtn.addEventListener('click', () => {
    sendMessage();
});

/* Enter Key */
userInput.addEventListener('keydown', (e) => {

    if (e.key === 'Enter') {

        e.preventDefault();

        sendMessage();
    }
});

/* Chips */
document.querySelectorAll('.chip').forEach(chip => {

    chip.addEventListener('click', () => {

        sendMessage(
            chip.dataset.msg
        );

    });

});