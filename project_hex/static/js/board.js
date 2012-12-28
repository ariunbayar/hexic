hexEnv.Board = atom.Class({
    Extends: LibCanvas.Scene.Element,

    Implements: LibCanvas.Behaviors.MouseListener,

    hexagons: null,
    cellSize: 1,
    startPoint: new Point(0, 0),
    currentShift: null,
    z: 0,

    /** @constructs */
    initialize: function(scene, cfg) {
        this.parent(scene, cfg);

        this.cellSize = cfg.cellSize;
        this.hexagons = [];
        this.startPoint = this.shape.from;
        this.z = cfg.z;

        this.setChildrenFactory(hexEnv.Hexagon)
            .createHexagons()
            .listenMouse();
    },

    createHexagons: function(){
        this.hexagons.empty();

        /*
        this.createBoard(6, 0, 0);
        this.createBoard(18, 0, 0);

        this.createBoard(0, 0, 10);
        this.createBoard(12, 0, 10);
        this.createBoard(24, 0, 10);

        this.createBoard(6, 0, 20);
        this.createBoard(18, 0, 20);
        */
        this.createBoard(0, 0, this.z);

        return this;
    },

    createBoard: function(sx, sy, sz){
        var point, x, y, x1, y1,
            width = hexEnv.Hexagon.hex[1][0],
            height = hexEnv.Hexagon.hex[2][1];

        for (y = sy + 0; y < sy + 10; y++) {
            for (x = sx + 0; x < sx + 10; x++) {
                if (Math.random() < 0.2) continue;
                x1 = x * width + (y % 2) * width / 2;
                y1 = y * height;

                var hex = this.createChild({
                    from: new Point(x1 + this.startPoint.x, y1 + this.startPoint.y),
                    p: new LibCanvas.Point3D(x1 + this.startPoint.x, y1 + this.startPoint.y, sz),
                    size: this.cellSize,
                    zIndex: sz,
                });
                hex.clickable(hex.redraw);
                this.hexagons.push();
            }
        }
    },

    clearPrevious: function () {},

    shift: function (point){
        point = Point(arguments);
        this.currentShift.move(point);
        this.hexagons.invoke('move', point);
        return this;
    },

    renderTo: function(ctx){
        ctx.stroke(this.shape.clone().snapToPixel(), 'red');
    },
});


