module.exports = (grunt) ->
  config = require './local_settings'
  grunt.initConfig
    config: config
    coffee:
      compile:
        expand: true,
        flatten: true,
        sourceMap: true
        src: "<%= config.coffee %>/*.coffee"
        dest: '<%= config.app %>/js/'
        ext: '.js'
    watch:
      livereload:
        options:
          livereload: true
        files: [
          "<%= config.app %>/*.html",
          "<%= config.app %>/js/*.js",
          "<%= config.app %>/js/lib/*.js",
        ]
      coffee:
        files: '<%= config.coffee %>/*.coffee'
        tasks: 'coffee:compile'
    connect:
      options:
        open: true
        port: 8000
      server:
        options:
          livereload: true
          base: "<%= config.app %>"

  child_process = null
  spawn_node_app = ->
    grunt.util.spawn
      cmd: 'node'
      args: ["#{config.app}/js/server.js", "debug"]
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

  grunt.event.on 'watch', (action, filepath, target) ->
    if child_process
      child_process.kill()
    console.log(">>> Restarting node application!!!")
    child_process = spawn_node_app()

  grunt.registerTask "server", ->
    child_process = spawn_node_app()
  grunt.registerTask "redis", ->
    spawn_redis()

  grunt.registerTask("default", ["redis", "connect", "server", "watch"])

  grunt.loadNpmTasks("grunt-contrib-watch")
  grunt.loadNpmTasks("grunt-contrib-coffee")
  grunt.loadNpmTasks("grunt-contrib-connect")
