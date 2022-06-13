///////////////////////
ctx.beginPath();
ctx.fillStyle = "rgb(200,0,0)";
ctx.fillRect (10, 10, 55, 50);
ctx.clearRect(45,45,60,60);
ctx.fill();
///////////////////////
const circle = new Path2D();
circle.arc(150, 75, 50, 0, 2 * Math.PI);
ctx.fillStyle = 'red';
ctx.fill(circle);

cvs.addEventListener('mousemove', function(event) {
  if (ctx.isPointInPath(circle, event.offsetX, event.offsetY)) {
    ctx.fillStyle = 'green';
  }
  else {
    ctx.fillStyle = 'red';
  }
  ctx.clearRect(0, 0, cvs.width, cvs.height);
  ctx.fill(circle);
});
///////////////////////
ctx.font="200px Verdana";
var gradient=ctx.createLinearGradient(0,0,cvs.width,0);
gradient.addColorStop("0","magenta");
gradient.addColorStop("0.5","blue");
gradient.addColorStop("1.0","red");
ctx.fillStyle=gradient;
ctx.fillText("click",100,900);