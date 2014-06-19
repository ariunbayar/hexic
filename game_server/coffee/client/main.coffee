@gameController = ($scope, $interval)->
  scopeWrap = (fn)-> (args...)-> $scope.$apply -> fn.apply(null, args)
  socket = io.connect window.server_address

  $scope.games = []
  $scope.player_id = null
  svg_game = null

  reset_game_settings = ->
    $scope.game_id = null
    $scope.players = {}
    $scope.is_ready = false
    $scope.is_host = false
    $scope.is_game_started = false

  init = ->
    reset_game_settings()

    $scope.$watch 'is_ready', (is_ready)->
      return unless $scope.game_id
      socket.emit('tick_ready', $scope.game_id, is_ready)
      $scope.players[$scope.player_id] = is_ready

  $scope.host_new = (e, v)->
    reset_game_settings()
    socket.emit('host_game', (new_game_id)->
      $scope.game_id = new_game_id
      $scope.players[$scope.player_id] = $scope.is_ready
      $scope.is_host = true
      )

  $scope.join = (game_id)->
    reset_game_settings()
    socket.emit('join_game', game_id, $scope.is_ready, scopeWrap (players)->
      $scope.game_id = game_id
      $scope.players = players
      $scope.players[$scope.player_id] = $scope.is_ready
      )

  $scope.start_game = ->
    socket.emit('start_game', $scope.game_id, _.keys($scope.players))

  $scope.is_room_ready = ->
    return false unless $scope.game_id
    return false unless _.size($scope.players) > 1
    return _.all($scope.players)

  socket.on 'connect', scopeWrap ->
    $scope.player_id = socket.socket.sessionid
    init()

  socket.on 'error', (reason) ->
    console.error('Unable to connect server', reason)

  socket.on 'games', scopeWrap (games)->
    $scope.games = games

  socket.on 'join', scopeWrap (player_id, is_ready)->
    $scope.players[player_id] = is_ready
    socket.emit('tick_ready', $scope.game_id, $scope.is_ready)

  socket.on 'leave', scopeWrap (player_id)->
    delete $scope.players[player_id]

  socket.on 'data', scopeWrap (type, args...)->
    switch type
      when 'ready_state'
        [player_id, is_ready] = args
        $scope.players[player_id] = is_ready
        #alert(type + "\n" + player_id + "\n" + is_ready)
      when 'start_game'
        [player_idx] = args
        #svg_game = new Engine('#game', 350, 300, player_idx)
        svg_game = new Engine('#game', 750, 600, player_idx)
        svg_game.move = svg_game_move
        $scope.is_game_started = true
      when 'board'
        [board_users, board_powers, board_moves] = args
        if $scope.is_game_started
          svg_game.updateBoard(board_users, board_powers, board_moves)

  svg_game_move = (fx, fy, tx, ty)->
    socket.emit('move', $scope.game_id, fx, fy, tx, ty)
