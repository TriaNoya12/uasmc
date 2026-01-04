const chatBody = document.getElementById("chat-body");
const input = document.getElementById("user-input");

input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function getTime() {
    const now = new Date();
    return now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = "message " + sender;

    msg.innerHTML = `
        <div class="avatar">${sender === "bot" ? "🤖" : "🙂"}</div>
        <div>
            <div class="bubble">${text}</div>
            <div class="time">${getTime()}</div>
        </div>
    `;

    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.reply, "bot");
    });
}
