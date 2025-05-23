var canvas = document.querySelector("#canvas");
var context = canvas.getContext("2d");
(function() {
    canvas.width = 280;
    canvas.height = 280;
    var Mouse = {x:0, y:0};
    var lastMouse = {x:0, y:0};
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.color = "black";
    context.lineWidth = 20;
    context.lineJoin = context.lineCap = 'round';

    canvas.addEventListener("mousemove", function(e) {
        lastMouse.x = Mouse.x;
        lastMouse.y = Mouse.y;
        // Mouse.x = e.pageX - this.offsetLeft-120;
        // Mouse.y = e.pageY - this.offsetTop-280;
        var rect = canvas.getBoundingClientRect();
        Mouse.x = e.clientX - rect.left;
        Mouse.y = e.clientY - rect.top;
        console.log(Mouse.x + "," + Mouse.y + "," + rect.left + "," + rect.top)}, false);


        canvas.addEventListener("mousedown", function(e) {
            canvas.addEventListener("mousemove", onPaint, false);
        }, false);
        canvas.addEventListener("mouseup", function() {
            canvas.removeEventListener("mousemove", onPaint, false);
        }, false);

        var onPaint = function() {
            context.lineWidth = context.lineWidth;
            context.lineJoin = "round";
            context.lineCap = "round";
            context.strokeStyle = context.color;

            context.beginPath();
            context.moveTo(lastMouse.x, lastMouse.y);
            context.lineTo(Mouse.x,Mouse.y );
            context.closePath();
            context.stroke();
        };
}());


$("#clearButton").on("click", function() {
    context.clearRect( 0, 0, 280, 280 );
    context.fillStyle="white";
    context.fillRect(0,0,canvas.width,canvas.height);
});

$("#predictButton").click(function(){
    $('#result').text(' Predicting...');
    var img = canvas.toDataURL('image/png');
    $.ajax({
        type: "POST",
        url: "https://dlwebappca2-ilzj.onrender.com/predict",
        data: img,
        success: function(data){
            $('#result').text('Predicted Output: ' + data);
        }
    });
});
