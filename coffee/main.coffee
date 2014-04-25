class GameEngine
  url_board: null
  url_progress: null
  url_move: null

  update_interval: null
  renderer: null

  user_id : null  # usage ?
  board_id: null

  constructor: (container_id, width, height) ->
    @renderer = new Engine(container_id, width, height)

  start: ->
    self = @
    fn = ->
      (-> @ajax(@url_progress, @update_interval, {}, @drawBoard)).call(self)
    setInterval(fn, @update_interval)

  drawBoard: (data) ->
    @renderer.updateBoard(@convertHexicDataForEngine(data))

  convertHexicDataForEngine: (hexic_data) ->
    data = []
    for y of hexic_data.board_users
      data[y] = [] if not (y of data)
      for x of hexic_data.board_users[y]
        [user_id, color] = hexic_data.board_users[y][x]
        power = hexic_data[@board_id][y][x]
        data[y][x] = [user_id, power] if not (x of data[y])
    getDirection = (fx, fy, tx, ty) ->
      shift = if fy % 2 then 0 else 1
      return 1 if ty == fy - 1 and tx == fx - 1 + shift
      return 2 if ty == fy - 1 and tx == fx + shift
      return 3 if ty == fy     and tx == fx + 1
      return 4 if ty == fy + 1 and tx == fx + shift
      return 5 if ty == fy + 1 and tx == fx - 1 + shift
      return 6 if ty == fy     and tx == fx - 1
      return 0
    for [fx, fy, tx, ty] in hexic_data.moves
      direction = getDirection(fx, fy, tx, ty)
      data[fy][fx][2] = direction if direction
    return data

  ajax: (url, timeout, data, successFunc = ->) ->
    data['board_id'] = @board_id
    $.ajax({
      url: url
      dataType: "json"
      data: data
      cache: false
      context: @
      timeout: timeout
      error: (xhr, msg) ->
      success: successFunc
    })

@init_svg_game = (playground, width, height) ->
  if typeof(Engine) == "undefined"
    throw "Render engine has not been included!"
    return
  return new GameEngine(playground, width, height)
