# TODO separate dev codes from prod
###
//# sourceMappingURL=server.js.map
###
require('source-map-support').install()

class Redis
  @get_client: ->
    unless @redis
      @redis = require('redis').createClient()
    @redis

  @handle_error: (err, data)->
    throw err if err

  @deprecated_handle_error: (callback_fn) ->
    # TODO only handle errors, don't do callback stuff
    (err, data) ->
      if err
        throw err
      else if callback_fn
        callback_fn(data)

class Model
  constructor: ->
    @redis = Redis.get_client()
    @$err = Redis.deprecated_handle_error
    @$e = Redis.handle_error

  @redis: Redis.get_client()
  @$err: Redis.deprecated_handle_error
  @$e: Redis.handle_error

class Player extends Model
  constructor: (@handshake_id) ->
    super()

  join_to: (game_id, callback) =>
    @redis.SADD "#{@handshake_id}_games", game_id, callback

  is_joined_to: (game_id, callback)=>
    @redis.SISMEMBER "#{@handshake_id}_games", game_id, (err, result)=>
      callback(err, result == 1)

  leave_from: (game_id, callback)=>
    @redis.SREM "#{@handshake_id}_games", game_id, callback

  get_games: (callback)=>
    @redis.SMEMBERS "#{@handshake_id}_games", callback

  @get_player: (handshake_id) =>
    new Player handshake_id

class Game extends Model
  constructor: (@game_id) ->
    super()

  join_player: (player, is_ready, callback) =>
    async.waterfall [
      @get_players
      , (players, cb)=>
        players[player.handshake_id] = is_ready
        json = JSON.stringify players
        @redis.SET "#{@game_id}_players", json, cb
      , (result, cb)=>
        if result == 'OK'
          player.join_to @game_id, cb
        else
          cb new Error "SET '#{@game_id}_players' returned '#{result}'"
    ], callback

  get_players: (callback)=>
    async.waterfall [
      (cb)=>
        @redis.GET "#{@game_id}_players", cb
      , (json_str, cb)=>
        try
          json = JSON.parse json_str
        catch e
          cb e
        finally
          cb null, json
    ], callback

  update_player: (player, is_ready, callback)=>
    async.waterfall [
      (cb)=>
        player.is_joined_to(@game_id, cb)
      , (is_joined, cb)=>
        if is_joined
          @get_players(cb)
        else
          msg = "Trying to update player when player '#{player.handshake_id}'
                 was not joined to '#{@game_id}'"
          cb(new Error(msg))
      , (players, cb)=>
        players[player.handshake_id] = is_ready
        json = JSON.stringify players
        @redis.SET "#{@game_id}_players", json, cb
      , (result, cb)=>
        if result == 'OK'
          cb()
        else
          cb new Error "SET '#{@game_id}_players' returned '#{result}'"
    ], callback

  remove_player: (player, callback)=>
    is_game_closed = false
    async.waterfall [
      @get_players
      , (players, cb)=>
        delete players[player.handshake_id]
        is_game_closed = _.keys(players).length == 0
        if is_game_closed
          Game.remove_game(@game_id, cb)
        else
          json = JSON.stringify players
          # TODO check if result == OK
          @redis.SET "#{@game_id}_players", json, cb
      , (result, cb)=>
        player.leave_from(@game_id, cb)
      , (is_player_left, cb)=>
        cb(null, is_game_closed)
    ], callback

  @create_game: (callback) =>
    game_id = null
    # TODO run within transaction
    async.waterfall [
      (cb)=>
        @redis.INCR 'game_count', cb
      , (count, cb)=>
        game_id = "game_#{count}"
        @redis.SADD 'games', game_id, cb
      , (is_added, cb)=>
        if is_added == 1
          @redis.SET "#{game_id}_players", '{}', cb
        else
          msg = "game '#{game_id}' already exists. Indicator was '#{is_added}'."
          cb new Error msg
      , (result, cb)=>
        cb null, new Game game_id
    ], callback

  @get_game: (game_id, callback) =>
    async.waterfall [
      (cb)=>
        @redis.SISMEMBER 'games', game_id, cb
      , (result, cb)=>
        if result == 1
          cb null, new Game game_id
        else
          cb new Error "game '#{game_id}' doesn't exist"
    ], callback

  @get_games: (callback)=>
    async.waterfall [
      (cb)=>
        @redis.SMEMBERS 'games', cb
      , (games, cb)=>
        games = if _.isArray games then games else []
        cb null, games
    ], callback

  @remove_game: (game_id, callback)=>
    async.waterfall [
      (cb)=>
        @redis.SREM "games", game_id, cb
      , (num_removed, cb)=>
        @redis.DEL "#{game_id}_players", cb
    ], callback

