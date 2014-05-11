console.log('===========> application is running')
runapp = ->
  fs = require('fs')
  handler = (req, res) ->
    fs.readFile "#{__dirname}/../index.html",
    (err, data) ->
      if err
        res.writeHead(500)
        return res.end('Error loading index.html')
      res.writeHead(200)
      res.end(data)

  app = require('connect')()
  if process.argv.length > 2 and process.argv[2] == 'debug'
    app.use(require('connect-livereload')())
  app.use(handler)
  server = require('http').createServer(app)
  sio = require('socket.io')
  io = sio.listen(server)
  io.set('store', new sio.RedisStore)
  io.set('log level', 2)

  io.sockets.on 'connection', (socket) ->
    socket.emit('news', 'connected to: ' + cluster.worker.id)
    socket.on 'workerid', (data) ->
      socket.emit('workeridresult', cluster.worker.id)
      socket.broadcast.emit('workeridresult', "[#{cluster.worker.id}]")

  server.listen(8000)

runSocketioApp = (port) ->
  sio = require('socket.io')
  io = sio.listen(port)
  io.set('store', new sio.RedisStore)
  io.set('log level', 2)
  io.sockets.on 'connection', (socket) ->
    socket.emit('news', 'connected to: ' + cluster.worker.id)
    socket.on 'workerid', (data) ->
      socket.emit('workeridresult', cluster.worker.id)
      socket.broadcast.emit('workeridresult', "[#{cluster.worker.id}]")

cluster = require('cluster')

if cluster.isMaster
  cpu_count = require('os').cpus().length
  for i in [0...cpu_count]
    cluster.fork()
    console.log('Creating new fork.')
  cluster.on 'exit', (worker) ->
    console.log('Worker ' + worker.id + ' died.')
    cluster.fork()
else
  runSocketioApp(8001)
  console.log('Worker ' + cluster.worker.id + ' running!')
