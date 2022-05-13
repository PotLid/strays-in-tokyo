// Handshake for the webSocket
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

socket.addEventListener('open', e => {
    socket.send(JSON.stringify({'messageType': 'user_handshake', username: encodeCookie()['username']}))
})

let username;
let targetUser = null;
let wc_connection;

// console.log('testing js')

function encodeCookie() {
    return document.cookie.split(';').reduce((obj, cookieLine) => {
        const [key, value] = cookieLine.split('=');
        return {
            ...obj,
            [key?.trim()]: value?.trim()
        }
    }, {})
}

// CLick on user_name => getting id (event listener to create element, and send message)

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        sendMessage();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function sendMessage() {
    const xsrf = document.getElementById('id-xsrf');
    const chatBox = document.getElementById("input-chat");
    const comment = chatBox.value;
    // const username = username;
    const id = username + '-' + new Date().toUTCString()

    chatBox.value = "";
    chatBox.focus();

    // const payload = {'sender': username, 'messageType': 'user_to_server', 'id': id  ,'comment': comment, 'xsrf': xsrf.value}
    const payload = {'sender': username, 'messageType': 'user_to_server', 'id': id  ,'comment': comment}

    if (comment !== "") {
        socket.send(JSON.stringify(payload));
    }
}

// {'messageType': 'like', 'id': unique_time_stamp }
function sendLike(e) {

    // console.log(e.target.nextSibling)

    // console.log(e.target.parentNode.parentElement)
    const xsrf = document.getElementById('id-xsrf');

    const targetId = e.target.parentNode.parentNode.getAttribute('id-chat');

    // const payload = {'messageType': 'like', 'id': targetId, 'xsrf': xsrf.value};
    const payload = {'messageType': 'like', 'id': targetId};

    // console.log(payload)

    socket.send(JSON.stringify(payload));
    // console.log('clicked like!')
}

function updateLike(message) {
    const targetId = message['id'];

    // console.log(targetId)

    const targetEl = document.getElementById(`count-${targetId}`);

    targetEl.innerText = `${message['totalLike']}`;
}

function directMsg(el) {
    const temp_targetUser = el.getAttribute('data-target');

    if(temp_targetUser === username) {
        alert('You can not DM yourself!')
        return;
    }

    targetUser = temp_targetUser;

    const body = document.body;
    const new_section = document.createElement('section');
    new_section.id = 'dm-section'
    new_section.className = 'dm-section'
    // new_section.style.height = '100%';
    // new_section.style.width = '100%';
    // new_section.style.top = '0';
    // new_section.style.left = '0';
    // new_section.style.position = 'fixed';
    // new_section.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';

    // dm wrap div
    const dm_wrap = document.createElement('div');
    dm_wrap.className = 'dm-wrap'

    // dm heading
    const dm_head = document.createElement('h2');
    dm_head.style.color = 'white';
    dm_head.innerText = 'To: ' + targetUser;

    // dm wrap text box
    const dm_input = document.createElement('input');
    dm_input.type = 'text';
    dm_input.id = 'dm-input'

    // dm send button
    const dm_send = document.createElement('button');
    dm_send.innerText = 'Send'
    dm_send.addEventListener('click', sendDirectMsg)

    // dm close button
    const dm_close = document.createElement('button');
    dm_close.innerText = 'Close'
    dm_close.addEventListener('click', closeDirectPrompt);

    dm_wrap.appendChild(dm_head)
    dm_wrap.appendChild(dm_input)
    dm_wrap.appendChild(dm_send)
    dm_wrap.appendChild(dm_close)

    new_section.appendChild(dm_wrap);

    body.appendChild(new_section);


    // const payload = {'sender': username, 'receiver': targetUser, 'messageType': 'dm', 'commend': commend }
}

function sendDirectMsg(el) {
    const input = document.getElementById('dm-input');
    const xsrf = document.getElementById('id-xsrf');

    // const payload = {'sender': username, 'receiver': targetUser, 'messageType': 'dm', 'comment': input.value, 'totalLike': 0, 'id': `DM-${new Date().toUTCString()}`, 'xsrf': xsrf.value }
    const payload = {'sender': username, 'receiver': targetUser, 'messageType': 'dm', 'comment': input.value, 'totalLike': 0, 'id': `DM-${new Date().toUTCString()}` }

    // console.log(payload)

    socket.send(JSON.stringify(payload));

    input.value = ''

    // need to add message log here
//    or nah just close
//
    closeDirectPrompt();

}

function closeDirectPrompt(el) {

    targetUser = null;

    document.getElementById('dm-section').remove();

}

