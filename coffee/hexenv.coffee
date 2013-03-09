hexEnv = {}
hexEnv.mouse_down = false
hexEnv.from = x: -1
hexEnv.cellHeight = 43
hexEnv.cellWidth = 50
hexEnv.moveFunc = (from, to) -> # override

hexEnv.cells = []
hexEnv.arrows = {}
hexEnv.posEqual = (a, b) ->
  (a.x == b.x) and (a.y == b.y)


hexEnv.mouseDown = (e) -> # EVENT
  return unless @board.data("is_ready")
  return if @mouse_down
  @mouse_down = true
  @from = $.extend(true, {}, $(e.currentTarget).data("position"))
  return

hexEnv.posEqual = (a, b) ->
  (a.x is b.x) and (a.y is b.y)

hexEnv.mouseUp = (e) -> # EVENT
  return unless @board.data("is_ready")
  @mouse_down = false
  to = $(e.currentTarget).data("position")
  return if @from.x is -1 or to.x is -1
  return unless (to.x + "_" + to.y) of @arrows  if @posEqual(@from, to)
  @arrows["temp"].hide() if "temp" of @arrows
  @moveFunc(@from, to, @board.attr("id"))

hexEnv.cellLeave = -> # EVENT
  return unless @board.data("is_ready")
  @from.x = -1 unless @mouse_down

# Shows arrow that are going to be moved when mouse clicks 
hexEnv.showArrow = (e) -> # EVENT
  return unless @board.data("is_ready")
  return if @from.x is -1
  to = $(e.currentTarget).data("position")
  if @posEqual(@from, to)
    @arrows["temp"].hide() if "temp" of @arrows
  else
    tmparr = @drawArrow(@from, to, "temp")
    tmparr.data("pos", @from.x + "_" + @from.y)

hexEnv.drawArrow = (from, to, key) ->
  arrow = @vector2arrow(from, to)
  return if arrow.length is 0
  key = (if (typeof key is "undefined") then from.x + "_" + from.y else key)
  if key of @arrows
    $arrow = @arrows[key]
    $arrow.attr("class", "arrow " + arrow).show()
  else
    $arrow = @newArrow(arrow)
    @arrows[key] = $arrow
    @board.append $arrow
  pos = @cells[from.x][from.y].position()
  $arrow.css({
    top: (pos.top - 20) + "px"
    left: (pos.left - 20) + "px"
  })
  $arrow

hexEnv.newArrow = (arrow) ->
  attrs = class: "arrow " + arrow
  $("<div></div>").attr(attrs)

hexEnv.vector2arrow = (from, to) ->
  arrow = ""
  xx = from.x
  xx += 1  if from.y % 2 is 0
  arrow = "arrow-0" if (to.x - 1 is from.x) and (to.y is from.y)
  arrow = "arrow-60" if (to.x is xx) and (to.y - 1 is from.y)
  arrow = "arrow-120" if (to.x + 1 is xx) and (to.y - 1 is from.y)
  arrow = "arrow-180" if (to.x + 1 is from.x) and (to.y is from.y)
  arrow = "arrow-240" if (to.x + 1 is xx) and (to.y + 1 is from.y)
  arrow = "arrow-300" if (to.x is xx) and (to.y + 1 is from.y)
  arrow

hexEnv.bindEventsTo = (board) ->
  board.find(".cell").bind("mouseenter", $.proxy(this, "showArrow"))
  board.find(".cell").bind("mouseleave", $.proxy(this, "cellLeave"))
  board.find(".cell").bind("mousedown", $.proxy(this, "mouseDown"))
  board.find(".cell").bind("mouseup", $.proxy(this, "mouseUp"))

hexEnv.initBoard = (user_id, board_id, board_data, board_users, moveFunc) ->
  cells = []
  board = $("#" + board_id)
  y = 0

  while y < board_data.length
    x = 0

    while x < board_data[y].length
      cells[x] = [] if typeof (cells[x]) is "undefined"
      cells[x][y] = 0
      x++
    y++
  y = 0

  while y < board_data.length
    x = 0

    while x < board_data[y].length
      continue  if board_data[y][x] <= 0
      cellback = $("<div class=\"cell-back\"></div>")
      cell = $("<div class=\"cell\"></div>")
      cellback.css
        top: (y * @cellHeight) + "px"
        left: (x * @cellWidth + ((if y % 2 then 0 else @cellWidth / 2))) + "px"

      cell.css
        top: (y * @cellHeight + 7) + "px"
        left: (x * @cellWidth + ((if y % 2 then 0 else @cellWidth / 2))) + "px"

      board.append cellback
      board.append cell
      cell.data "position",
        x: x
        y: y

      cell.data "back", cellback
      cells[x][y] = cell
      x++
    y++
  @user_id = user_id
  @cells = cells
  @bindEventsTo board
  @board = board
  @users = board_users
  @moveFunc = moveFunc

hexEnv.ajax = (url, timeout, data, successFunc) ->
  $.ajax({
    url: url
    dataType: "json"
    data: data
    cache: false
    timeout: timeout
    success: successFunc
    error: (xhr, msg) ->
  })


# TODO log errors and submit
hexEnv.drawBoard = (moves, board_data, board_users) ->
  # TODO too much code?
  @board.data("is_ready", false)
  @users = board_users
  cells = @cells
  
  # show board values and user colors
  y = 0
  while y < board_data.length
    x = 0
    while x < board_data[y].length
      if board_data[y][x]
        n = board_data[y][x]
        if n >= 9000
          n = Math.round(n / 1000) + "k"
        else n = Math.round(n / 100) / 10 + "k"  if n >= 100
        cells[x][y].html n # original
        if @users[y][x][0] is @user_id
          cells[x][y].attr("class", "cell cellfriend")
        else
          cells[x][y].attr("class", "cell cellfoe")
        background = cells[x][y].data("back")
        background.attr("class", "cell-back cell" + board_users[y][x][1])
      x++
    y++
  
  # show moves in arrows
  mentions = []
  tmparr = []
  if "temp" of @arrows
    tmparr = @arrows["temp"]
    mentions[0] = tmparr
  i = 0

  while i < moves.length
    move = moves[i]
    arr = @drawArrow(
      x: move[0]
      y: move[1]
    ,
      x: move[2]
      y: move[3]
    )
    key = move[0] + "_" + move[1]
    tmparr.hide()  if tmparr.data("pos") is (key)  if tmparr.length
    mentions[mentions.length] = key
    i++
  arrows = @arrows
  $.each(arrows, (k, arr) ->
    if mentions.indexOf(k) is -1
      arr.remove()
      delete arrows[k]
  )

  @board.data("is_ready", true)
