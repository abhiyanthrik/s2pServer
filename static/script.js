// import {io} from "https://cdn.socket.io/4.7.2/socket.io.min.js"
let socket = io();
socket.on('connect', function(){
    console.log("Connected...!", socket.connected)
});

const video = document.querySelector("#videoElement");

video.width = 500;
video.height = 375;

function capture(video, scaleFactor) {
    if(scaleFactor == null){
        scaleFactor = 1;
    }
    let w = video.videoWidth * scaleFactor;
    let h = video.videoHeight * scaleFactor;
    let canvas = document.createElement('canvas');
    canvas.width  = w;
    canvas.height = h;
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, w, h);
    return canvas;
}

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (err0r) {
        console.log(err0r)
        console.log("Something went wrong!");
    });
}

const FPS = 50;

setInterval(() => {
    let type = "image/png";
    let frame = capture(video, 1);
    let data = frame.toDataURL(type);
    data = data.replace('data:' + type + ';base64,', ''); //split off junk
    socket.emit('image', data);
    console.log("Image Sent...");
}, 10000/FPS);


socket.on('response_back', function(image){
    const image_id = document.getElementById('image');
    image_id.src = image;
    console.log("Image Received...");
});
