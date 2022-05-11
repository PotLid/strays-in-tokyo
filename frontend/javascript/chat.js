// Handshake for the webSocket
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let wc_connection;

console.log('testing js')

// CLick on user_name => getting id (event listener to create element, and send message)




function onEnter(e) {
    if(e.code === 'Enter') {
        sendMessage();
    }
}

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function sendMessage() {
    const chatBox = document.getElementById("chat-comment");
    const comment = chatBox.value;
    chatBox.value = "";
    chatBox.focus();

    const payload = {'sender': 'username', 'messageType': 'user_to_server', 'id': unique_time_stamp  ,'comment': comment}
    if (comment !== "") {
        socket.send(JSON.stringify(payload));
    }
}

// Message Format for the chat
// <p className="message"> Hello </p>
// <p className="user_message"> What's up? </p>

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat-body');

    chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}

// // called when the page loads to get the chat_history
function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);

            console.log(messages)

            // for (const message of messages) {
            //     addMessage(message);
            // }
        }
    };
    request.open("GET", "/chat-history");
    request.send();
}


// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType

    // Need to add interaction over the web socket

    switch (messageType) {
        case 'server_to_user':
            addMessage(message);
            break;

        case 'like_update':
            //  Doing function that find message with corresponding id then update

            break;

        case 'dm':
            //  Manage the DM

            break;


        default:
            console.log("received an invalid WS messageType");
    }
}

function chat_init() {

    get_chat_history()

    // use this line to start your video without having to click a button. Helpful for debugging
    // startVideo();
}
