game = null


class HexController
  hexagon_radius: 50
  update: true
  colors:
    background: createjs.Graphics.getRGB(32, 38, 35)
    hex_border: createjs.Graphics.getRGB(63, 159, 112)
    hex_fill: createjs.Graphics.getRGB(6, 59, 33)


  constructor: (container_id) ->
    # setup default values
    @board = [
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 0, 1],
      [1, 1, 0, 0, 1],
      [1, 1, 1, 1, 1]
    ]

    @point_start = null
    @point_end = null

    @arrow = null
    @hexagon = null

    # create canvas in container element
    $canvas = $('<canvas></canvas>')
    $container = $(container_id).append($canvas)

    # set our playground non-draggable
    @set_nondraggable($container)

    # store and set the sizing
    @width = $container.width()
    @height = $container.height()
    $canvas.attr(width: @width, height: @height)

    # initialize Stage
    @stage = new createjs.Stage($canvas.get(0))
    @stage.enableMouseOver()
    @drawBackground()

    # draw the board
    @hexagon_width = @hexagon_radius * Math.sqrt(3)
    @cells = []
    offset_x = 100
    offset_y = 100
    for y of @board
      cell_rows = new Array()
      for x of @board[y]
        continue unless @board[y][x]
        pos_x = @hexagon_width * x + (y % 2) * @hexagon_width / 2
        pos_y = @hexagon_radius * 1.5 * y
        shape = @new_hexagon(offset_x + pos_x, offset_y + pos_y)
        cell =
          arrow: null
          hexagon: shape

        @stage.addChild(shape)
        cell_rows[x] = cell
      @cells.push(cell_rows)
    
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

@start_game = (playground) ->
  game = new HexController(playground)
