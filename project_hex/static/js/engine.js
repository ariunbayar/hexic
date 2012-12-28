LibCanvas.extract();
window.hexEnv = {};
atom.dom(function(){
    window.hex = new hexEnv.Controller('canvas');
});


function getAngle(x1, y1, x2, y2) {
    return Math.atan2(y2 - y1, x2 - x1);
}

function normalizeAngle(angle){
    var angle60 = Math.PI / 3;
    return angle60 * Math.round(angle / angle60);
}
