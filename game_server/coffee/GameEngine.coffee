class GameEngine
  url_board: null
  url_progress: null
  url_move: null

  update_interval: null
  renderer: null

  board_id: null

  constructor: (container_id, width, height, user_id) ->
    @renderer = new Engine(container_id, width, height, user_id)

  start: ->
    self = @
    fn = ->
      (-> @ajax(@url_progress, @update_interval, {}, @drawBoard)).call(self)
    setInterval(fn, @update_interval)

  drawBoard: (data) ->
    #@renderer.updateBoard(data.board_users, data[@board_id], data.moves)
    board_users = [
      [1, 0, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 0]
      [0, 0, 0, 0, 0, 2]
    ]
    board_powers = [
      [50, 10, 10, 10, 10, 10]
      [10, 10, 10, 10, 10, 10]
      [10, 10, 10, 10, 10, 10]
      [10, 10, 10, 10, 10, 10]
      [10, 10, 10, 10, 10, 10]
      [10, 10, 10, 10, 10, 50]
    ]
    board_moves = [
      [5, 5, 4, 4]
    ]
    @renderer.updateBoard(board_users, board_powers, board_moves)

  ajax: (url, timeout, data, successFunc = ->) ->
    data['board_id'] = @board_id
    $.ajax
      url: url
      dataType: "json"
      data: data
      cache: false
      context: @
      timeout: timeout
      error: (xhr, msg) ->
      success: successFunc

@init_svg_game = (playground, width, height, user_id) ->
  if typeof(Engine) == "undefined"
    throw new Error("Render engine has not been included!")
    return
  return new GameEngine(playground, width, height, user_id)
