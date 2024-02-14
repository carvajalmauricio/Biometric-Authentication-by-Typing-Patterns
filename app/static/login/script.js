const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

let keysPressed = [];

document.addEventListener('keydown', function(event) {
    if (!keysPressed.some(item => item.key === event.key && item.type === 'keydown')) {
        keysPressed.push({ key: event.key, timeStamp: Date.now(), type: 'keydown' });
    }
});

document.addEventListener('keyup', function(event) {
    keysPressed.push({ key: event.key, timeStamp: Date.now(), type: 'keyup' });
});

function startCapturing() {
    keysPressed = [];
    document.addEventListener('keydown', captureKey);
    document.addEventListener('keyup', releaseKey);
}

function stopCapturing() {
    document.removeEventListener('keydown', captureKey);
    document.removeEventListener('keyup', releaseKey);
}

function captureKey(event) {
    let key = event.key;
    let timeStamp = Date.now();
    keysPressed.push({key: key, timeStamp: timeStamp});
}

function releaseKey(event) {
    let key = event.key;
    let timeStamp = Date.now();
    keysPressed.forEach(function(item, index) {
        if (item.key === key) {
            item.timeStamp = timeStamp;
        }
    });
}

function sendData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        }
    };
    xhttp.open("POST", "/getdata", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(keysPressed));
}


