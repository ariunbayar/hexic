@gameController = ($scope, $interval)->
  scopeWrap = (fn)-> (args...)-> $scope.$apply -> fn.apply(null, args)
  socket = io.connect window.server_address

  $scope.games = []
  $scope.player_id = null

  reset_game_settings = ->
    $scope.game_id = null
    $scope.players = {}
    $scope.is_ready = false

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
      )

  $scope.join = (game_id)->
    reset_game_settings()
    socket.emit('join_game', game_id, $scope.is_ready, scopeWrap (players)->
      $scope.game_id = game_id
      $scope.players = players
      $scope.players[$scope.player_id] = $scope.is_ready
      )

  $scope.game_is_valid = ->
    $scope.game_id in $scope.games

  socket.on 'connect', scopeWrap ->
    $scope.player_id = socket.socket.sessionid
    init()

  socket.on 'error', (reason) ->
    console.error('Unable to connect server', reason)

  socket.on 'games', scopeWrap (games)->
    $scope.games = games

  socket.on 'join', scopeWrap (player_id, is_ready)->
    $scope.players[player_id] = is_ready

  socket.on 'leave', scopeWrap (player_id)->
    delete $scope.players[player_id]

  socket.on 'data', scopeWrap (type, args...)->
    switch type
      when 'ready_state'
        [player_id, is_ready] = args
        $scope.players[player_id] = is_ready

  $interval((->true), 2000)
