const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let prevX = null;
let prevY = null;
ctx.lineWidth = 6;

let draw = false;

// Adjust canvas size based on CSS properties
const computedStyle = getComputedStyle(canvas);
canvas.width = parseInt(computedStyle.width, 10);
canvas.height = parseInt(computedStyle.height, 10);

// Function to get mouse position relative to the canvas
function getMousePos(evt) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

canvas.addEventListener("mousedown", (e) => {
    const pos = getMousePos(e);
    prevX = pos.x;
    prevY = pos.y;
    draw = true;
});

canvas.addEventListener("mouseup", () => {
    draw = false;
});

canvas.addEventListener("mousemove", (e) => {
    if (!draw) return;
    const pos = getMousePos(e);
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    prevX = pos.x;
    prevY = pos.y;
});

// Add event listener for image upload
const imageLoader = document.getElementById('imageLoader');
imageLoader.addEventListener('change', handleImageUpload, false);

function handleImageUpload(e) {
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(e.target.files[0]);
}

// Color picker logic
let clrs = Array.from(document.querySelectorAll(".clr"));
clrs.forEach(clr => {
    clr.addEventListener("click", () => {
        ctx.strokeStyle = clr.dataset.clr;
    });
});

// Text input and type button elements
const textInput = document.getElementById('textInput');
const typeBtn = document.querySelector('.type');

let typingMode = false;

// Event listener for type button
typeBtn.addEventListener('click', () => {
    typingMode = !typingMode;
    if (typingMode) {
        textInput.style.display = 'block'; // Show text input
        textInput.focus(); // Automatically focus on the input
    } else {
        textInput.style.display = 'none'; // Hide text input
        drawTextOnCanvas(textInput.value); // Draw text on canvas
        textInput.value = ''; // Clear the text input
    }
});

// Function to draw text on canvas
function drawTextOnCanvas(text) {
    if (!text) return;

    ctx.font = '16px Arial'; // Adjust font as needed
    ctx.fillStyle = '#000'; // Adjust text color as needed
    ctx.fillText(text, 100, 100); // Adjust text position as needed
}

// Clear button logic
let clearBtn = document.querySelector(".clear");
clearBtn.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    textInput.value = '';
    textInput.style.display = 'none';
});

var sketch_counter = 0;

let saveBtn = document.querySelector(".save");
saveBtn.addEventListener("click", () => {

    if (textInput.style.display === 'block' && textInput.value.trim() !== '') {
        console.log(textInput.value);
        let res_test = 1;
        sendDataToFlask({ type: 'text', data: textInput.value })
        .then(() => {
            return processDataInFlask({ type: 'text', data: textInput.value });
            }
        );
        console.log(res_test);
    } else {

        let tempCanvas = document.createElement('canvas');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;

        let tempCtx = tempCanvas.getContext('2d');
        tempCtx.fillStyle = '#FFFFFF'; // Set fill color to white
        tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height); // Fill the canvas with white

        // Draw the current canvas content on top of the white background
        tempCtx.drawImage(canvas, 0, 0);
        // Save the image
        let data = tempCanvas.toDataURL("image/png");
        let a = document.createElement("a");
        a.href = data;
        a.download = "sketch.png";
        a.click();
        // Clean up: remove the temporary canvas
        tempCanvas.remove();

        let sketch_name = "";
        if (sketch_counter == 0) {
            sketch_name = "sketch.png";
        } else {
            sketch_name = "sketch " + "(" + sketch_counter + ").png";
        }
        sketch_counter += 1;

        sendDataToFlask({ type: 'text', data: sketch_name })
        .then(() => {
                return processDataInFlask({ type: 'text', data: sketch_name });
            }
        );
    }
    canvas.classList.add('canvas-flip');
    clearBtn.click();

});

function sendDataToFlask(text) {
    return fetch('/save_data', {
        method: 'POST',
        body: JSON.stringify({ text: text }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then((data)=> {
        console.log(data);
        return data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function processDataInFlask(text) {
    return fetch('/process_data', {
        method: 'POST',
        body: JSON.stringify({ text: text }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then((data)=> {
        console.log(data);
        // console.log(data.result);
        // console.log(typeof(data.result));
        // var resultObject = JSON.parse(data.result);
        // console.log(resultObject.events);
        // Process events
        if (data.events && data.links && data.events.length === data.links.length) {
            data.events.forEach((event, index) => {
                const eventElement = document.createElement('a');
                eventElement.href = data.links[index];
                eventElement.target = '_blank';
                eventElement.classList.add('ticket');
                eventElement.textContent = event;
                document.querySelector('.events').appendChild(eventElement);
            });
        }

        // Process notes
        if (data.notes) {
            data.notes.forEach(note => {
                const noteElement = document.createElement('div');
                noteElement.classList.add('ticket');
                noteElement.textContent = note;
                document.querySelector('.notes').appendChild(noteElement);
            });
        }

        return data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}