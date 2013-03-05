update = true

colors =
  background: createjs.Graphics.getRGB(32, 38, 35)
  hex_border: createjs.Graphics.getRGB(63, 159, 112)
  hex_fill: createjs.Graphics.getRGB(6, 59, 33)

Hexagon = (x, y, hex_radius) ->
  radius = ((if hex_radius then hex_radius else 50))
  hexagon = new createjs.Shape()
  hexagon.graphics.setStrokeStyle 10, "round"
  hexagon.graphics.beginStroke colors.hex_border
  hexagon.graphics.beginFill colors.hex_fill
  hexagon.graphics.drawPolyStar 0, 0, radius, 6, 0, -90
  hexagon.x = x
  hexagon.y = y
  
  # attach handlers
  hexagon.onMouseOver = (e) ->
    if hex.point_start
      hex.point_end = e.target
      hex.temp_arrow.visible = true
      update = true

  hexagon.onPress = (e) ->
    hex.point_start = e.target
    e.onMouseUp = (ev) ->
      hex.point_start = 0
      hex.point_end = 0
      update = true

  return hexagon

Arrow = (x, y, rotation) ->
  arrow = new createjs.Shape()
  size = 40
  arrow.regX = size
  arrow.regY = size * 2
  num_arrows = ""
  coef = 0.75
  scaled_size = size
  i = 0

  while i < 5
    offset_x = size - scaled_size / 2
    offset_y = offset_x * 3 - size
    arrow.graphics.moveTo offset_x, offset_y
    arrow.graphics.setStrokeStyle scaled_size / 7
    arrow.graphics.beginStroke "#AAAAAA"
    arrow.graphics.lineTo offset_x + scaled_size / 2, offset_y - scaled_size / 2
    arrow.graphics.lineTo offset_x + scaled_size, offset_y
    arrow.graphics.endStroke()
    scaled_size = scaled_size * coef
    i += 1
  arrow.rotation = ((if rotation then rotation else 0))
  arrow.x = x
  arrow.y = y
  arrow

angleFromPoints = (point_start, point_end) ->
  a = undefined
  b = undefined
  c = undefined
  angle = undefined
  b = point_end.y - point_start.y
  c = point_end.x - point_start.x
  a = Math.sqrt(b * b + c * c)
  angle = Math.acos(b / a) * 180 / Math.PI
  angle = 360 - angle  if c > 0
  angle += 180
  angle


###
Hexagon game logic
###
hex =
  stage: null
  fpsLabel: null
  board: [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1]
  ]
  point_start: null
  point_end: null
  hexagon_radius: 50
  hexagon_width: null
  cells: []
  temp_arrow: null
  arrow: null
  hexagon: null
  width: null
  height: null

window.hex = hex

hex.init = (container_id) ->
  # create canvas in container element
  $canvas = $('<canvas></canvas>')
  $container = $(container_id).append($canvas)
  # set our playground non-draggable
  $container.on('dragstart',
    (e)->
      e.preventDefault()
      return
  )
  hex.width = $container.width()
  hex.height = $container.height()
  $canvas.attr(width: hex.width, height: hex.height)

  # initialize Stage
  stage = undefined
  stage = new createjs.Stage($canvas.get(0))
  stage.enableMouseOver()
  hex.stage = stage
  hex.drawBackground()
  hex.temp_arrow = Arrow(0, 0, null)
  hex.hexagon_width = hex.hexagon_radius * Math.sqrt(3)
  offset_x = 100
  offset_y = 100
  y = 0

  while y < hex.board.length
    cell_rows = new Array()
    x = 0

    while x < hex.board[0].length
      x += 1
      continue  unless hex.board[y][x]
      pos_x = hex.hexagon_width * x + (y % 2) * hex.hexagon_width / 2
      pos_y = hex.hexagon_radius * 1.5 * y
      shape = Hexagon(offset_x + pos_x, offset_y + pos_y, hex.hexagon_radius)
      cell =
        arrow: null
        hexagon: shape

      stage.addChild shape
      cell_rows[x] = cell
    hex.cells.push cell_rows
    y += 1
  
  # fpsLabel
  hex.fpsLabel = new createjs.Text("-- fps", "bold 18px Arial", "#000")
  stage.addChild hex.fpsLabel
  stage.addChild hex.temp_arrow
  hex.fpsLabel.x = 10
  hex.fpsLabel.y = 20
  
  #draw to the canvas
  stage.update()
  createjs.Ticker.addListener hex
  createjs.Ticker.setFPS 50

hex.drawBackground = ->
  # fill background
  shape = new createjs.Shape()
  shape.graphics.beginFill colors.background
  shape.graphics.rect(0, 0, hex.width, hex.height)
  hex.stage.addChild shape

hex.showArrow = (point_start, point_end) ->
  return  if Math.abs(point_end.x - point_start.x) > hex.hexagon_width + 1
  return  if Math.abs(point_end.y - point_start.y) > hex.hexagon_width + 1
  hex.temp_arrow.x = point_start.x
  hex.temp_arrow.y = point_start.y
  hex.temp_arrow.rotation = angleFromPoints(point_start, point_end)
  hex.temp_arrow

hex.tick = ->
  if update
    if hex.point_start and hex.point_end
      hex.showArrow hex.point_start, hex.point_end  if hex.point_start.x isnt hex.point_end.x or hex.point_start.y isnt hex.point_end.y
    else
      hex.temp_arrow.visible = false
    hex.fpsLabel.text = Math.round(createjs.Ticker.getMeasuredFPS()) + " fps"
    update = false
    hex.stage.update()
