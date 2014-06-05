debug   = require('debug')('hexic-play')
suspend = require('suspend')
resume  = suspend.resume
_       = require('underscore')
Game    = require('../model/Game')
Player  = require('../model/Player')

class Client
  constructor: (@socket, @sockets)->
    debug('Connect from: ' + @socket.id)
    _.bindAll(@, 'host_game', 'join_game', 'disconnect')
    @notify_current_games()
    @socket.on('host_game', @host_game)
    @socket.on('join_game', @join_game)
    #@socket.on 'tick_ready', @tick_ready
    #@dummy = 123  # TODO debug only
    #return console.log 'invalid scope' unless @dummy == 123

  notify_current_games: suspend (to_all)->
    games = yield Game.get_games(resume())
    @socket.emit('games', games)
    @socket.broadcast.emit('games', games) if to_all

  notify_game_status: suspend (game)->
    players = yield game.get_players(resume())
    @sockets
      .in(game.game_id)
      .emit('game_status', [game.game_id, players])

  host_game: suspend ->
    game = yield Game.create_game(resume())
    yield @join_game([game.game_id, false], game, resume())
    @notify_current_games(true)

  join_game: suspend ([game_id, is_ready], game, callback) ->
    player = Player.get_player(@socket.id)
    games_left = yield player.join_to(game_id, resume())
    games_removed = yield Game.remove_players(
      games_left, [player.id], @socket, resume())
    games_updated = _.difference(games_left, games_removed)
    game = yield Game.get_game(game_id, resume()) unless game
    yield game.join_players([player.id], !!is_ready, @socket, resume())
    @notify_game_status(game)
    @notify_current_games(true) if games_removed.length
    for game_id in games_updated
      @notify_game_status(yield Game.get_game(game_id, resume()))
    if callback  # called from host_game
      callback()

  disconnect: suspend ->
    debug('Disconnect from: ' + @socket.id)
    player = Player.get_player(@socket.id)
    games = yield player.get_games(resume())
    yield player.leave_from(games, resume())
    games_removed = yield Game.remove_players(
      games, [player.id], @socket, resume())
    games_updated = _.difference(games, games_removed)
    @notify_current_games(true) if games_removed.length
    for game_id in games_updated
      @notify_game_status(yield Game.get_game(game_id, resume()))

module.exports = Client
