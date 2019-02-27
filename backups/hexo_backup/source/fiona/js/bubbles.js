/**
 * Refer to:    https://github.com/ndroi/JSDrawLove
 * Modified by: https://github.com/luuil
 *              luuil@outlook.com
 */

// draw heart in different sizes and colors
function Love(w, h, context) {
    var me = this;
    function rand() {
        me.max_scale = (Math.random() * 3.2 + 1.2) * w / 521;
        me.cur_scale = 1.2 * w / 521;

        me.x = Math.floor(Math.random() * w - 40);
        me.y = Math.floor(h - Math.random() * 200);

        // limit rgb range to generate more PINK hearts:
        //    r[200,255], g[30,200], b[100, 255]
        // how to generate random number within range [min, max]:
        //    Math.floor(Math.random()*(max-min+1)+min)
        me.rgb_R = Math.floor(Math.random() * (255 - 200 + 1) + 200);
        me.rgb_G = Math.floor(Math.random() * (200 - 30 + 1) + 30);
        me.rgb_B = Math.floor(Math.random() * (255 - 100 + 1) + 100);
        me.alpha = Math.random() * 0.2 + 0.8;

        me.vector = Math.random() * 5 + 0.4;
    }
    (function() {
        rand();
    }());
    me.drawHeart = function() {
        if (me.alpha < 0.01)
            rand();
        if (me.cur_scale < me.max_scale)
            me.cur_scale += 0.3;
        x = me.x;
        y = me.y;
        scale = me.cur_scale;
        context.fillStyle = "rgba(" + me.rgb_R + "," + me.rgb_G + "," + me.rgb_B + "," + me.alpha + ")";
        context.shadowBlur = 10;
        context.shadowColor = "rgb(" + me.rgb_R + "," + me.rgb_G + "," + me.rgb_B + ")";
        context.beginPath();
        context.bezierCurveTo(x + 2.5 * scale, y + 2.5 * scale, x + 2.0 * scale, y, x, y);
        context.bezierCurveTo(x - 3.0 * scale, y, x - 3.0 * scale, y + 3.5 * scale, x - 3.0 * scale, y + 3.5 * scale);
        context.bezierCurveTo(x - 3.0 * scale, y + 5.5 * scale, x - 1.0 * scale, y + 7.7 * scale, x + 2.5 * scale, y + 9.5 * scale);
        context.bezierCurveTo(x + 6.0 * scale, y + 7.7 * scale, x + 8.0 * scale, y + 5.5 * scale, x + 8.0 * scale, y + 3.5 * scale);
        context.bezierCurveTo(x + 8.0 * scale, y + 3.5 * scale, x + 8.0 * scale, y, x + 5.0 * scale, y);
        context.bezierCurveTo(x + 3.5 * scale, y, x + 2.5 * scale, y + 2.5 * scale, x + 2.5 * scale, y + 2.5 * scale);
        context.fill();
        context.closePath();
        me.y -= me.vector;
        me.alpha -= (me.vector / 2.9 * 3.5 / h);
    }
}

function HeartBubbles(id) {
    // get window size
    const WIDTH = window.innerWidth;
    const HEIGHT = window.innerHeight;

    var canvas = document.getElementById(id);
    canvas.setAttribute("width", WIDTH);
    canvas.setAttribute("height", HEIGHT);
    var context = canvas.getContext("2d");

    // generate heart bubbles
    var heartBubbles = {
        loves: [],
        DURATION: 30,
        begin: function() {
            this.createLove();
        },
        createLove: function() {
            for (var i = 0; i < WIDTH / 77; i++) {
                var love = new Love(WIDTH, HEIGHT, context);
                this.loves.push(love);
            }
            setInterval(this.drawLove.bind(this), this.DURATION);
        },
        drawLove: function() {
            context.clearRect(0, 0, WIDTH, HEIGHT);
            for (var key in this.loves) {
                this.loves[key].drawHeart();
            }
        }
    }
    
    // start animation
    window.onload = function() {
        heartBubbles.begin();
    }
}


