var stageWidth = 1024;
var stageHeight = 768;
var stage;
var update = true;


var Hexagon = function(x, y, hex_radius){
    var radius = (hex_radius ? hex_radius : 50);
    var hexagon = new createjs.Shape();
    var border_color = createjs.Graphics.getRGB(0, 0, 0);
    var fill_color = createjs.Graphics.getRGB(200, 200, 200);

    hexagon.graphics.setStrokeStyle(10, 'round');
    hexagon.graphics.beginStroke(border_color);

    hexagon.graphics.beginFill(fill_color);
    hexagon.graphics.drawPolyStar(0, 0, radius, 6, 0, -90);
    hexagon.x = x;
    hexagon.y = y;
    return hexagon;
}


var hex = {
    fpsLabel: null,
    hexagons: [],
    board: [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
}

hex.init = function(){
    //new stage
    stage = new createjs.Stage(document.getElementById("canvas"));
    stage.enableMouseOver();

    var hexagon_radius = 50;
    var hexagon_width = hexagon_radius * Math.sqrt(3);
    var offset_x = 100;
    var offset_y = 100;

    for (var y = 0; y < hex.board.length; y += 1) {
        for (var x = 0; x < hex.board[0].length; x += 1) {
            if (!hex.board[y][x]) continue;
            var pos_x = hexagon_width * x + (y % 2) * hexagon_width / 2;
            var pos_y = hexagon_radius * 1.5 * y;
            var shape = Hexagon(offset_x + pos_x, offset_y + pos_y, hexagon_radius);
            stage.addChild(shape);
            //shape.onPress = hex.pressHandler;
            hex.hexagons.push(shape);
        }
    }

    // fpsLabel
    hex.fpsLabel = new createjs.Text("-- fps", "bold 18px Arial", "#000");
    stage.addChild(hex.fpsLabel);
    hex.fpsLabel.x = 10;
    hex.fpsLabel.y = 20;

    //draw to the canvas
    stage.update(); 
    createjs.Ticker.addListener(hex);
    createjs.Ticker.setFPS(50); 
}

hex.pressHandler = function(e){
    e.onMouseMove = function(ev){
        e.target.x = ev.stageX;
        e.target.y = ev.stageY;
        update = true;
    }
}

hex.tick = function(){
    if(update){
        hex.fpsLabel.text = Math.round(createjs.Ticker.getMeasuredFPS()) + " fps";
        update = false;
        stage.update(); 
    }
}
