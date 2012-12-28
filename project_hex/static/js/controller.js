hexEnv.Controller = atom.Class({
    app: null,
    back_scene: null,
    front_scene: null,
    /** board position indexed boards */
    boards: {},
    /** current board index as in this.boards */
    current_board: null,
    /** front layer object */
    front: null,

    getDisplayWidth: function(){
        var hex = hexEnv.Hexagon.hexagon;
            width = hex.size.x * hexEnv.Hexagon.scale;
        return width * (5 + 1 + 10 + 1 + 5);
    },

    getDisplayHeight: function(){
        var hex = hexEnv.Hexagon.hexagon;
            height = hex.size.y * hexEnv.Hexagon.scale;
        return height * (5 + 1 + 10 + 1 + 5);
    },

    /**
     * @constructs
     * @param {string} el - link to dom element
     */
    initialize: function (el) {
        this.app = new LibCanvas.App('canvas', {
            width: this.getDisplayWidth(),
            height: this.getDisplayHeight(),
            mouse: true,
        });
        this.back_scene = this.app.createScene('back', {intersection: 'manual'});
        this.front_scene = this.app.createScene('front', {intersection: 'manual'});
        this.start();

        /*
        this.libcanvas = new LibCanvas(el, { name: 'main', })
            .listenMouse()
            .size({width: 640, height: 480}, true)
            .start();
        this.start();
        this.libcanvas.update();
        */
    },

    initBoards: function(boards) {
        boards.forEach(function(id){
            this.boards[id] = new hexEnv.Board(this.back_scene, this.mouseDown);
        }, this);
    },

    getRelativeBoard: function (id, y, x) {
        // y_x
        var pos = id.split('_'),
            _x = parseInt(pos[1]) + x,
            _y = parseInt(pos[0]) + y,
            new_id = _y + '_' + _x;
        if (new_id in this.boards)
            return this.boards[new_id];
        else
            return false;
    },

    /**
     * Draws boards with current_board centered.
     */
    draw: function(){
        var board,
            id = this.current_board,
            arr = [[-1, -1, -5, -5], [-1, 0, -5, 6], [-1, 1, -5, 17], // follows y_x
                   [ 0, -1, 6, -5], [ 0, 0, 6, 6], [ 0, 1, 6, 17],
                   [ 1, -1, 17, -5], [ 1, 0, 17, 6], [ 1, 1, 17, 17]];
        arr.forEach(function(pos){
            board = this.getRelativeBoard(id, pos[0], pos[1]);
            if (board) board.draw(new Point(pos[2], pos[3]));
        }, this);
    },

    drawFront: function(){
        var params = {shape: this.app.rectangle, controller: this};
        this.front = new hexEnv.Front(this.front_scene, params);
    },

    addShadow: function (colors, shadow) {
        if (shadow == 1) return colors;

        var c = atom.clone(colors);
        for (key in c) {
            if ('r' in c[key]) { // is color
                c[key].r = Math.round(c[key].r * shadow);
                c[key].g = Math.round(c[key].g * shadow);
                c[key].b = Math.round(c[key].b * shadow);
            }else{
                this.addShadow(c[key], shadow);
            }
        }
        return c;
    },

    createHexagon: function (layer, boardX, boardY) {
        var points = [], shaper, scale, colors, x, y,
            size = this.self.hexSize;

        scale = (layer.name == 'current' ? 1 : 0.7);
        offsetX = size.x * boardX + (boardY % 2 ? size.x / 2 : 0);
        offsetY = size.y * boardY;
        colors = this.addShadow(this.colors, scale);
        for (var i=0; i<this.self.hex.length; i++) {
            x = (this.self.hex[i][0] + offsetX);
            y = (this.self.hex[i][1] + offsetY);
            points.push(new Point(x, y).mul(this.self.cellSize * scale));
        }
        shaper = layer.createShaper({
            shape: new Polygon(points),
            stroke: colors.stroke.toString(),
            fill: colors.fill.toString(),
            lineWidth: 4 * scale,
            hover: {stroke: colors.hover.stroke.toString(),
                    fill: colors.hover.fill.toString()},
            active: {stroke: colors.active.stroke.toString(),
                     fill: colors.active.fill.toString()},
        });
        shaper.listenMouse().clickable();
        return shaper;
    },

    startControlLayer: function () {
        var shaper,
            layer = this.libcanvas;

        shaper = layer.createShaper({
            shape: new Circle(50, 300, 15),
            fill: "#fff",
        });
        shaper.origPos = shaper.shape.center.clone();
        shaper
            .listenMouse()
            .clickable()
            .draggable(this.dragging)
            .addEvent('stopDrag', this.draggingStop);
        layer.zIndex = 2;
    },

    startCurrentLayer: function () {
        var layer = this.libcanvas.createLayer('current', 1);

        for (var x=10; x--;) {
            for (var y=10; y--;)
                if (Math.random() > 0.5)
                    this.createHexagon(layer, x, y);
        }
    },

    startBackLayer: function () {
        var layer = this.libcanvas.createLayer('back', 0);

        for (var x=10; x--;) {
            for (var y=10; y--;)
                if (Math.random() > 0.5)
                    this.createHexagon(layer, x, y);
        }
        this.shiftElements(layer, new Point(130, 80));
    },

    setColors: function () {
        this.colors = {
            stroke: new Color('lime'),
            fill: new Color('green'),
            hover: {stroke: new Color('yellow'),
                    fill: new Color('olive')},
            active: {stroke: new Color('red'),
                     fill: new Color('maroon')},
        };
        return this.colors;
    },

    shiftElements: function (layer, offset) {
        var elems = layer.elems,
            i = elems.length;
        while (i--) {
            el = elems[i];
            el.shape.move(offset);
        }
    },

    dragging: function (offset) {  // relative to mover shape
        var currentOffset = offset.clone().mul(8),
            backOffset = offset.clone().mul(4),
            current_layer = this.libcanvas.layer('current'),
            back_layer = this.libcanvas.layer('back'),
            i;

        var shiftElements = function (layer, offset) {
            var elems = layer.elems,
                i = elems.length;
            while (i--) {
                el = elems[i];
                el.shape.move(offset);
            }
        }
        shiftElements(current_layer, currentOffset);
        shiftElements(back_layer, backOffset);
    },

    draggingStop: function (e) {  // relative to mover shape
        this.shape.x = this.origPos.x;
        this.shape.y = this.origPos.y;
    },

    /** @private */
    start: function(){
        var boards = [
            '0_0', '0_1', '0_2',
            '1_0', '1_1', '1_2',
            '2_0', '2_1', '2_2',
        ];
        this.initBoards(boards);
        this.current_board = '1_1';
        this.drawFront();
        this.draw();
        return;

        this.setColors();
        this.startControlLayer();
        this.startCurrentLayer();
        this.startBackLayer();
    },

    mouseDown: function(e) {
        hex.front.setOriginCell(this);
    },

    processMove: function(cell, direction){
        console.log(cell, direction);
    },
});


