suspend = require('suspend')
resume  = suspend.resume
_       = require('underscore')

class Game
  @__games: 'games'
  @get_games: suspend.async ->
    games = yield REDIS.SMEMBERS('games', resume())
    if _.isArray(games) then games else []

  @create_game: suspend.async ->
    count = yield REDIS.INCR('game_count', resume())
    game_id = "game_#{count}"
    is_added = yield REDIS.SADD('games', game_id, resume())
    if is_added == 1
      result = yield REDIS.SET("#{game_id}_players", '{}', resume())
      if result == 'OK'
        return new Game(game_id)
      err = "Couldn't set #{game_id}_players. Result was '#{result}'."
    else
      err = "game '#{game_id}' already exists. Indicator was '#{is_added}'."
    throw new Error(error_msg)

  @remove_players: suspend.async (game_ids, player_ids)->
    # removes players from given games, purges the game when empty
    return unless _.isArray(game_ids)   && game_ids.length
    return unless _.isArray(player_ids) && player_ids.length
    k_game_players = [game_ids].map((game_id)-> "#{game_id}_players")
    v_game_players = yield REDIS.MGET(k_game_players, resume())
    empty_game_ids = []
    empty_games = []
    update_args = []
    for key, idx in k_game_players
      players = _.omit(JSON.parse(v_game_players[idx]), player_ids)
      if _.keys(players).length == 0
        empty_game_ids.push(game_ids[idx])
        empty_games.push(key)
      else
        update_args.push(key, JSON.stringify(players))
    # TODO use transaction
    if update_args.length
      result = yield REDIS.MSET(update_args, resume())
      if result != 'OK'
        throw new Error("Couldn't set #{update_args}. Result #{result}")
    if empty_games.length
      num_deleted = yield REDIS.DEL(empty_games, resume())
      if num_deleted != empty_games.length
        msg = "Couldn't remove '#{empty_games}'. Removed #{num_deleted}"
        throw new Error(msg)
      num_removed = yield REDIS.SREM([@__games].concat(empty_game_ids), resume())
      if num_removed != empty_game_ids.length
        throw new Error("Removing '#{empty_game_ids}' from '#{@__games}'
                         failed. Removed #{num_removed}")

  constructor: (@game_id) ->
    @__players = "#{@game_id}_players"

  #get_players: suspend.async ->
    #return yield REDIS.GET("#{@game_id}_players", resume())

  join_players: suspend.async (player_id, is_ready) ->
    players = yield REDIS.GET(@__players, resume())
    players = JSON.parse(players)
    players[player_id] = !!is_ready  # convert to boolean to be safe
    result = yield REDIS.SET(@__players, JSON.stringify(players), resume())
    if result != 'OK'
      throw new Error("SET '#{@__players}' returned '#{result}'")

  #update_player: (player, is_ready, callback)=>
    #async.waterfall [
      #(cb)=>
        #player.is_joined_to(@game_id, cb)
      #, (is_joined, cb)=>
        #if is_joined
          #@get_players(cb)
        #else
          #msg = "Trying to update player when player '#{player.id}'
                 #was not joined to '#{@game_id}'"
          #cb(new Error(msg))
      #, (players, cb)=>
        #players[player.id] = is_ready
        #json = JSON.stringify players
        #@redis.SET "#{@game_id}_players", json, cb
      #, (result, cb)=>
        #if result == 'OK'
          #cb()
        #else
          #cb new Error "SET '#{@game_id}_players' returned '#{result}'"
    #], callback

  #remove_player: (player, callback)=>
    #is_game_closed = false
    #async.waterfall [
      #@get_players
      #, (players, cb)=>
        #delete players[player.id]
        #is_game_closed = _.keys(players).length == 0
        #if is_game_closed
          #Game.remove_game(@game_id, cb)
        #else
          #json = JSON.stringify players
          ## TODO check if result == OK
          #@redis.SET "#{@game_id}_players", json, cb
      #, (result, cb)=>
        #player.leave_from(@game_id, cb)
      #, (is_player_left, cb)=>
        #cb(null, is_game_closed)
    #], callback

  #@get_game: (game_id, callback) =>
    #async.waterfall [
      #(cb)=>
        #@redis.SISMEMBER 'games', game_id, cb
      #, (result, cb)=>
        #if result == 1
          #cb null, new Game game_id
        #else
          #cb new Error "game '#{game_id}' doesn't exist"
    #], callback

  #@remove_game: (game_id, callback)=>
    #async.waterfall [
      #(cb)=>
        #@redis.SREM "games", game_id, cb
      #, (num_removed, cb)=>
        #@redis.DEL "#{game_id}_players", cb
    #], callback

module.exports = Game
