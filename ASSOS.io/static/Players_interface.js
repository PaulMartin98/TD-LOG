// function drawing the life of the player in function of the radius of his ball
function drawLife(rayon){
  // h,v the x,y coordinates of the center of the life bar
  var h = 100;
  var v = 100;
  // radius of the life bar
  var r = 50;
  var diff;
  var arrondi;
  // % of the life in function of the radius of the ball
  var vie = (rayon/15)*100;
  // % of the life lost
  diff = (vie/100)*Math.PI*2;

  // drawing a withe circle for the background
  players_ctx.beginPath();
  players_ctx.arc(v,h,r,0,2*Math.PI,false);  // cercle blanc intérieur
  players_ctx.fillStyle='#FFF';
  players_ctx.fill();
  players_ctx.closePath();

  // drawing the green arc representing the life of the player
  players_ctx.beginPath();  // arc vert
  players_ctx.lineWidth = 15;
  players_ctx.strokeStyle = "#b3cf3c";
  players_ctx.arc(v,h,r,-Math.PI/2,-Math.PI/2+diff,false);
  players_ctx.stroke();
  players_ctx.closePath();

  // drawing the red arc representing the life lost
  players_ctx.beginPath();  // arc rouge
  players_ctx.strokeStyle = "#ea1f1f";
  players_ctx.arc(v,h,r,diff-Math.PI/2,3*Math.PI/2,false);
  players_ctx.stroke();
  players_ctx.closePath();

  // writing the % of the life in the middle of the life bar
  players_ctx.beginPath();
  players_ctx.fillStyle='#000';   // texte intérieur
  players_ctx.textAlign='center';
  players_ctx.font = '10pt Verdana'
  arrondi = Math.round(100*vie)/100;
  players_ctx.fillText(arrondi+'%',h+2,v+6);
  players_ctx.closePath();
}

// function drawing the ennemies positions on the minimap, (x,y) ennemy position, (w,h) position of the top left corner of the minimap
function drawPixel(x,y,w,h){
  // calculating the position on the minimap in function of the compressing rate of the minimap ( here 159/1327)
  var x_p = w + x*159/1327;
  var y_p = h + y*159/1327;

  // drawing the pixel
  players_ctx.beginPath();
  players_ctx.fillStyle = "#FF0000"
  players_ctx.arc(x_p,y_p,3,0,2*Math.PI);
  players_ctx.fill();
  players_ctx.closePath();
}

// drawing the minimap
function drawMiniMap(){
  //(x,y) position of the top left corner of the minimap
  var x = players_canvas.width-270;
  var y = players_canvas.height-170;

  // chargin the image
  var img = new Image();
  img.src = "img_mini.png";
  // width and height  of the picture of the minimap
  var w = 248;
  var h = 159;

  // drawing a white rectangle for the background
  players_ctx.beginPath();
  players_ctx.fillStyle = "#FFF";
  players_ctx.fillRect(x,y,w,h);
  players_ctx.closePath();

  // drawing a border for the minimap
  players_ctx.beginPath();
  players_ctx.strokeStyle = "#d35400";
  players_ctx.lineWidth = 3;
  players_ctx.rect(x,y,w,h);
  players_ctx.stroke();
  players_ctx.closePath();

  // charging the minimap by its id defined in client.html
  var img = document.getElementById("source");
  players_ctx.drawImage(img,x,y);

  // drawing the position of the player ( function as drawPixel but in a different color)
  var x_p = x + personalX*159/1327;
  var y_p = y + personalY*159/1327;
  players_ctx.beginPath();
  players_ctx.fillStyle = "#01DF01";
  players_ctx.arc(x_p,y_p,3,0,2*Math.PI,false);
  players_ctx.fill();
  players_ctx.closePath();

  // drawing the ennemies posiitons
  for (var id_players in client_players){
    if (id_players != id){
      drawPixel(client_players[id_players]["x"],client_players[id_players]["y"],x,y);
    }
  }
}

//function writing the pseudo of the players near their ball, (x,y) position of the ennemy on the canvas
function drawPseudo(pseudo,x,y)
{
  players_ctx.beginPath();
  players_ctx.font = "20px Arial";
  players_ctx.fillStyle = "#da6210";
  players_ctx.fillText(pseudo,x,y);
  players_ctx.closePath();

}

//function writing the 3 best scores
function drawScore()
{
  // (x,y) positon on the canvas
  var x = 50;
  var y = players_canvas.height-100;
  // defining a table of existing id
  var id_best_score = [id,id,id];

  // calculating the 3 best score and updating the table id_best_score which contains the id of the 3 best players
  for (var idp in client_players)
  {
    if(client_players[idp]["score"]>client_players[id_best_score[0]]["score"]){
      id_best_score[2] = id_best_score[1];
      id_best_score[1] = id_best_score[0];
      id_best_score[0] = idp;
    }
    else if(client_players[idp]["score"]>client_players[id_best_score[1]]["score"]){
      id_best_score[2] = id_best_score[1];
      id_best_score[1] = idp;
    }
    else if(client_players[idp]["score"]>client_players[id_best_score[2]]["score"]){
      id_best_score[2] = idp;
    }
  }

  // writing a title
  players_ctx.beginPath();
  players_ctx.font = "30px Arial";
  players_ctx.fillStyle = "#0040FF";
  players_ctx.fillText("Best Players:",x+50,y-40);
  players_ctx.closePath();

  // writing the best scores
  for (var idp in id_best_score)
  {
    //score of the player
    var sc = client_players[id_best_score[idp]]["score"];
    // string we want to write
    var s = client_players[id_best_score[idp]]["pseudo"] +" : " + sc.toString();

    // wrting the score on the canvas
    players_ctx.beginPath();
    players_ctx.font = "20px Arial";
    players_ctx.fillStyle = "#da6210";
    players_ctx.fillText(s,x,y);
    players_ctx.closePath();
    //updating the position where the score is written
    y = y + 30;
  }
}
