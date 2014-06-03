@gameController = ($scope, $interval)->
  scopeWrap = (fn)-> (args...)-> $scope.$apply -> fn.apply(null, args)
  socket = io.connect window.server_address

  $scope.games = []
  $scope.game_id = null
  $scope.players = []
  $scope.is_ready = false
  $scope.session_id = null

  init = ->
    $scope.$watch 'is_ready', (is_ready)->
      socket.emit 'tick_ready', [$scope.game_id, is_ready]

  $scope.host_new = -> socket.emit 'host_game'
  $scope.join = (game_id)->
    $scope.is_ready = false
    socket.emit 'join_game', [game_id, $scope.is_ready]

  socket.on 'connect', scopeWrap ->
    $scope.session_id = socket.socket.sessionid
    init()
  socket.on 'games', scopeWrap (games)->
    $scope.games = games
  socket.on 'game_status', scopeWrap ([game_id, players])->
    $scope.game_id = game_id
    $scope.players = players
  socket.on 'error', (reason) ->
    console.error('Unable to connect server', reason)

  do_something = ->
    console.log 'doing something', new Date / 1000
  $interval(do_something, 2000)
