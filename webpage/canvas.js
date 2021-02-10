let canvas = document.querySelector('#canvas');

// Resizing of the canvas window
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Context is used to change things on the canvas
let ctx = canvas.getContext('2d');