const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let prevX = null;
let prevY = null;
ctx.lineWidth = 5;

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

// Clear button logic
let clearBtn = document.querySelector(".clear");
clearBtn.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Save button logic
let saveBtn = document.querySelector(".save");
saveBtn.addEventListener("click", () => {
    let data = canvas.toDataURL("image/png");
    let a = document.createElement("a");
    a.href = data;
    a.download = "sketch.png";
    //TODO save png with white background
    a.click();
})

