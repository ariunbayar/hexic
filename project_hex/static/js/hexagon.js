/**
 * Formula to solve Sx:
 * Ez = distance from eye to the center of the screen
 * Ex = X coordinate of the eye
 * Px = X coordinate of the 3D point
 * Pz = Z coordinate of the 3D point
 * Sx = (Ez*(Px-Ex)) / (Ez+Pz) + Ex
 *
 * Formula to solve Sy:
 * Ez = distance from eye to the center of the screen
 * Ey = Y coordinate of the eye 
 * Py = Y coordinate of the 3D point
 * Pz = Z coordinate of the 3D point    
 * Sy = (Ez*(Py-Ey)) / (Ez+Pz) + Ey
 */

hexEnv.Hexagon = atom.Class({
    Extends: LibCanvas.Scene.Element,

    Implements: [Clickable, Draggable],

    Static: {
        hex: [
            [1.732, 0],
            [3.464, 1],
            [3.464, 3],
            [1.732, 4],
            [    0, 3],
            [    0, 1],
        ],
        eye: new LibCanvas.Point3D([1, 0, 50]),
    },

    initialize: function (scene, options) {
        this.parent(scene, options);
        /*
        var x, y, z, points = [];

        z = options.p.z;
        for (var i=0; i<this.self.hex.length; i++) {
            x = (this.self.hex[i][0] + options.p.x);
            y = (this.self.hex[i][1] + options.p.y);
            points.push(this.transform(x, y, z, options.size));
        }
        this.shape = new Polygon(points);
        */
        this.clickable(this.redraw);
        this.draggable(this.redraw);

        //this.listenMouse();
        this.addEvent('over', function(e){console.log('mouseover');});
    },

    transform: function (_x, _y, _z, scale) {
        var x, y,
            eye = this.self.eye;
        x = (eye.z * (_x - eye.x)) / (eye.z + _z) + eye.x;
        y = (eye.z * (_y - eye.y)) / (eye.z + _z) + eye.y;

        //x = _x / 2 - _y/20 + 10;
        //y = _y / 5 + 10 + _z;

        //x = _x;
        //y = _y;
        return new Point([x, y]).mul(scale);
    },

    get type () {
        return this.options.type;
    },

    /** @private */
    fastMoveRect: function (hex, shift) {
        hex.each(function(point){
            point.x += shift.x;
            point.y += shift.y;
        });
    },

    addShift: function (shift) {
        this.fastMoveRect(this.shape, shift);
        this.fastMoveRect(this.previousBoundingShape, shift);
        return this;
    },

    renderTo: function (ctx) {
        console.log('renderTo');
        if (this.hover) {
            //ctx.stroke(this.shape, 'rgba(255, 255, 255, 0.5)');
            ctx.fill(this.shape, 'rgba(255, 0, 0, 0.5)');
        }else{
            ctx.fill(this.shape, 'rgba(200, 200, 200, 1)');
            ctx.stroke(this.shape, 'rgba(255, 255, 255, 1)');
        }
        return this;
    }
});
