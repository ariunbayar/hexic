var retrieveBoardURL = '/game/board/';
var retrieveProgressURL = '/game/progress/';
var moveURL = '/game/move/';
var progressInterval = 1000;

$(document).ready(function(){
    $(".hexboard").each(initBoard);
});

function initBoard() {
    var me = $(this);
    var board_id = me.attr('id');
    hexEnv.ajax(retrieveBoardURL, 2000,
        {board_id: board_id},
        function(json){
            var user_id = $('#user_id').val();
            hexEnv.initBoard(user_id, json.board_id, json[json.board_id], json.board_users, movethem);
            showBoardProgress(json.board_id);
        });
}

/**
 * Shows game progress on the board.
 * Moves, counts and colors
 */
function showBoardProgress(board_id) {
    hexEnv.ajax(retrieveProgressURL, 1000,
        {board_id: board_id},
        function(json){
            hexEnv.drawBoard(json.moves, json[json.board_id], json.board_users);
        });
    setTimeout('showBoardProgress("' + board_id + '")', progressInterval);
}

function movethem(from, to, board_id) {
    hexEnv.ajax(moveURL, 3000,
        {fx: from.x, fy: from.y, tx: to.x, ty: to.y,
            user_id: $('#user_id').val(), board_id: board_id},
        function(){});
}