hexEnv.Front = atom.Class({
    Extends: LibCanvas.Scene.Element,
    Implements: [Clickable],

    Static: {
        move_arrow: [[0, -10], [5, 0], [0, 10], [10, 0]],
    },

    move_arrows: null,
    cell_from: null,
    move_angle: 0,

    initialize: function (scene, options){
        this.parent(scene, options);
        this.clickable(this.redraw);
        this.listenMouse();
        this.addEvent('mouseup', this.mouseUp);
        this.addEvent('mousemove', this.mouseMove);
        this.addEvent(['mouseup', 'mousemove', 'mousedown'], function(e){e.fall()});
    },

    setOriginCell: function(cell){
        var points = [];
        this.cell_from = cell;
        this.move_arrows = [];

        this.self.move_arrow.forEach(function(p){
            var point = new Point(p[0], p[1]);
            point.move(cell.shape.center);
            points.push(point);
        }, this);
        shape = new Polygon(points);
        for (var i=0; i<3; i++) {
            this.move_arrows.push(shape.clone().move([i*4, 0]));
        }
    },


    renderTo: function(ctx){
        ctx.fill(this.options.shape, "rgba(0, 0, 0, 0)");

        if (this.cell_from) {
            this.move_arrows.forEach(function(shape){
                var shape1 = shape.clone();
                ctx.fill(shape1.rotate(this.move_angle, this.cell_from.shape.center), "#fff");
            }, this);
        }
    },

    getController: function(){
        return this.options.controller;
    },

    mouseUp: function(e){
        if (this.cell_from == null) return;

        // topleft 1, topright 2, right 3, bottomright 4, bottomleft 5, left 6
        var direction = Math.round((this.move_angle + Math.PI) * 3 / Math.PI);
        this.getController().processMove(this.cell_from, direction || 6);
        this.cell_from = null;
    },

    mouseMove: function(e){
        if (this.cell_from) {
            var angle,
                from = this.cell_from.shape.center,
                to = e.offset;

            angle = getAngle(from.x, from.y, to.x, to.y);
            angle = normalizeAngle(angle);
            if (angle == this.move_angle)
                return;  // Don't do anything until arrow changes
            else
                this.move_angle = angle;

            this.redraw();
        }
    },
});


