function Clock(id, start, end, countDown=false) {

    function timeDiff(c, countDown=false) {
        var now = Date();
        var f = (Date.parse(now) - Date.parse(c)) / 1000;
        if (countDown) {
            f = (Date.parse(c) - Date.parse(now)) / 1000;
        }
        var g = Math.floor(f / (3600 * 24));
        f = f % (3600 * 24);
        var b = Math.floor(f / 3600);
        if (b < 10) {
            b = "0" + b
        }
        f = f % 3600;
        var d = Math.floor(f / 60);
        if (d < 10) {
            d = "0" + d
        }
        f = f % 60;
        if (f < 10) {
            f = "0" + f
        }
        return {days: g, hours: b, minutes: d, seconds: f}
    }
    
    function updateHTML(id, time) {
        var val = '<span class="digit">' + time.days + '</span> 天 '
            + '<span class="digit">' + time.hours + '</span> 时 '
            + '<span class="digit">' + time.minutes + '</span> 分 '
            + '<span class="digit">' + time.seconds + '</span> 秒';
        var element = document.getElementById(id)
        element.innerHTML = val
    }

    function setDiff(id, target, countDown) {
        var diff = timeDiff(target, countDown);
        updateHTML(id, diff);
    }
    
    var target = start
    if (countDown) {
        target = end
    }

    setDiff(id, target, countDown);
    setInterval(function () {
        setDiff(id, target, countDown);
    }, 500);
}