var stageWidth = 1024;
var stageHeight = 768;
var update = true;


var colors = {
    background: createjs.Graphics.getRGB(32, 38, 35),
    hex_border: createjs.Graphics.getRGB(63, 159, 112),
    hex_fill: createjs.Graphics.getRGB(6, 59, 33),
    //hex_fill: createjs.Graphics.getRGB(59, 112, 86),
    //background: createjs.Graphics.getRGB(59, 143, 102)
}


var Hexagon = function(x, y, hex_radius){
    var radius = (hex_radius ? hex_radius : 50);
    var hexagon = new createjs.Shape();
    var fill_color = createjs.Graphics.getRGB(200, 200, 200);

    hexagon.graphics.setStrokeStyle(10, 'round');
    hexagon.graphics.beginStroke(colors.hex_border);

    hexagon.graphics.beginFill(colors.hex_fill);
    hexagon.graphics.drawPolyStar(0, 0, radius, 6, 0, -90);
    hexagon.x = x;
    hexagon.y = y;

    // attach handlers
    hexagon.onMouseOver = function(e){
        hex.point_end = new createjs.Point(e.target.x, e.target.y);
        update = true;
    }
    hexagon.onPress = function(e){
        hex.point_start = new createjs.Point(e.target.x, e.target.y);
        e.onMouseUp = function(ev){
            hex.point_start = null;
            hex.point_end = null;
        }
    }

    return hexagon;
}


var Arrow = function(x, y, rotation) {
    var arrow = new createjs.Shape();
    var size = 40;

    arrow.regX = size;
    arrow.regY = size * 2;

    var num_arrows = '';
    var coef = 0.75;
    var scaled_size = size;
    for (var i = 0; i < 5; i += 1) {
        var offset_x = size - scaled_size / 2;
        var offset_y = offset_x * 3 - size;
        arrow.graphics.moveTo(offset_x, offset_y);
        arrow.graphics.setStrokeStyle(scaled_size/7);
        arrow.graphics.beginStroke("#AAAAAA");
        arrow.graphics.lineTo(offset_x + scaled_size/2, offset_y - scaled_size/2);
        arrow.graphics.lineTo(offset_x + scaled_size, offset_y);
        arrow.graphics.endStroke();
        scaled_size = scaled_size * coef;
    }

    arrow.rotation = (rotation ? rotation : 0);
    arrow.x = x;
    arrow.y = y;
    return arrow;
}


var angleFromPoints = function(point_start, point_end){
    var a, b, c, angle;
    b = point_end.y - point_start.y;
    c = point_end.x - point_start.x;
    a = Math.sqrt(b*b + c*c);
    angle = Math.acos(b / a) * 180 / Math.PI;
    console.log(c);
    if (c > 0) {
        angle = 360 - angle;
    }
    angle += 180;
    console.log(angle);
    return angle;
}


/**
 * Hexagon game logic
 */
var hex = {
    stage: null,
    fpsLabel: null,
    hexagons: [],
    board: [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ],
    point_start: null,
    point_end: null,
    hexagon_radius : 50,
    hexagon_width : null
}

hex.init = function(){
    var stage;
    stage = new createjs.Stage(document.getElementById("canvas"));
    stage.enableMouseOver();
    hex.stage = stage;
    hex.drawBackground();
    hex.hexagon_width = hex.hexagon_radius * Math.sqrt(3);

    var offset_x = 100;
    var offset_y = 100;

    for (var y = 0; y < hex.board.length; y += 1) {
        for (var x = 0; x < hex.board[0].length; x += 1) {
            if (!hex.board[y][x]) continue;
            var pos_x = hex.hexagon_width * x + (y % 2) * hex.hexagon_width / 2;
            var pos_y = hex.hexagon_radius * 1.5 * y;
            var shape = Hexagon(offset_x + pos_x, offset_y + pos_y, hex.hexagon_radius);
            stage.addChild(shape);
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

hex.drawBackground = function(){
    // fill background
    var shape = new createjs.Shape();
    shape.graphics.beginFill(colors.background);
    shape.graphics.rect(0, 0, stageWidth, stageHeight);
    hex.stage.addChild(shape);
}

hex.showArrow = function(point_start, point_end){
    if(Math.abs(point_end.x - point_start.x) > hex.hexagon_width + 1)
        return;
    if(Math.abs(point_end.y - point_start.y) > hex.hexagon_width + 1)
        return;
    var rotation = angleFromPoints(point_start, point_end);
    var arrow = Arrow(point_start.x, point_start.y, rotation);
    hex.stage.addChild(arrow);
}

/*
hex.pressHandler = function(e){
    e.onMouseMove = function(ev){
        console.log(ev.stageX, ev.stageY);
        return;
        e.target.x = ev.stageX;
        e.target.y = ev.stageY;
        update = true;
    }
}
*/

hex.tick = function(){
    if (update){
        if (hex.point_start && hex.point_end){
            if (hex.point_start.x != hex.point_end.x || hex.point_start.y != hex.point_end.y){
                hex.showArrow(hex.point_start, hex.point_end);
            }
        }
        hex.fpsLabel.text = Math.round(createjs.Ticker.getMeasuredFPS()) + " fps";
        update = false;
        hex.stage.update(); 
    }
}
