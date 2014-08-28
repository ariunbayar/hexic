_      = require('underscore')
whenjs = require('when')

class ServerThread
  # begin constants TODO differentiate
  cell_limit: 250
  move_limit: 489
  decr_map: [
    0, 0, 1, 2, 3, 3, 4, 4, 5, 5, #  0 -  9
    5, 5, 5, 6, 6, 6, 6, 6, 6, 6, # 10 - 19
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, # 20 - 29
  ]
  decr_min: 29
  decr_div: 10
  decr_add: 4.3
  # end of constants

  is_idle: true
  tick_count: 1

  constructor: ->
    setInterval(_.bind(@tick, @), SETTINGS.MASTER_PROCESSING_INTERVAL)
    @io = SIO.listen(require("http").createServer())
    @io.set("store", new SIO.RedisStore)

  tick: ->
    return unless @is_idle
    @is_idle = false
    @tick_count = (@tick_count % 3) + 1  # next tick

    p_game_ids = @get_game_ids()
    each_game_processing = whenjs.map(p_game_ids, (game_id)=>
      p_game_data = @get_game(game_id)
      p_game_data = @game_tick(p_game_data)
      @set_game(game_id, p_game_data)
      @notify_game_data(p_game_data)
    )

    each_game_processing.done(=> @is_idle = true)

  get_game_ids: ->
    return whenjs.promise (resolve, reject)->
      # TODO change to get from members
      REDIS.KEYS('game_*', (err, games)->
        return reject(err) if err
        games = _.filter(games, ((v)->/^game_[0-9a-f]+$/.test(v)))
        resolve(games)
        )

  get_game: (game_id)->
    return whenjs.promise (resolve, reject)->
      REDIS.HGETALL(game_id, (err, game_data)->
        return reject(err) if err
        return reject(new Error("Game not found")) unless game_data
        game_data =
          player_id_map: JSON.parse(game_data.player_id_map)
          players      : JSON.parse(game_data.players)
          powers       : JSON.parse(game_data.powers)
          move_queue   : JSON.parse(game_data.move_queue)
          moves        : JSON.parse(game_data.moves)
          moves4client : JSON.parse(game_data.moves4client)
        resolve(game_data)
        )

  set_game: (game_id, p_game_data)->
    p_game_data.then((_game_data)->
      game_data =
        player_id_map: JSON.stringify(_game_data.player_id_map)
        players      : JSON.stringify(_game_data.players)
        powers       : JSON.stringify(_game_data.powers)
        move_queue   : JSON.stringify(_game_data.move_queue)
        moves        : JSON.stringify(_game_data.moves)
        moves4client : JSON.stringify(_game_data.moves4client)
        id           : game_id
      REDIS.HMSET(game_id, game_data, (err, result)->
        throw err if err
      )
    )

  notify_game_data: (p_game_data)->
    p_game_data.then((game_data)=>
      @io.sockets.in(game_data.id).emit('data', 'board',
        game_data.players, game_data.powers, game_data.moves4client)
    )

  game_tick: (p_game_data) ->
    p_game_data.then((game_data)=>
      if @tick_count == 3
        game_data = @process_power_increment(game_data)
      game_data = @process_dirty_moves(game_data)
      game_data = @process_moves(game_data)
      return game_data
    )

  process_power_increment: (game_data)->
    powers = game_data.powers
    players = game_data.players
    for row, y in powers
      for power, x in row
        is_limit_reached = powers[y][x] < @cell_limit
        is_bla = powers[y][x] > 0  # TODO what is it?
        is_user = players[y][x] > 0
        if is_limit_reached and is_bla and is_user
          powers[y][x]++
    return game_data

  process_dirty_moves: (game_data)->
    # helper to cleanup move_queue to moves
    queue = game_data.move_queue
    moves = game_data.moves
    players = game_data.players
    get = (arr2d, [x, y])-> arr2d[y][x]

    while queue.length
      move = queue.shift()
      src_coord = move[0..1]
      dst_coord = move[2..3]
      src_cell = src_coord.join('_')
      dst_cell = dst_coord.join('_')

      # is it a removal move?
      if _.isEqual(src_coord, dst_coord)
        moves[src_cell] = [src_coord, [], {}]
        continue

      # so this actually is a move
      dst_info = [dst_cell].concat(dst_coord)
      moves[src_cell] = [src_coord, dst_info, {}]

      # destination cell has no moves yet?
      if dst_cell not in moves
        moves[dst_cell] = [dst_coord, [], {}]
        continue

      # its ok that destination has destination
      dst_has_dst = !!moves[dst_cell][1].length
      dsts_dst_is_src = moves[dst_cell][1][0] == src_cell
      is_same_user = get(players, src_coord) == get(players, dst_coord)
      move_is_reversing = dst_has_dst and dsts_dst_is_src and is_same_user

      # but is it nullifying move?
      if move_is_reversing
        # when move_is_reversing it is nullifying dest2src move
        moves[dst_cell] = [dst_coord, [], {}]

    return game_data

  process_moves: (game_data)->
    game_data = @_set_power_candidates(game_data)
    game_data = @_apply_power_candidates(game_data)
    return game_data

  _get_decrement: (number)->
    # main algorithm for decrement a cell when moving
    if @decr_min < number
      n = ~~((number / @decr_div) + @decr_add)
    else
      n = @decr_map[number]
    return n

  _set_power_candidates: (game_data)->
    # decrements cells and collect power candidates
    get_coord = (arr2d, [x, y])-> arr2d[y][x]
    set_coord = (arr2d, [x, y], v)-> arr2d[y][x] = v
    powers = game_data.powers
    moves = game_data.moves
    players = game_data.players
    game_data.moves4client = []  # will be populated along the way

    for cell_idx, move of moves
      # next iteration if has no destination
      continue unless move[1].length

      [src_coord, dest_info, candidates] = move
      dest_cell = dest_info[0]
      dest_coord = dest_info[1..2]
      src_user   = get_coord(players,  src_coord)
      src_power  = get_coord(powers, src_coord)
      dest_user  = get_coord(players,  dest_coord)
      dest_power = get_coord(powers, dest_coord)

      # extract the moving power
      moving_power = @_get_decrement(src_power)
      will_overflow = dest_power + moving_power > @move_limit
      if will_overflow and src_user == dest_user
        moving_power = @move_limit - dest_power

      # apply subtraction on source cell
      src_power -= moving_power
      set_coord(powers, src_coord, src_power)

      # apply subtraction on destination cell
      if src_user == dest_user
        # same user will be an increment
        dest_power += moving_power
        set_coord(powers, dest_coord, dest_power)
      else
        # Different user is a fight. Compute in `apply` step
        dest_candidates = moves[dest_cell][2]
        n = dest_candidates[src_user]? and dest_candidates[src_user] || 0
        n += moving_power
        dest_candidates[src_user] = n
      game_data.moves4client.push(src_coord.concat(dest_coord))

    return game_data

  _apply_power_candidates: (game_data)->
    # power candidates will be fought and winners apply
    get_coord = (arr2d, [x, y])-> arr2d[y][x]
    set_coord = (arr2d, [x, y], v)-> arr2d[y][x] = v
    moves = game_data.moves
    powers = game_data.powers
    players = game_data.players

    for cell_idx, move of moves
      [cell_coord, dest_info, candidates] = move

      cur_cell =
        user_id: get_coord(players, cell_coord)
        power: get_coord(powers, cell_coord)
        decr: 0  # increment or decrement amount on cur_cell.power
      winner = user_id: 0, power: 0

      # pick the winner iterating through candidates
      for user_id, moving_power of candidates
        if moving_power > cur_cell.power
          if moving_power > winner.power
            # set winner as this user
            winner.user_id = +user_id
            winner.power = moving_power
        else if moving_power > cur_cell.decr
          cur_cell.decr = moving_power

      # apply the winner
      if winner.user_id
        # this cell is mine. Remove the old move
        move[1] = []
        cur_cell.user_id = winner.user_id
        cur_cell.power -= winner.power - cur_cell.power
      else
        # no winner just decrement what old user had
        cur_cell.power -= cur_cell.decr
      set_coord(players, cell_coord, cur_cell.user_id)
      set_coord(powers, cell_coord, cur_cell.power)
      move[2] = {}

    return game_data

module.exports = ServerThread
