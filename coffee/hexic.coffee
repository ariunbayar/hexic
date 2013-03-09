class HexController
  url_board: null
  url_progress: null
  url_move: null

  update_interval: null
  hexagon_radius: null
  update: true

  point_start: null
  point_end: null
  is_ready: false
  colors:
    background: createjs.Graphics.getRGB(32, 38, 35)
    hex_border: createjs.Graphics.getRGB(63, 159, 112)
    hex_fill: createjs.Graphics.getRGB(6, 59, 33)

  constructor: (container_id) ->
    @container_id = container_id
    @time_left_to_update = 0

  drawBackground: ->
    # fill background
    shape = new createjs.Shape()
    shape.graphics.beginFill(@colors.background)
    shape.graphics.rect(0, 0, @width, @height)
    @stage.addChild(shape)

  show_arrow: (point_start, point_end) ->
    if Math.abs(point_end.x - point_start.x) > @hexagon_width + 1
      return
    if Math.abs(point_end.y - point_start.y) > @hexagon_width + 1
      return
    @temp_arrow.x = point_start.x
    @temp_arrow.y = point_start.y
    @temp_arrow.rotation = @angle_from_points(point_start, point_end)
    return @temp_arrow

  new_hexagon: (x, y, coord) ->
    hexagon = new createjs.Shape()
    hexagon.graphics.setStrokeStyle(10, "round")
    hexagon.graphics.beginStroke(@colors.hex_border)
    hexagon.graphics.beginFill(@colors.hex_fill)
    hexagon.graphics.drawPolyStar(0, 0, @hexagon_radius, 6, 0, -90)

    hexagon.x = x
    hexagon.y = y
    hexagon.coord = coord

    self = @
    
    # attach handlers
    hexagon.onMouseOver = (e) ->
      if self.point_start
        self.point_end = e.target
        self.temp_arrow.visible = true
        self.update = true

    hexagon.onPress = (e) ->
      self.point_start = e.target
      e.onMouseUp = (ev) ->
        self.move(self.point_start.coord, self.point_end.coord)
        self.point_start = null
        self.point_end = null
        self.update = true

    hexagon.update = (n, user_id) -> self.update_hexagon(hexagon, n, user_id)

    return hexagon

  update_hexagon: (hexagon, n, user_id) ->
    console.log('please implement')

  move: (from, to) ->
    params = {
      fx: from.x
      fy: from.y
      tx: to.x
      ty: to.y
    }
    @ajax(@url_move, 3000, params)

  new_arrow: (x, y, rotation) ->
    arrow = new createjs.Shape()
    size = 40
    arrow.regX = size
    arrow.regY = size * 2
    num_arrows = ""
    coef = 0.75
    scaled_size = size

    for i in [1..5]
      offset_x = size - scaled_size / 2
      offset_y = offset_x * 3 - size
      arrow.graphics.moveTo(offset_x, offset_y)
      arrow.graphics.setStrokeStyle(scaled_size / 7)
      arrow.graphics.beginStroke("#AAAAAA")
      arrow.graphics.lineTo(offset_x + scaled_size / 2, offset_y - scaled_size / 2)
      arrow.graphics.lineTo(offset_x + scaled_size, offset_y)
      arrow.graphics.endStroke()
      scaled_size = scaled_size * coef
    arrow.rotation = (if rotation then rotation else 0)
    arrow.x = x
    arrow.y = y
    return arrow

  init_board: (self, json) ->
    ###
    A callback function for board details
    Initialize board by drawing into stage
    ###
    user_id = $("#user_id").val()
    board = json[json.board_id]

    # draw the board
    self.cells = []
    offset_x = 100
    offset_y = 100
    for y of board
      cell_rows = new Array()
      for x of board[y]
        continue unless board[y][x]
        pos_x = self.hexagon_width * x - (y % 2) * self.hexagon_width / 2
        pos_y = self.hexagon_radius * 1.5 * y
        shape = self.new_hexagon(offset_x + pos_x, offset_y + pos_y, {x: x, y: y})
        cell =
          arrow: null
          hexagon: shape

        self.stage.addChildAt(shape, 1)
        cell_rows[x] = cell
      self.cells.push(cell_rows)

    @is_ready = true
    return

  draw_updated_data: (self, data) ->
    self.is_ready = false
    self.users = data.board_users
    cells = self.cells
    
    # show board values and user colors
    board_data = data[data.board_id]
    for y of board_data
      for x of board_data[y]
        if board_data[y][x]
          cells[y][x].hexagon.update(board_data[y][x], self.users[y][x][0])

    # TODO allow it to show arrows
    return
    
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
      if tmparr.lenght
        tmparr.hide() if tmparr.data('pos') is (key)
      mentions[mentions.length] = key
      i++
    arrows = @arrows
    $.each(arrows, (k, arr) ->
      if mentions.indexOf(k) is -1
        arr.remove()
        delete arrows[k]
        return
    )

    @is_ready = true

  start: ->
    @hexagon_width = @hexagon_radius * Math.sqrt(3)

    # create canvas in container element
    $canvas = $('<canvas></canvas>')
    $container = $(@container_id).append($canvas)

    # set our playground non-draggable
    @set_nondraggable($container)

    # store and set the sizing
    @width = $container.width()
    @height = $container.height()
    $canvas.attr(width: @width, height: @height)

    # initialize Stage
    @stage = new createjs.Stage($canvas.get(0))
    @stage.enableMouseOver()
    # TODO change the board id
    @ajax(@url_board, 2000, {board_id: 'board1'}, @init_board)
    @drawBackground()

    # fpsLabel
    @fpsLabel = new createjs.Text("-- fps", "bold 18px Arial", "#000")
    @stage.addChild(@fpsLabel)
    @fpsLabel.x = 10
    @fpsLabel.y = 20

    @temp_arrow = @new_arrow(0, 0, null)
    @stage.addChild(@temp_arrow)
    
    #draw to the canvas
    @stage.update()
    createjs.Ticker.addListener(@)
    createjs.Ticker.setFPS(50)

  tick: (time_passed) ->
    if @update
      if @point_start and @point_end
        if @point_start.x isnt @point_end.x or @point_start.y isnt @point_end.y
          @show_arrow(@point_start, @point_end)
      else
        @temp_arrow.visible = false
      @fpsLabel.text = Math.round(createjs.Ticker.getMeasuredFPS()) + " fps"
      @update = false
      @stage.update()

    # load and show the progress every interval
    @time_left_to_update -= time_passed
    if @time_left_to_update <= 0
      # reset the time to update
      @time_left_to_update += @update_interval
      @ajax(@url_progress, @update_interval, {}, @draw_updated_data)

  set_nondraggable: (element) ->
    $(element).on('dragstart',
      (e)->
        e.preventDefault()
        return
    )

  angle_from_points: (point_start, point_end) ->
    b = point_end.y - point_start.y
    c = point_end.x - point_start.x
    a = Math.sqrt(b * b + c * c)
    angle = Math.acos(b / a) * 180 / Math.PI
    angle = 360 - angle  if c > 0
    angle += 180
    return angle

  ajax: (url, timeout, data, successFunc = ->) ->
    self = @
    $.ajax({
      url: url
      dataType: "json"
      data: data
      cache: false
      timeout: timeout
      error: (xhr, msg) ->
      success: (json) ->
        successFunc(self, json)
    })


@init_game = (playground) ->
  return new HexController(playground)
