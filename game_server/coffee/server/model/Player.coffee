suspend = require('suspend')
resume  = suspend.resume
_       = require('underscore')

class Player
  @get_player: (id) ->
    return new Player(id)

  constructor: (@id) ->
    #_.bindAll(@, 'join_to')
    @__games = "games_for_#{@id}"

  get_games: (callback)->
    REDIS.SMEMBERS(@__games, callback)

  join_to: suspend.async (game_id)->
    games = yield @get_games(resume())
    yield @leave_from(games, resume())
    # join to game
    num_added = yield REDIS.SADD(@__games, game_id, resume())
    if num_added != 1
      msg = "Couldn't add '#{game_id}' to #{@__games}. Result #{is_added}."
      throw new Error(msg)
    return games

  leave_from: (games, callback)->
    return callback() unless _.isArray(games) and games.length
    REDIS.SREM([@__games].concat(games), (err, num_removed)->
      if err == null and num_removed != games.length
        err = new Error("Removing '#{games}' failed. Removed #{num_removed}")
      callback(err)
    )

  #is_joined_to: (game_id, callback)=>
    #@redis.SISMEMBER "#{@id}_games", game_id, (err, result)=>
      #callback(err, result == 1)



module.exports = Player
