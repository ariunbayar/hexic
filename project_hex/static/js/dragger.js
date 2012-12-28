hexEnv.Dragger = atom.Class({
    Extends: LibCanvas.Scene.Dragger,
    initialize: function (mouse) {
        this.parent(mouse);
    },

    addLayersShift: function (point) {
        var p;
        for (var i = this.scenes.length; i--;) {
            p = new Point(point.x * this.scenes[i].zoom, point.y * this.scenes[i].zoom);
            this.scenes[i].addShift(p);
        }
    },
});
