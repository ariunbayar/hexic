_ = require('underscore')

class ServerThread
  is_idle: true
  constructor: ->
    setInterval(_.bind(@process, @), SETTINGS.MASTER_PROCESSING_INTERVAL)
    @io = SIO.listen(require("http").createServer())
    @io.set("store", new SIO.RedisStore)

  process: ->
    return unless @is_idle
    @is_idle = false
    #@notify_workers(['def', 'abc'])
    @is_idle = true

  notify_workers: (msg) ->
    @io.sockets.emit("games", msg)

module.exports = ServerThread
