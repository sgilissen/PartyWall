var host = window.location.hostname;
var port = window.location.port;
var preimages = [];
var socket = new WebSocket("ws://" + host + ":" + port + "/ws");

socket.onmessage = function(event) {
    addMsgToWall(event.data);
};

socket.onclose = function(event) {
    console.log("!!! CONNECTION CLOSED BY SERVER !!!")
};

socket.onerror = function(error) {
    console.log("!!! An error occured !!!")
};

function addMsgToWall(msg) {
    //<div class="msg"><p><span>-</span><br />Post een bericht door de QR-code te scannen!</p></div>
    var containerDiv = document.getElementById("messages");
    var msgDiv = document.createElement("div");
    msgDiv.setAttribute('class', 'msg');
    var p = document.createElement("p");
    var span = document.createElement("span");

    var d = new Date();
    var currentTime = ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) + ":" + ("0" + d.getSeconds()).slice(-2);
    span.appendChild(document.createTextNode(currentTime));
    p.appendChild(span);
    p.appendChild(document.createElement("br"))
    p.appendChild(document.createTextNode(msg));

    msgDiv.appendChild(p);



    containerDiv.appendChild(msgDiv);
    containerDiv.insertBefore(msgDiv, containerDiv.childNodes[0]);

    //msgDiv.appendChild(document.createTextNode(user + " - " + currentTime));
    //li.appendChild(document.createTextNode(command + " - " + payload));
    //li.appendChild(span);
    //containerDiv.appendChild(li);
    //containerDiv.insertBefore(li, ul.childNodes[0]);
    console.log("Received: " + msg);

}