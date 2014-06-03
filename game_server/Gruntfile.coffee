module.exports = (grunt) ->
  config = require './local_settings'
  grunt.initConfig
    config: config
    coffee:
      server:
        options:
          sourceMap: true
        expand  : true,
        cwd     : 'coffee/server/',
        src     : ['**/*.coffee'],
        dest    : 'app/server/',
        ext     : '.js'
      client:
        options:
          sourceMap: true
        expand  : true,
        cwd     : 'coffee/client/',
        src     : ['**/*.coffee'],
        dest    : 'app/client/js/',
        ext     : '.js'
    sass:
      compile:
        expand  : true,
        flatten : true,
        cwd     : 'sass/',
        src     : ['*.scss'],
        dest    : 'app/client/css/',
        ext     : '.css'
    watch:
      livereload:
        options:
          livereload: true
        files: ["app/client/**/*"]
      coffee_server:
        options:
          nospawn: true
        files: ["coffee/server/**/*.coffee"]
        tasks: ["coffee:server", "server:reload"]
      coffee_client:
        files: ['coffee/client/**/*.coffee']
        tasks: ['coffee:client']
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
          base: ["app/client", "bower_components"]

  child_process = null
  server_reloading = false
  spawn_node_app = ->
    grunt.util.spawn
      cmd: 'node'
      args: ["--harmony_generators", "app/server/main.js"]
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
