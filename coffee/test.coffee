login = ->
  $.get '/game/auto_login', (rval) ->
    return unless rval
    $('#id_phone_number').val(rval.phone_number)
    $('#id_pin_code').val(rval.pin_code)
    $('#login-form').submit()

quick_match = ->
  btn = $('#quick_match')
  max_request = 5
  num_requested = 0

  toggle_btn_txt = (is_pending)->
    if is_pending
      btn.html('Searching...')
    else
      btn.html('Quick Match')

  find_opponent = (callback)->
    if num_requested >= max_request
      console.log "Max #{max_request} requests exceeded"
      toggle_btn_txt(false)
      return
    num_requested++
    $.get '/game/quick_match', (rval)->
      if rval.opponent
        callback()
      else
        setTimeout find_opponent, 3000

  btn.click ->
    toggle_btn_txt(true)
    find_opponent(begin_match)

  begin_match = ->
    console.log 'begin match'

$ ->
  if location.pathname == '/security/login'
    login()

  if location.pathname == '/game/dashboard/'
    quick_match()

