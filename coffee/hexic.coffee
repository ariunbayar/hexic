class HexController
  url_board: null
  url_progress: null
  url_move: null

  update_interval: null
  hexagon_radius: null
  update: true
  point_start: null
  point_end: null
  colors:
    background: createjs.Graphics.getRGB(32, 38, 35)
    hex_border: createjs.Graphics.getRGB(63, 159, 112)
    hex_fill: createjs.Graphics.getRGB(6, 59, 33)

  constructor: (container_id) ->
    @container_id = container_id
    @hexagon_width = @hexagon_radius * Math.sqrt(3)

  drawBackground: ->
    # fill background
    shape = new createjs.Shape()
    shape.graphics.beginFill(@colors.background)
    shape.graphics.rect(0, 0, @width, @height)
    @stage.addChild(shape)

  show_arrow: (point_start, point_end) ->
    return if Math.abs(point_end.x - point_start.x) > @hexagon_width + 1
    return if Math.abs(point_end.y - point_start.y) > @hexagon_width + 1
    @temp_arrow.x = point_start.x
    @temp_arrow.y = point_start.y
    @temp_arrow.rotation = @angle_from_points(point_start, point_end)
    @temp_arrow

  new_hexagon: (x, y) ->
    hexagon = new createjs.Shape()
    hexagon.graphics.setStrokeStyle(10, "round")
    hexagon.graphics.beginStroke(@colors.hex_border)
    hexagon.graphics.beginFill(@colors.hex_fill)
    hexagon.graphics.drawPolyStar(0, 0, @hexagon_radius, 6, 0, -90)
    hexagon.x = x
    hexagon.y = y

    hex_game = @
    
    # attach handlers
    hexagon.onMouseOver = (e) ->
      if hex_game.point_start
        hex_game.point_end = e.target
        hex_game.temp_arrow.visible = true
        hex_game.update = true

    hexagon.onPress = (e) ->
      hex_game.point_start = e.target
      e.onMouseUp = (ev) ->
        hex_game.point_start = null
        hex_game.point_end = null
        hex_game.update = true

    return hexagon

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

  init_board: (json) ->
    ###
    A callback function for board details
    Initialize board by drawing into stage
    ###
    user_id = $("#user_id").val()
    board = json[json.board_id]
    console.log(@)
    console.log(@hexagon_radius)
    console.log(hex_game.hexagon_radius)

    # draw the board
    hex_game.cells = []
    offset_x = 100
    offset_y = 100
    for y of board
      cell_rows = new Array()
      for x of board[y]
        continue unless board[y][x]
        pos_x = hex_game.hexagon_width * x + (y % 2) * hex_game.hexagon_width / 2
        pos_y = hex_game.hexagon_radius * 1.5 * y
        shape = hex_game.new_hexagon(offset_x + pos_x, offset_y + pos_y)
        cell =
          arrow: null
          hexagon: shape

        hex_game.stage.addChild(shape)
        cell_rows[x] = cell
      hex_game.cells.push(cell_rows)

    #hexEnv.initBoard(user_id, json.board_id, json[json.board_id], json.board_users, movethem)
    #showBoardProgress(json.board_id)
    return

  start: ->
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

  tick: ->
    if @update
      if @point_start and @point_end
        if @point_start.x isnt @point_end.x or @point_start.y isnt @point_end.y
          @show_arrow(@point_start, @point_end)
      else
        @temp_arrow.visible = false
      @fpsLabel.text = Math.round(createjs.Ticker.getMeasuredFPS()) + " fps"
      @update = false
      @stage.update()

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

  ajax: (url, timeout, data, successFunc) ->
    self = @
    $.ajax({
      url: url
      dataType: "json"
      data: data
      cache: false
      timeout: timeout
      error: (xhr, msg) ->
        return
      success: ((json) ->
        console.log(@);
        return (json) ->
          successFunc(json)
      )(self)
    })


@init_game = (playground) ->
  return new HexController(playground)
