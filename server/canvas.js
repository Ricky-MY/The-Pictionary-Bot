window.addEventListener("load", () => {
    function _(selector){
        return document.querySelector(selector);
    }


    const canvas = _("#brushboard");
    const ctx = canvas.getContext("2d");

    let isDrawing = false;
    let _new = true;
    
    console.log(window.innerWidth, window.innerHeight)
    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;

    canvas.addEventListener("resize", () => {
        let w = window.innerWidth;
        let h = window.innerHeight;

        var temp_cnvs = document.createElement('canvas');
        var temp_cntx = temp_cnvs.getContext('2d');

        temp_cnvs.width = w; 
        temp_cnvs.height = h;
        temp_cntx.fillStyle = rgba(128, 128, 128, 0.719);  // the original canvas's background color
        temp_cntx.fillRect(0, 0, w, h);
        temp_cntx.drawImage(canvas, 0, 0);

        console.log(w, h);
        canvas.height = w;
        canvas.width = h;
        ctx.drawImage(temp_cnvs, 0, 0);
        console.log(canvas.width, canvas.height)

    })

    function draw(e){
        if (!isDrawing) return;
        color = _("#pen-color").value;
        
        console.log(_new)
        if (_new) {
            ctx.beginPath();
            _new = false;
        }
        let x = e.clientX - canvas.offsetLeft;
        let y = e.clientY - canvas.offsetTop;
        ctx.strokeStyle = color;
        ctx.lineWidth = parseInt(_("#open-size").value);
        ctx.shadowColor = color;
        ctx.lineCap = "round";
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    function doResetCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        console.log("Cleared Canvas");
        ctx.beginPath()
    }

    function doShipFile() {
        if (!submit) return;
        submit = false;
        var dataURL = canvas.toDataURL();
        console.log(dataURL)
    }

    canvas.addEventListener('mousedown', e=> {
        isDrawing = true;
    })

    canvas.addEventListener('mouseup', e=> {
        isDrawing = false;
        _new = true;
    })

    canvas.addEventListener('mousemove', e=>{
        draw(e); 
    })

    ctx.beginPath();
    ctx.moveTo(100,100);
    ctx.lineTo(200,100);
    ctx.stroke();
})
