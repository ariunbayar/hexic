window.init = (srv_addr) ->
  ask_worker_id = ->
    socket.emit "workerid", {}
  socket = io.connect srv_addr
  socket.on "news", (data) ->
    console.log data
  socket.on "workeridresult", (data) ->
    console.log "worker id is: ", data
    document.getElementById("wid").innerHTML = "worker id is: " + data
