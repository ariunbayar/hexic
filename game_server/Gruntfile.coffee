module.exports = (grunt) ->
  config = require './local_settings'
  grunt.initConfig
    config: config
    coffee:
      compile:
        options:
          sourceMap: false  # TODO true
        files:
          "app/js/client.js": "coffee/client.coffee"
          "app/js/GameEngine.js": "coffee/GameEngine.coffee"
      compile_server:
        options:
          sourceMap: true
        files:
          "app/js/server.js": "coffee/server.coffee"
    sass:
      compile:
        files:
          "app/css/style.css": "sass/style.scss"
    watch:
      livereload:
        options:
          livereload: true
        files: [
          "app/index.html",
          "app/js/lib/*.js",
          "app/js/client.js",
          "app/js/GameEngine.js",
          "app/css/*.css",
        ]
      coffee_server:
        options:
          nospawn: true
        files: ["coffee/server.coffee"]
        tasks: ["coffee:compile_server", "server:reload"]
      coffee:
        files: ['coffee/client.coffee', 'coffee/GameEngine.coffee']
        tasks: ['coffee:compile']
      sass:
        files: ["sass/style.scss"]
        tasks: ['sass:compile']
    connect:
      options:
        open: true
        port: 8000
      server:
        options:
          livereload: true
          base: ["app", "bower_components"]

  child_process = null
  server_reloading = false
  spawn_node_app = ->
    grunt.util.spawn
      cmd: 'node'
      args: ["app/js/server.js", "debug"]
      opts: {stdio: 'inherit'}
    , (error, result, code) ->
      console.log('>>> Node application stopped!!!')
  spawn_redis = ->
    grunt.util.spawn
      cmd: config.redis.cmd
      args: config.redis.args
      opts: {stdio: 'inherit'}
    , (error, result, code) ->
      console.log('>>> Redis stopped!!!')
      unless server_reloading
        grunt.task.run 'server:reload'

  grunt.registerTask "server", ->
    child_process = spawn_node_app()
  grunt.registerTask "server:reload", ->
    server_reloading = true
    child_process.kill() if child_process
    console.log(">>> Restarting node application!!!")
    setTimeout ->
      child_process = spawn_node_app()
      server_reloading = false
    , 2000
  grunt.registerTask "redis", ->
    spawn_redis()

  grunt.registerTask("default",
    ["coffee", "sass", "redis", "connect", "server", "watch"])

  grunt.loadNpmTasks("grunt-contrib-watch")
  grunt.loadNpmTasks("grunt-contrib-coffee")
  grunt.loadNpmTasks("grunt-contrib-connect")
  grunt.loadNpmTasks("grunt-contrib-sass")
