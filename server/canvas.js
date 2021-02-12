window.addEventListener("load", () => {
    const canvas = _("#brushboard");
    const ctx = canvas.getContext("2d");

    let isDrawing = false;
    let resetCanvas = false;
    
    canvas.height = window.innerHeight;
    console.log(window.innerwidth)
    canvas.width = window.innerwidth;


    document.getElementById('reset-canvas').onclick = function() {
        resetCanvas = true;
    }

    window.addEventListener("resize", () => {
        canvas.height = window.innerHeight;
        canvas.width = window.innerwidth;
    })
    
    function _(selector){
        return document.querySelector(selector);
    }

    function draw(e){
        if (!isDrawing) return;
        color = _("#pen-color").value;
        ctx.beginPath();
        let x = e.clientX;
        let y = e.clientY;
        ctx.strokeStyle = color;
        ctx.lineWidth = parseInt(_("#open-size").value);
        ctx.shadowColor = color;
        ctx.lineCap = "round";
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    function doResetCanvas() {
        if (!resetCanvas) return;
        resetCanvas = false;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        console.log("Cleared Canvas");
    }

    window.addEventListener('mousedown', e=> {
        isDrawing = true;
        doResetCanvas();
    })

    window.addEventListener('mouseup', e=> {
        isDrawing = false;
    })

    window.addEventListener('mousemove', e=>{
        draw(e);
    })

    ctx.beginPath();
    ctx.moveTo(100,100);
    ctx.lineTo(200,100);
    ctx.stroke();
})
