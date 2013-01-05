var halftone = {
    stage: null,
    stageWidth: 1800,
    stageHeight: 1600,
    image: null,
}


halftone.init = function(){
    halftone.stage = new createjs.Stage(document.getElementById("canvas"));

    halftone.draw_background();
    //halftone.draw_circles();
    halftone.draw_image();

    halftone.stage.update();
}


halftone.draw_background = function(){
    var shape = new createjs.Shape();
    shape.graphics.beginFill('000');
    shape.graphics.rect(0, 0, halftone.stageWidth, halftone.stageHeight);
    halftone.stage.addChild(shape);
}


halftone.draw_circles = function(){
    var shape = new createjs.Shape();
    shape.graphics.beginFill('FCDB00');

    var width = 50,
        height = 36,
        size = 10,
        offset = new createjs.Point(50, 88),
        grid = 12;
    for (var x = 0; x < width; x += 1) {
        for (var y = 0; y < height; y += 1) {
            var rand_size = Math.random() * size;
            shape.graphics.drawCircle(
                    offset.x + x*grid,
                    offset.y + y*grid,
                    rand_size
            );
        }
    }

    shape.rotation = -10;

    halftone.stage.addChild(shape);
}


halftone.load_image = function(){
    /*
    halftone.image = new Image();
    halftone.image.onload = halftone.draw_image;
    halftone.image.src = "dave.png";
    */
}


halftone.draw_image = function(){
    // extract image data
    var dave = $('canvas#dave'),
        img = $('img'),
        width = img.width(),
        height = img.height(),
        ctx = dave[0].getContext('2d');
    ctx.drawImage(img[0], 0, 0, width, height);
    var data = ctx.getImageData(0, 0, width, height);

    // draw circles
    var shape = new createjs.Shape();
    shape.graphics.beginFill('FCDB00');

    var size = 8,
        offset = new createjs.Point(-20, 100),
        source_grid = 1,
        grid = 8,
        treshhold = 3;

    for (var ygrid = 0; ygrid < data.height; ygrid+=source_grid) {
        for (var xgrid = 0; xgrid < data.width; xgrid+=source_grid) {
            // acquare the grid values
            var mid_avg = 0;
            for (var y = 0; y < source_grid; y += 1) {
                for (var x = 0; x < source_grid; x += 1) {
                    var i = ((ygrid+y) * 4) * data.width + (xgrid+x) * 4;
                    var avg = (data.data[i] + data.data[i + 1] + data.data[i + 2]) / 3;
                    data.data[i] = avg;
                    data.data[i + 1] = avg;
                    data.data[i + 2] = avg;
                    mid_avg += avg;
                }
            }
            var n = size * mid_avg / (source_grid*source_grid*256);
            if (n > treshhold) {
                shape.graphics.drawCircle( offset.x + xgrid*grid, offset.y + ygrid*grid, n);
            }
        }
    }

    shape.rotation = -10;

    halftone.stage.addChild(shape);

    ctx.putImageData(data, 0, 0);

    /*
    bmp = new createjs.Bitmap(halftone.image);
    bmp.regX = halftone.image.width >> 1;
    bmp.regY = halftone.image.height >> 1;
    bmp.x = bmp.regX;
    bmp.y = bmp.regY;
    halftone.stage.addChild(bmp);
    halftone.stage.update();
    */
}
