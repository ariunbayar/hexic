suspend = require('suspend')
resume  = suspend.resume
_       = require('underscore')

class Player
  @get_player: (id) ->
    return new Player(id)

  constructor: (@id) ->
    #_.bindAll(@, 'join_to')
    @__games = "#{@id}_games"

  get_games: (callback)->
    REDIS.SMEMBERS(@__games, callback)

  join_to: suspend.async (game_id)->
    # leave current games
    games = yield @get_games(resume())
    if _.isArray(games) && games.length
      num_removed = yield REDIS.SREM([@__games].concat(games), resume())
      if num_removed != games.length
        throw new Error("Removing '#{games}' failed. Removed #{num_removed}")
    # join to game
    num_added = yield REDIS.SADD(@__games, game_id, resume())
    if num_added != 1
      msg = "Couldn't add '#{game_id}' to #{@__games}. Result #{is_added}."
      throw new Error(msg)
    return games

  #leave_from: (games, callback)->
    #callback() unless _.isArray(games) && games.length
    #REDIS.SREM([@__games].concat(games), callback)

  #is_joined_to: (game_id, callback)=>
    #@redis.SISMEMBER "#{@id}_games", game_id, (err, result)=>
      #callback(err, result == 1)



module.exports = Player
