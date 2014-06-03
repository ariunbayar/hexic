cluster = require("cluster")

spawn_master = ->
  ServerThread = require("./service/ServerThread")
  new ServerThread()

  cpu_count = require("os").cpus().length
  cluster.on("exit", (worker) -> cluster.fork())
  cluster.fork() for i in [1..cpu_count]

spawn_worker = (worker) ->
  ClientThread = require("./service/ClientThread")
  new ClientThread()

setup_global = ->
  require('source-map-support').install({})
  sio      = require("socket.io")
  settings = require("./settings")
  redis    = require("redis")
  redis.debug_mode = settings.DEBUG

  global.SETTINGS      = settings
  global.REDIS         = redis.createClient()
  global.SIO           = sio
  global.ERROR_HANDLER = (err, data) -> throw err  if err

setup_global()
if cluster.isMaster
  spawn_master()
else
  spawn_worker(cluster.worker)
