const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
    console.log("WebSocket connection established");
};

socket.onmessage = (event) => {
    console.log("Message from server:", event.data);
    document.getElementById("output").innerText = event.data;
};

socket.onclose = () => {
    console.log("WebSocket connection closed");
};

function sendMessage() {
    const message = document.getElementById("messageInput").value;
    socket.send(message);
}
