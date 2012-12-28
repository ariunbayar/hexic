var BoardEdit = {
    last_action: 'noop',

    init: function () {
        $('.actions input[name=action]').change(BoardEdit.actionChange);
        $('form#board-save').submit(BoardEdit.submitBoard);
    },

    /**
     * Applies action when the radio button changes
     */
    actionChange: function(){
        var value = $(this).val();

        if (BoardEdit.last_action == 'cell'){
            $('.board-main .cell').unbind('click', BoardEdit.toggleCell);
            $('.actions input[name=random]').unbind('click', BoardEdit.randomCells);
        }

        BoardEdit.last_action = value;
        if (value == 'cell'){
            $('.board-main .cell').bind('click', BoardEdit.toggleCell);
            $('.actions input[name=random]').bind('click', BoardEdit.randomCells);
        }
    },

    /**
     * Toggle cell action when the cell is clicked
     */
    toggleCell: function(){
        var cell = $(this);
        cell.toggleClass('off');
    },

    /**
     * Prepares the board data for submission before the form is submitted.
     */
    submitBoard: function(){
        var board = [], form = $(this);
        $('.board-main .board_row').each(function(){
            var row = [];
            $(this).children('.cell').each(function(){
                var cell = $(this);
                if (cell.hasClass('off')){
                    row.push('');
                }else{
                    var count = parseInt(cell.html()),
                        player = cell.attr('player');
                    row.push(count + '-' + player);
                }
            });
            board.push(row.join());
        });
        form.children('[name=data]').val(board.join(';'));
    },

    /**
     * Randomly toggles cells
     */
    randomCells: function(){
        $('.board-main .cell').each(function(){
            var cell = $(this);
            cell.toggleClass('off', Math.random() > .4);
        });
    }
}
