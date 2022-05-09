// Handshake for the webSocket
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

let wc_connection;

console.log('testing js')

// CLick on user_name => getting id (event listener to create element, and send message)



//
// function onEnter(e) {
//     if(e.code === 'Enter') {
//         sendMessage();
//     }
// }
//
// // Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
// function sendMessage() {
//     const chatBox = document.getElementById("chat-comment");
//     const comment = chatBox.value;
//     chatBox.value = "";
//     chatBox.focus();
//     if (comment !== "") {
//         socket.send(JSON.stringify({'messageType': 'chatMessage', 'comment': comment}));
//     }
// }
//
// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}

// // called when the page loads to get the chat_history
function get_chat_history() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessage(message);
            }
        }
    };
    request.open("GET", "/chat-history");
    request.send();
}
//
//
// // Called whenever data is received from the server over the WebSocket connection
// socket.onmessage = function (ws_message) {
//     const message = JSON.parse(ws_message.data);
//     const messageType = message.messageType
//
//     switch (messageType) {
//         case 'chatMessage':
//             addMessage(message);
//             break;
//         case 'webRTC-offer':
//             webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
//             webRTCConnection.createAnswer().then(answer => {
//                 webRTCConnection.setLocalDescription(answer);
//                 socket.send(JSON.stringify({'messageType': 'webRTC-answer', 'answer': answer}));
//             });
//             break;
//         case 'webRTC-answer':
//             webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
//             break;
//         case 'webRTC-candidate':
//             webRTCConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
//             break;
//         default:
//             console.log("received an invalid WS messageType");
//     }
// }
//
// function startVideo() {
//     const constraints = {video: true, audio: true};
//     navigator.mediaDevices.getUserMedia(constraints).then((myStream) => {
//         const elem = document.getElementById("myVideo");
//         elem.srcObject = myStream;
//
//         // Use Google's public STUN server
//         const iceConfig = {
//             'iceServers': [{'url': 'stun:stun2.1.google.com:19302'}]
//         };
//
//         // create a WebRTC connection object
//         webRTCConnection = new RTCPeerConnection(iceConfig);
//
//         // add your local stream to the connection
//         webRTCConnection.addStream(myStream);
//
//         // when a remote stream is added, display it on the page
//         webRTCConnection.onaddstream = function (data) {
//             const remoteVideo = document.getElementById('otherVideo');
//             remoteVideo.srcObject = data.stream;
//         };
//
//         // called when an ice candidate needs to be sent to the peer
//         webRTCConnection.onicecandidate = function (data) {
//             socket.send(JSON.stringify({'messageType': 'webRTC-candidate', 'candidate': data.candidate}));
//         };
//     })
// }
//
//
// function connectWebRTC() {
//     // create and send an offer
//     webRTCConnection.createOffer().then(webRTCOffer => {
//         socket.send(JSON.stringify({'messageType': 'webRTC-offer', 'offer': webRTCOffer}));
//         webRTCConnection.setLocalDescription(webRTCOffer);
//     });
//
// }
//
function chat_init() {

    get_chat_history()

    // use this line to start your video without having to click a button. Helpful for debugging
    // startVideo();
}