hexEnv.Board = atom.Class({
    cells: {},

    initialize: function(scene, mouseDown) {
        this.scene = scene;
        this.mouseDown = mouseDown;
    },

    /** 
     * @param {Point} offset - board offset
     */
    draw: function (offset) {
        // sample
        var x, y, cell, color, joins;
        for (y=0; y<10; y++) {
            for (x=0; x<10; x++) {
                //if (Math.random() > 0.5) continue;

                joins = [
                    (y - 1) + '_' + (x - 1),
                    (y - 1) + '_' + x,
                    (y - 1) + '_' + (x + 1),
                    y + '_' + (x - 1),
                ];
                follow_adj = Math.random() > 0.1;
                if (joins[0] in this.cells && follow_adj) {
                    color = this.cells[joins[0]].color;
                }else if (joins[1] in this.cells && follow_adj) {
                    color = this.cells[joins[1]].color;
                }else if (joins[2] in this.cells && follow_adj) {
                    color = this.cells[joins[2]].color;
                }else if (joins[3] in this.cells && follow_adj) {
                    color = this.cells[joins[3]].color;
                }else{
                    color = new Color('green').self.random();
                }
                cell = new hexEnv.Hexagon(this.scene, {
                    pos: new Point(x, y),
                    offset: offset,
                    bridge: Math.random() > 0.9 ? 'out' : false,
                    count: (x + y / 10) * 100 + 1,
                    color: color,
                });
                cell.addEvent('mousedown', this.mouseDown);
                this.cells[y+'_'+x] = cell;
            }
        }
    },

    mouseDown: function(e){
        console.log('cell mousedown');
        return;
        var cell = this;
        var shape = Animatable(cell.shape);
        shape.animate({
            props: {},
            time: 50,
            onFinish: function(prevAnim){
                cell.count = Math.ceil(cell.count * 1.1);
                cell.redraw();
                if (cell.count > 1000000) {
                    cell.count = 1000000;
                    return;
                }
                shape.animate({
                    props: {},
                    time: 1,
                    onFinish: prevAnim.repeat,
                });
            },
        });
    },
});