class LobbyServer
  init: (@cache, @socket, @sockets) ->
    @notify_games()
    @socket.on 'host_game', @host_game
    @socket.on 'join_game', @join_game
    @socket.on 'tick_ready', @tick_ready
    @socket.on 'disconnect', @disconnect
    @$err = Redis.deprecated_handle_error

  disconnect: =>
    # TODO console.log 'disconnect', @socket.id, @socket.handshake.session_id
    player = Player.get_player(@socket.id)
    async.waterfall [
      (cb)=>
        player.get_games(cb)
      , (game_ids, cb)=>
        for game_id in game_ids
          game = null
          async.waterfall [
            (cb)=>
              Game.get_game(game_id, cb)
            , (_game, cb)=>
              game = _game
              game.remove_player(player, cb)
            , (is_game_closed, cb)=>
              if is_game_closed
                @notify_games true
              else
                @notify_game_status game
          ], @$e
    ], @$e

  notify_games: (broadcast) =>
    async.waterfall [
      Game.get_games
      , (games, cb)=>
        @socket.emit 'games', games
        if broadcast
          @socket.broadcast.emit 'games', games
    ], @$e

  host_game: =>
    game = null
    async.waterfall [
      Game.create_game
      , (_game, cb)=>
        @notify_games true
        game = _game
        player = Player.get_player @socket.id
        game.join_player player, false, cb
      , (cb)=>
        @notify_game_status game
        @socket.join game.game_id
    ], @$e

  notify_game_status: (game) =>
    async.waterfall [
      game.get_players
      , (players, cb)=>
        @sockets.in(game.game_id).emit 'game_status', [game.game_id, players]
    ], @$e

  join_game: ([game_id, is_ready]) =>
    game = null
    async.waterfall [
      (cb)=>
        Game.get_game(game_id, cb)
      , (_game, cb)=>
        game = _game
        player = Player.get_player @socket.id
        game.join_player player, !!is_ready, cb
      , (cb)=>
        @notify_game_status game
        @socket.join game.game_id
    ], @$e

  tick_ready: ([game_id, is_ready]) =>
    game = null
    async.waterfall [
      (cb)=>
        Game.get_game(game_id, cb)
      , (_game, cb)=>
        game = _game
        player = Player.get_player @socket.id
        game.update_player player, !!is_ready, cb
      , (result, cb)=>
        @notify_game_status game
        @socket.join game.game_id
    ], @$e

class SocketIOApp
  init: (port) ->
    io = sio.listen(port)
    cache = Redis.get_client()
    io.configure ->
      io.set('store', new sio.RedisStore)
      io.set('log level', 2)
      io.set 'authorization', (handshakeData, callback) ->
        cookie = handshakeData.headers.cookie
        match = /PHPSESSID=([\w\d]+);/.exec cookie
        if match
          handshakeData.session_id = match[1]
          callback null, true
        else
          callback new Error "Invalid cookie '#{cookie}'", false
    io.sockets.on 'connection', (socket) ->
      (new LobbyServer).init(cache, socket, io.sockets)

class GameServer
  is_idle: true
  init: (cache, interval) ->
    #@cache = cache
    @interval = interval
    @io = sio.listen(require('http').createServer())
    @io.set('store', new sio.RedisStore)

  start: ->
    self = @
    @timer = setInterval((-> self.process.call self), @interval)

  process: ->
    return unless @is_idle
    @is_idle = false
    #console.log('processing games!')
    #@io.sockets.emit('message', 'message from main thread')
    @is_idle = true

  stop: ->
    clearInterval @timer

cluster = require 'cluster'
sio     = require 'socket.io'
async   = require 'async'
_       = require 'underscore'

if cluster.isMaster
  cpu_count = require('os').cpus().length
  for i in [0...cpu_count]
    cluster.fork()
    console.log('Creating new fork.')
  cluster.on 'exit', (worker) ->
    console.log('Worker ' + worker.id + ' died.')
    cluster.fork()
  game = new GameServer
  redis = Redis.get_client()
  game.init(redis, 500)
  game.start()
else
  (new SocketIOApp).init(8001)
  console.log('Worker ' + cluster.worker.id + ' running!')
