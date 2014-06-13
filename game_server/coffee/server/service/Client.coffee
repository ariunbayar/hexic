debug   = require('debug')('hexic-play')
_       = require('underscore')

class Client
  constructor: (@socket, @sockets)->
    @rooms = @socket.manager.rooms
    @roomClients = @socket.manager.roomClients
    @socket.on('host_game',  _.bind(@receive_host_game, @))
    @socket.on('join_game',  _.bind(@receive_join_game, @))
    @socket.on('tick_ready', _.bind(@receive_tick_ready, @))

  _get_game_ids: (rooms)->
    fn = (memo, v, k)-> if k then memo.concat(k[1..]) else memo
    _.reduce(rooms, fn, [])

  _get_player_games: (player_id)->
    return @_get_game_ids(@roomClients[player_id])

  _get_games: ->
    return @_get_game_ids(@rooms)

  _notify_games: ->
    @sockets.emit('games', @_get_games())

  _leave_old_games: (player_id, notify_games = true)->
    cur_games = @_get_player_games(player_id)
    num_empty_games = 0
    for game_id in cur_games
      @socket.leave(game_id)
      @sockets.in(game_id).emit('leave', player_id)
      num_empty_games++ unless _.size(@rooms['/' + game_id])
    @_notify_games() if num_empty_games and notify_games

  _get_players_for: (game_id)->
    fn = (memo, player_id)->
      # TODO ready state defaulting to false?
      memo[player_id] = false
      return memo
    return _.reduce(@rooms['/' + game_id], fn, {})

  receive_connect: ->
    debug('Connect from: ' + @socket.id)
    @socket.emit('games', @_get_games())

  receive_disconnect: ->
    player_id = @socket.id
    debug('Disconnect from: ' + player_id)
    @_leave_old_games(player_id)

  receive_host_game: (client_callback)->
    @_leave_old_games(@socket.id, false)
    # join to new game
    REDIS.INCR('game_count', (err, game_count)=>
      throw err if err
      game_id = 'game_' + game_count
      @socket.join(game_id)
      # notify everyone about the new game
      @_notify_games()
      client_callback(game_id)
    )

  receive_join_game: (game_id, is_ready, client_callback) ->
    player_id = @socket.id
    @_leave_old_games(player_id)
    @socket.join(game_id)
    # notify existing players
    @sockets.in(game_id).emit('join', player_id, is_ready)
    # notify the player about current_players
    client_callback(@_get_players_for(game_id))

  receive_tick_ready: (game_id, is_ready)->
    player_id = @socket.id
    # notify ready state within room
    @sockets.in(game_id).emit('data', 'ready_state', player_id, is_ready)
    debug game_id, is_ready

module.exports = Client
