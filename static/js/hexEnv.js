var hexEnv = {};

hexEnv.mouse_down = false;
hexEnv.from = {x: -1};
hexEnv.cellHeight = 43;
hexEnv.cellWidth = 50;
hexEnv.moveFunc = function (from, to) {}; // override
hexEnv.cells = [];
hexEnv.arrows = {};

hexEnv.posEqual = function (a, b) {
    return (a.x == b.x) && (a.y == b.y);
}

hexEnv.mouseDown = function (e) {  // EVENT
    if (!this.board.data('is_ready')) return;
    if (this.mouse_down) return;
    this.mouse_down = true;
    this.from = $.extend(true, {}, $(e.currentTarget).data('position'));
}

hexEnv.mouseUp = function (e) {  // EVENT
    if (!this.board.data('is_ready')) return;
    this.mouse_down = false;
    var to = $(e.currentTarget).data('position');
    if (this.from.x == -1 || to.x == -1) return;
    if (this.posEqual(this.from, to)) {
        if (!((to.x + '_' + to.y) in this.arrows)) return;
    }
    if ('temp' in this.arrows) this.arrows['temp'].hide();
    console.log(this.from, to);
    this.moveFunc(this.from, to, this.board.attr('id'));
}

hexEnv.cellLeave = function () {  // EVENT
    if (!this.board.data('is_ready')) return;
    if (!this.mouse_down) {
        this.from.x = -1;
    }
}

/* Shows arrow that are going to be moved when mouse clicks */
hexEnv.showArrow = function (e) {  // EVENT
    if (!this.board.data('is_ready')) return;
    if (this.from.x == -1) return;
    var to = $(e.currentTarget).data('position');
    if (this.posEqual(this.from, to)) {
        if ('temp' in this.arrows) {
            this.arrows['temp'].hide();
        }
    }else{
        var tmparr = this.drawArrow(this.from, to, 'temp');
        tmparr.data('pos', this.from.x + '_' + this.from.y);
    }
}

hexEnv.drawArrow = function (from, to, key) {
    var arrow = this.vector2arrow(from, to);
    if (arrow.length == 0) return;

    key = (typeof key == 'undefined') ? from.x + '_' + from.y : key;
    if (key in this.arrows) {
        $arrow = this.arrows[key];
        $arrow.attr('class', "arrow " + arrow).show();
    }else{
        $arrow = this.newArrow(arrow);
        this.arrows[key] = $arrow;
        this.board.append($arrow)
    }
    var pos = this.cells[from.x][from.y].position();
    $arrow.css({top: (pos.top - 20) + "px", left: (pos.left - 20) + "px"});
    return $arrow;
}

hexEnv.newArrow = function (arrow) {
    var attrs = {'class': "arrow " + arrow};
    return $("<div></div>").attr(attrs);
}

hexEnv.vector2arrow = function (from, to) {
    var arrow = '';
    var xx = from.x;
    if (from.y % 2 == 0) xx += 1;
    if ((to.x - 1 == from.x) && (to.y == from.y)) arrow = 'arrow-0';
    if ((to.x == xx) && (to.y - 1 == from.y)) arrow = 'arrow-60';
    if ((to.x + 1 == xx) && (to.y - 1 == from.y)) arrow = 'arrow-120';
    if ((to.x + 1 == from.x) && (to.y == from.y)) arrow = 'arrow-180';
    if ((to.x + 1 == xx) && (to.y + 1 == from.y)) arrow = 'arrow-240';
    if ((to.x == xx) && (to.y + 1 == from.y)) arrow = 'arrow-300';
    return arrow;
}

hexEnv.bindEventsTo = function (board) {
    board.find(".cell").bind('mouseenter', $.proxy(this, 'showArrow'));
    board.find(".cell").bind('mouseleave', $.proxy(this, 'cellLeave'));
    board.find(".cell").bind('mousedown', $.proxy(this, 'mouseDown'));
    board.find(".cell").bind('mouseup', $.proxy(this, 'mouseUp'));
}

hexEnv.initBoard = function (user_id, board_id, board_data, board_users, moveFunc) {
    var cells = [];
    var board = $('#' + board_id);

    for (var y=0; y<board_data.length; y++) {
        for (var x=0; x<board_data[y].length; x++) {
            if (typeof(cells[x]) == 'undefined') cells[x] = [];
            cells[x][y] = 0;
        }
    }
    for (var y=0; y<board_data.length; y++) {
        for (var x=0; x<board_data[y].length; x++) {
            if (board_data[y][x] <= 0) continue;
            var cellback = $('<div class="cell-back"></div>');
            var cell = $('<div class="cell"></div>');
            cellback.css({top: (y * this.cellHeight) + 'px', left: (x * this.cellWidth + (y%2 ? 0 : this.cellWidth/2)) + 'px'});
            cell.css({top: (y * this.cellHeight + 7) + 'px', left: (x * this.cellWidth + (y%2 ? 0 : this.cellWidth/2)) + 'px'});
            board.append(cellback);
            board.append(cell);
            cell.data('position', {x: x, y: y});
            cell.data('back', cellback);
            cells[x][y] = cell;
        }
    }
    this.user_id = user_id;
    this.cells = cells;
    this.bindEventsTo(board);
    this.board = board;
    this.users = board_users;
    this.moveFunc = moveFunc;
}

hexEnv.ajax = function (url, timeout, data, successFunc) {
    $.ajax({
        url: url,
        dataType: 'json',
        data: data,
        cache: false,
        timeout: timeout,
        success: successFunc,
        error: function (xhr, msg) {
            // TODO log errors and submit
        },
    });
}

hexEnv.drawBoard = function (moves, board_data, board_users) {
    // TODO too much code?
    this.board.data('is_ready', false);
    this.users = board_users;
    var cells = this.cells;

    // show board values and user colors
    for (y = 0; y < board_data.length; y++) {
        for (x = 0; x < board_data[y].length; x++) {
            if (board_data[y][x]) {
                var n = board_data[y][x];
                if (n >= 9000)
                    n = Math.round(n / 1000) + 'k';
                else if (n >= 100)
                    n = Math.round(n / 100) / 10 + 'k';
                cells[x][y].html(n); // original
                if (this.users[y][x][0] == this.user_id) {
                    cells[x][y].attr('class', 'cell cellfriend');
                }else{
                    cells[x][y].attr('class', 'cell cellfoe');
                }
                var background = cells[x][y].data('back');
                background.attr('class', 'cell-back cell' + board_users[y][x][1]);
            }
        }
    }
    // show moves in arrows
    var mentions = [];
    var tmparr = [];
    if ('temp' in this.arrows) {
        tmparr = this.arrows['temp'];
        mentions[0] = tmparr;
    }
    for (var i = 0; i < moves.length; i++) {
        var move = moves[i];
        var arr = this.drawArrow({x: move[0], y: move[1]}, {x: move[2], y: move[3]});
        var key = move[0] + '_' + move[1];
        if (tmparr.length) {
            if (tmparr.data('pos') == (key)) tmparr.hide();
        }
        mentions[mentions.length] = key;
    }
    var arrows = this.arrows;
    $.each(arrows, function(k, arr){
        if (mentions.indexOf(k) == -1) {
            arr.remove();
            delete arrows[k];
        }
    });

    this.board.data('is_ready', true);
}


