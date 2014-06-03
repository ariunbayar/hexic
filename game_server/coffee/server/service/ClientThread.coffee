suspend = require('suspend')
resume  = suspend.resume
_       = require('underscore')
Client  = require('./Client')

class ClientThread
  clients: {}
  constructor: ->
    _.bindAll(@, 'client_connect')
    @io = SIO.listen(SETTINGS.WORKER_LISTEN_PORT)
    @io.set('store', new SIO.RedisStore)
    @io.set('log level', SETTINGS.SOCKETIO_LOGLEVEL)
    @io.set('authorization', @client_authorize)
    @io.sockets.on('connection', @client_connect)

  client_authorize: (handshakeData, callback)->
    cookie = handshakeData.headers.cookie
    match = /PHPSESSID=([\w\d]+)/.exec(cookie)
    if match
      handshakeData.session_id = match[1]
      callback(null, true)
    else
      callback(throw new Error("Invalid cookie '" + cookie + "'"))

  client_connect: (socket)->
    @clients[socket.id] = new Client(socket)
    socket.on("disconnect", _.bind(@client_disconnect, @, socket))

  client_disconnect: (socket)->
    @clients[socket.id].disconnect()
    delete @clients[socket.id]

module.exports = ClientThread
