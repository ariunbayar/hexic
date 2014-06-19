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

@init_svg_game = (playground, width, height, user_id) ->
  if typeof(Engine) == "undefined"
    throw new Error("Render engine has not been included!")
    return
  return new GameEngine(playground, width, height, user_id)
