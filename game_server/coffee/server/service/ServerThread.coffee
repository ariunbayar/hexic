class ServerThread
  is_idle: true
  worker_conn_channel: "game_status"
  constructor: ->
    setInterval(@process, SETTINGS.MASTER_PROCESSING_INTERVAL)
    @io = SIO.listen(require("http").createServer())
    @io.set("store", new SIO.RedisStore)

  notify_workers: (msg) ->
    @io.sockets.emit("games", msg)

  process: ->
    return unless @is_idle
    @is_idle = false
    @notify_workers()
    @is_idle = true

module.exports = ServerThread
