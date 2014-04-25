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
    return if @tmp
    @tmp = 1 if @tmp == undefined
    @renderer.updateBoard(@convertHexicDataForEngine(data))

  convertHexicDataForEngine: (hexic_data) ->
    data = []
    powers = hexic_data[@board_id]
    users = hexic_data.board_users
    moves = hexic_data.moves
    for y of users
      data[y] = [] if not (y of data)
      for x of users[y]
        [user_id, color] = users[y][x]
        power = powers[y][x]
        data[y][x] = [user_id, power] if not (x of data[y])
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
