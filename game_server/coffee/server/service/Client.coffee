debug   = require('debug')('hexic-play')
_       = require('underscore')

class Client
  constructor: (@socket, @sockets)->
    @rooms = @socket.manager.rooms
    @roomClients = @socket.manager.roomClients
    @socket.on('host_game',  _.bind(@receive_host_game, @))
    @socket.on('join_game',  _.bind(@receive_join_game, @))
    @socket.on('tick_ready', _.bind(@receive_tick_ready, @))
    @socket.on('start_game', _.bind(@receive_start_game, @))
    @socket.on('move',       _.bind(@receive_move, @))
    @player_games = []

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
    debug 'joined by', player_id
    @_leave_old_games(player_id)
    @socket.join(game_id)
    # notify existing players
    @sockets.in(game_id).emit('join', player_id, is_ready)
    # notify the player about current_players
    client_callback(@_get_players_for(game_id))

    player_ids = _.keys(@_get_players_for(game_id))
    if _.size(game_id, player_ids) >= 2
      @receive_start_game(game_id, player_ids)

  receive_tick_ready: (game_id, is_ready)->
    player_id = @socket.id
    # notify ready state within room
    @sockets.in(game_id).emit('data', 'ready_state', player_id, is_ready)
    debug game_id, is_ready, player_id

  receive_start_game: (game_id, player_ids)->
    # only 2 players allowed
    return unless _.isArray(player_ids) and _.size(player_ids) >= 2
    player_1_idx = 1
    player_2_idx = 2
    player_ids = {1: player_ids[0], 2: player_ids[1]}

    # prepare the board
    size = 5
    players = (0  for x in [1..size] for i in [1..size])
    powers  = (10 for x in [1..size] for i in [1..size])

    set_player_location = (x, y, idx, power)->
      players[y][x] = idx
      powers[y][x] = power
    set_player_location(0, 0, player_1_idx, 50)
    set_player_location(size-1, size-1, player_2_idx, 50)

    # create the game
    game_data = {
      player_id_map: JSON.stringify(player_ids)
      players      : JSON.stringify(players)
      powers       : JSON.stringify(powers)
      move_queue   : JSON.stringify([])
      moves        : JSON.stringify({})
      moves4client : JSON.stringify([])
      id           : game_id
    }
    REDIS.HMSET(game_id, game_data, (err, result)=>
      throw err if err
      REDIS.EXPIRE(game_id, 300)  # TODO idle game duration from settings
      for idx, player_id of player_ids
        @sockets.socket(player_id).emit('data', 'start_game', +idx)
    )

  receive_move: (game_id, fx, fy, tx, ty)->
    ### TODO validate the move
      def move_valid(move, board, user_id, users):
          (x, y, x1, y1) = move
          xx = x + (0 if y % 2 else 1)

          is_valid = ((x1 - 1 == x) and (y1 == y))\
                    or ((x1 == xx) and (y1 - 1 == y))\
                    or ((x1 + 1 == xx) and (y1 - 1 == y))\
                    or ((x1 + 1 == x) and (y1 == y))\
                    or ((x1 + 1 == xx) and (y1 + 1 == y))\
                    or ((x1 == xx) and (y1 + 1 == y))\
                    or (x == x1 and y == y1) # not move, a removal
          is_valid = is_valid and (users[y][x][0] == user_id)
          return is_valid
    ###
    REDIS.HGET(game_id, 'move_queue', (err, move_queue)=>
      throw err if err
      return unless move_queue
      REDIS.HGET(game_id, 'winner_id', (err, winner_id)->
        return if winner_id
        move_queue = JSON.parse(move_queue)
        move_queue.push([+fx, +fy, +tx, +ty])
        move_queue = JSON.stringify(move_queue)
        REDIS.HSET(game_id, 'move_queue', move_queue, (err, result)->
          throw err if err
          REDIS.EXPIRE(game_id, 300)  # TODO idle game duration from settings
        )
      )
    )

module.exports = Client
