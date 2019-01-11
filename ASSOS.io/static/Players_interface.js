function drawLife(rayon){
  var h = 100;
  var v = 100;
  var r = 50;
  var diff;
  var arrondi;
  var vie = (rayon/15)*100;
  diff = (vie/100)*Math.PI*2;
  players_ctx.beginPath();
  players_ctx.arc(v,h,r,0,2*Math.PI,false);  // cercle blanc intérieur
  players_ctx.fillStyle='#FFF';
  players_ctx.fill();
  players_ctx.closePath();

  players_ctx.beginPath();  // arc vert
  players_ctx.lineWidth = 15;
  players_ctx.strokeStyle = "#b3cf3c";
  players_ctx.arc(v,h,r,-Math.PI/2,-Math.PI/2+diff,false);
  players_ctx.stroke();
  players_ctx.closePath();

  players_ctx.beginPath();  // arc rouge
  players_ctx.strokeStyle = "#ea1f1f";
  players_ctx.arc(v,h,r,diff-Math.PI/2,3*Math.PI/2,false);
  players_ctx.stroke();
  players_ctx.closePath();

  players_ctx.fillStyle='#000';   // texte intérieur
  players_ctx.textAlign='center';
  players_ctx.font = '10pt Verdana'
  arrondi = Math.round(100*vie)/100;
  players_ctx.fillText(arrondi+'%',h+2,v+6);
}

function drawMiniMap(){
  var x = 50;
  var y = 200;
  var img = new Image();
  img.src = "img_mini.png";
  var w = 248;
  var h = 159;
  players_ctx.beginPath();
  players_ctx.fillStyle = "#FFF";
  players_ctx.fillRect(x,y,w,h);
  players_ctx.closePath();

  players_ctx.beginPath();
  players_ctx.strokeStyle = "#d35400";
  players_ctx.lineWidth = 3;
  players_ctx.rect(x,y,w,h);
  players_ctx.stroke();
  players_ctx.closePath();

  //var img = document.getElementById("{{ url_for('static', filename='img_mini.png') }}");
  //players_ctx.drawImage(img,x,y)
  //players_ctx.beginPath();
  //im.onload = function(){
  //var img = new Image();   // Crée un nouvel élément Image
  //img.src = "/static/img_mini.png"; // Définit le chemin vers sa source
  //players_ctx.drawImage(img,x,y);
  //}
  //players_ctx.closePath();
}
