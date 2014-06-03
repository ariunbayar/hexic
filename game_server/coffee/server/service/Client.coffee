suspend = require('suspend')
resume  = suspend.resume
_       = require('underscore')
Game    = require('../model/Game')
Player  = require('../model/Player')

class Client
  constructor: (@socket)->
    console.log('connect', @socket.id)
    _.bindAll(@, 'host_game')
    @notify_current_games()
    @socket.on('host_game', @host_game)
    #@socket.on 'join_game', @join_game
    #@socket.on 'tick_ready', @tick_ready
    #@socket.on 'disconnect', @disconnect

  notify_current_games: suspend (to_all)->
    games = yield Game.get_games(resume())
    @socket.emit('games', games)
    @socket.broadcast.emit('games', games) if to_all

  host_game: suspend ->
    game = yield Game.create_game(resume())
    player = Player.get_player(@socket.id)
    games_left = yield player.join_to(game.game_id, resume())
    yield Game.remove_players(games_left, [@socket.id], resume())
    yield game.join_players([player.id], false, resume())
    @notify_current_games(true)

  disconnect: ->
    console.log('disconnect', @socket.id)

module.exports = Client