hexEnv.Hexagon = atom.Class({
    Extends: LibCanvas.Scene.Element,
    Implements: [Clickable],
    Static: {
        border: {
            width: 2,
            color: 'rgba(255, 255, 255, 0.5)',
        },
        textStyle: {
            lineWidth: 1,
            strokeStyle: '',
            fillStyle: 'yellow',
            font: "bold 14px 'Oswald',courier",
        },
        hexagon: {
            points: [
                [1.732, 0],
                [3.464, 1],
                [3.464, 3],
                [1.732, 4],
                [    0, 3],
                [    0, 1],
            ],
            size: new Point(3.464, 3),
        },
        scale: 10,
        bridge: {
            out: {
                points: [
                    [0, 0],
                    [0.5, 0.25],
                    [1, 0],
                    [0.5, 0.5],
                ],
                lineWidth: 2.3,
                strokeStyle: 'rgba(255, 255, 255, 0.9)',
                fillStyle: 'rgba(255, 0, 0, 0.9)',
            },
        },
    },

    text: '',
    bridge: false,
    count: 0,
    count_color: null,
    color: '#FFFFFF',

    initialize: function (scene, options) {
        // sample
        //var texts = ['99', '0.1K', '9.1K', '27K', '99K', '99M', '99G'];
        //this.text = texts[Math.round(Math.random() * 6)];

        options.shape = this.initShape(options.pos, options.offset);
        this.parent(scene, options); // Draw the shape by parent

        if (options.bridge) this.initBridge(options.bridge);
        this.count = options.count;
        this.setColor(options.color);

        this.clickable(this.redraw)
        this.listenMouse();
    },

    setColor: function(color) {
        var darker = color.shift([-40, -40, -40]);
        if (darker.r > 255) darker.r = 255;
        if (darker.g > 255) darker.g = 255;
        if (darker.b > 255) darker.b = 255;
        if (darker.r < 0) darker.r = 0;
        if (darker.g < 0) darker.g = 0;
        if (darker.b < 0) darker.b = 0;

        this.color = color;
        this.count_color = darker.toString();
    },

    drawCount: function(ctx) {
        var count = this.count,
            color = this.count_color;
        if (count == 0) return;
        var x = this.shape.center.x,
            y = this.shape.center.y,
            power = count > 1 ? Math.ceil(Math.log(count) / Math.LN10) : 1,
            angle = Math.PI * 2 * count / Math.pow(10, power),
            level_size = this.self.scale * 0.25;
            radius = power * level_size;

        ctx.set({lineWidth: level_size});
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, angle);
        ctx.stroke(color);
        if (count > 9) {
            ctx.fill(new Circle(x, y, radius - level_size), color);
            ctx.stroke(new Circle(x, y, radius - level_size), color);
        }
    },

    initShape: function (pos, board_offset) {
        var points = [], i,
            size = this.self.hexagon.size,
            shift_even = (pos.y % 2 ? size.x / 2 : 0),
            offsetX = size.x * pos.x + shift_even + board_offset.x * size.x,
            offsetY = size.y * pos.y + board_offset.y * size.y,
            offset = new Point(offsetX, offsetY);

        this.self.hexagon.points.forEach(function(p){
            var point = new Point(p[0], p[1]);
            point.move(offset).mul(this.self.scale);
            points.push(point);
        }, this);
        return new Polygon(points);
    },

    initBridge: function (bridge) {
        var direction = Math.random() * 360;
        var points = [], shape;
            offset = this.shape.center.clone(),
            width = this.self.bridge.out.points[2][0],
            angle = Math.PI * direction / 180;

        this.bridge = bridge;
        this.bridge_shapes = [];
        if (bridge == 'out') {
            this.self.bridge.out.points.forEach(function(p){
                var point = new Point(p[0], p[1]);
                point.mul(this.self.scale);
                point.move([offset.x, offset.y]);
                points.push(point);
            }, this);
            shape = new Polygon(points).move([-width / 2 * this.self.scale, 0]);
            for (var i=0; i<3; i++) {
                this.bridge_shapes.push(shape.clone().move([0, i*4]).rotate(angle, offset));
            }
        }
    },

    renderTo: function (ctx) {
        if (this.hover) {
            ctx.fill(this.shape, new Color('olive').toString());
        }else{
            ctx.fill(this.shape, this.color.toString());
        }
        ctx.set({ lineWidth: this.self.border.width });
        //ctx.stroke(this.shape, this.self.border.color);

        if (this.bridge == 'out') { // the cell is a bridge out
            ctx.set({lineWidth: this.self.bridge.out.lineWidth});
            this.bridge_shapes.forEach(function(shape){
                ctx.stroke(shape, this.self.bridge.out.strokeStyle);
                ctx.fill(shape, this.self.bridge.out.fillStyle);
            }, this);
        }else{
            this.drawCount(ctx);
            metrics = ctx.measureText(this.text);
            point = this.shape.center.clone();
            point.x -= metrics.width / 2;
            point.y += 5;
            ctx .set(this.self.textStyle)
                .strokeText(this.text, point)
                .fillText(this.text, point);
        }
        return this.parent();
    },
});