function replyDirectMsg(message) {
    const input = document.getElementById('dm-input');
    const xsrf = document.getElementById('id-xsrf');

    // const payload = {'sender': message['receiver'], 'receiver': message['sender'], 'messageType': 'dm', 'comment': input.value, 'totalLike': 0, 'id': `DM-${new Date().toUTCString()}`, 'xsrf': xsrf.value }
    const payload = {'sender': message['receiver'], 'receiver': message['sender'], 'messageType': 'dm', 'comment': input.value, 'totalLike': 0, 'id': `DM-${new Date().toUTCString()}`}

    socket.send(JSON.stringify(payload));

    input.value = ''

    closeDirectPrompt();
}

function gotDirectMsg(message) {
    const body = document.body;
    const new_section = document.createElement('section');
    new_section.id = 'dm-section'
    new_section.className = 'dm-section'

    // dm wrap div
    const dm_wrap = document.createElement('div');
    dm_wrap.className = 'dm-wrap'

    // dm heading
    const dm_head = document.createElement('h2');
    dm_head.style.color = 'white';
    dm_head.innerText = 'From: ' + message['sender'];

    // dm text
    const dm_text = document.createElement('p');
    dm_text.style.color = 'white';
    dm_text.innerText = message['comment']

    // dm wrap text box
    const dm_input = document.createElement('input');
    dm_input.type = 'text';
    dm_input.id = 'dm-input'

    // dm send button
    const dm_send = document.createElement('button');
    dm_send.innerText = 'Reply'
    dm_send.addEventListener('click', () => replyDirectMsg(message))

    // dm close button
    const dm_close = document.createElement('button');
    dm_close.innerText = 'Close'
    dm_close.addEventListener('click', closeDirectPrompt);

    dm_wrap.appendChild(dm_head)
    dm_wrap.appendChild(dm_text)
    dm_wrap.appendChild(dm_input)
    dm_wrap.appendChild(dm_send)
    dm_wrap.appendChild(dm_close)

    new_section.appendChild(dm_wrap);

    body.appendChild(new_section);
}


// Message Format for the chat
// <p className="message"> Hello </p>
// <p className="user_message"> What's up? </p>

// Renders a new chat message to the page
function addMessage(chatMessage) {
    // console.log(chatMessage)
    const chat = document.getElementById('chat-body');

    const chatNode = document.createElement('p');
    chatNode.className = chatMessage['sender'] === username ? 'user_message' : 'message';
    chatNode.innerText = chatMessage['comment'];
    chatNode.setAttribute('id-chat', chatMessage['id']);
    chatNode.setAttribute('like', '0');

    const likeWrap = document.createElement('span');
    likeWrap.className = 'like-wrap'

    const button = document.createElement('button');
    button.innerText = 'like'
    button.addEventListener('click', sendLike)
    const likeTotal = document.createElement('p');
    likeTotal.setAttribute('id', `count-${chatMessage['id']}`);
    likeTotal.innerText = `${chatMessage['totalLike'] ? chatMessage['totalLike'] : '0'}`
    likeWrap.appendChild(button)
    likeWrap.appendChild(likeTotal)

    chatNode.appendChild(likeWrap)

    chat.appendChild(chatNode)
    //
    // chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}

// // called when the page loads to get the chat_history
function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);

            // console.log(messages)

            for (const message of messages) {
                addMessage(message);
            }
        }
    };
    request.open("GET", "/chat-history");
    request.send();
}

function getUserList() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const users = JSON.parse(this.response);

            console.log(users)

            for (const user of users) {
                addUser(user)
            }
        }
    };
    request.open("GET", "/loggedUsers");
    request.send();
}

function addUser(message) {
    const userList = document.getElementById('ul-users');

    const button = document.createElement('button');
    button.id = `u-${message['username']}`;
    button.className = 'buttonuser';
    button.setAttribute('data-target', message['username']);
    button.addEventListener('click', e => directMsg(e.target));

    const img = document.createElement('img');
    img.src = `/frontend/static/${message['profile_picture']}`
    img.id = 'kitty'

    button.appendChild(img)
    button.innerText = message['username'];

    userList.appendChild(button);

}

function removeUser(message) {
    document.getElementById(`u-${message['username']}`).remove();
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
            updateLike(message)

            break;

        case 'dm':
            //  Manage the DM
            gotDirectMsg(message)

            break;

        case 'user_connect':
            addUser(message)

            break;

        case 'user_disconnect':
            removeUser(message)

            break;


        default:
            console.log("received an invalid WS messageType");
    }
}

function chat_init() {
    username = encodeCookie()['username'];

    get_chat_history()

    getUserList();

    // const result = encodeCookie();
    //
    // console.log(result)

    // use this line to start your video without having to click a button. Helpful for debugging
    // startVideo();
}
