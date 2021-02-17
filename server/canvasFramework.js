export default class DrawableCanvas {
    COLORS = {
        RED:"#f44336",
        YELLOW:"#ffeb3b",
        BLUE:"#304ffe",
        GREEN:"#00897b",
        ORANGE:"#ff5722"
    }

    canvas = document.getElementById('brushboard');
    ctx = this.canvas.getContext("2d");

    w = this.canvas.width;
    h = this.canvas.height;

    flag = false;
    prevX = 0;
    currX = 0;
    prevY = 0;
    currY = 0;

    dot_flag = false;

    x = this.COLORS.RED; 
    y = 4;

    
    constructor(){

        this.canvas.addEventListener("mousemove", (e) =>
            this.findxy('move', e)
        , false);
        this.canvas.addEventListener("mousedown", (e) =>
            this.findxy('down', e)
        , false);
        this.canvas.addEventListener("mouseup", (e) =>
            this.findxy('up', e)
        , false);
        this.canvas.addEventListener("mouseout", (e) => 
            this.findxy('out', e)
        , false);

        this.canvas.addEventListener("touchmove", (e) =>
            this.findxy('touchmove', e)
        , false);
        this.canvas.addEventListener("touchstart", (e) =>
            this.findxy('touchstart', e)
        , false);
        this.canvas.addEventListener("touchend", (e) =>
            this.findxy('touchend', e)
        , false);
        this.canvas.addEventListener("touchcancel", (e) => 
            this.findxy('touchcancel', e)
        , false);

        this.reSize();
    }

    reSize(){
        this.canvas.width  = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        this.w = this.canvas.width;
        this.h = this.canvas.height;
    }

    findxy=(res, e)=> {
        
        if (res == 'down') {
            this.prevX = this.currX;
            this.prevY = this.currY;
            this.currX = e.clientX - this.canvas.offsetLeft;
            this.currY = e.clientY - this.canvas.offsetTop;
            
    
            this.flag = true;
            this.dot_flag = true;
            if (this.dot_flag) {
                this.ctx.beginPath();
                this.ctx.fillStyle = this.x;
                this.ctx.fillRect(this.currX, this.currY, 2, 2);
                this.ctx.closePath();
                this.dot_flag = false;
            }
        }
        if (res == 'up' || res == "out") {
            this.flag = false;
        }
        if (res == 'move') {
            if (this.flag) {
                this.prevX = this.currX;
                this.prevY = this.currY;
                this.currX = e.clientX - this.canvas.offsetLeft;
                this.currY = e.clientY - this.canvas.offsetTop;
                this.draw();
            }
        }

        if (res == 'touchstart') {
            this.prevX = this.currX;
            this.prevY = this.currY;
            this.currX = e.touches[0].clientX - this.canvas.offsetLeft;
            this.currY = e.touches[0].clientY - this.canvas.offsetTop;
    
            this.flag = true;
            this.dot_flag = true;
            if (this.dot_flag) {
                this.ctx.beginPath();
                this.ctx.fillStyle = this.x;
                this.ctx.fillRect(this.currX, this.currY, 2, 2);
                this.ctx.closePath();
                this.dot_flag = false;
            }
        }
        if (res == 'touchend' || res == "touchcancel") {
            this.flag = false;
        }
        if (res == 'touchmove') {
            if (this.flag) {
                this.prevX = this.currX;
                this.prevY = this.currY;
                this.currX = e.touches[0].clientX - this.canvas.offsetLeft;
                this.currY = e.touches[0].clientY - this.canvas.offsetTop;
                this.draw();
            }
        }

        
        
    }

    draw() {
        this.ctx.beginPath();
        this.ctx.moveTo(this.prevX, this.prevY);
        this.ctx.lineTo(this.currX, this.currY);
        this.ctx.strokeStyle = this.x;
        this.ctx.lineWidth = this.y;
        this.ctx.stroke();
        this.ctx.closePath();
    }

    erase() {
        this.ctx.clearRect(0, 0, this.w, this.h);
        this.ctx.globalCompositeOperation = "source-over";
        
    }

    save() {
        document.getElementById("canvasimg").style.border = "2px solid";
        var dataURL = canvas.toDataURL();
        document.getElementById("canvasimg").src = dataURL;
        document.getElementById("canvasimg").style.display = "inline";
    }

    color(obj) {
        switch (obj) {
            case 1:
                this.ctx.globalCompositeOperation = "source-over";
                this.x = this.COLORS.RED;
                this.y=4;
                break;
            case 2:
                this.ctx.globalCompositeOperation = "source-over";
                this.x = this.COLORS.YELLOW;
                this.y=4;
                break;
            case 3:
                this.ctx.globalCompositeOperation = "source-over";
                this.x = this.COLORS.BLUE;
                this.y=4;
                break;
            case 4:
                this.ctx.globalCompositeOperation = "source-over";
                this.x = this.COLORS.GREEN;
                this.y=4;
                break;
            case 5:
                this.ctx.globalCompositeOperation = "source-over";
                this.x = this.COLORS.ORANGE;
                this.y=4;
                break;
            case 6:
                this.ctx.globalCompositeOperation = "destination-out";
                break;
            case 7:
                this.erase()
                break;

                
            
        }

       

    
    }


}