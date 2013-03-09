retrieveBoardURL = "/game/board/"
retrieveProgressURL = "/game/progress/"
moveURL = "/game/move/"
progressInterval = 1000


@initBoard = ->
  me = $(this)
  board_id = me.attr("id")
  hexEnv.ajax(retrieveBoardURL, 2000, {board_id: board_id},
    (json) ->
      user_id = $("#user_id").val()
      hexEnv.initBoard(user_id, json.board_id, json[json.board_id],
                       json.board_users, movethem)
      showBoardProgress(json.board_id)
      return
  )
  return


###
  Shows game progress on the board.
  Moves, counts and colors
###
@showBoardProgress = (board_id) ->
  hexEnv.ajax(retrieveProgressURL, 1000, board_id: board_id,
    (json) ->
      hexEnv.drawBoard(json.moves, json[json.board_id], json.board_users)
      return
  )
  setTimeout("showBoardProgress(\"" + board_id + "\")", progressInterval)
  return


movethem = (from, to, board_id) ->
  params = {
    fx: from.x
    fy: from.y
    tx: to.x
    ty: to.y
    user_id: $("#user_id").val()
    board_id: board_id
  }
  hexEnv.ajax(moveURL, 3000, params, ->)
  return
