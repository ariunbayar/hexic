login = ->
  $.get '/game/auto_login', (rval) ->
    return unless rval
    $('#id_phone_number').val(rval.phone_number)
    $('#id_pin_code').val(rval.pin_code)
    $('#login-form').submit()

$ ->
  if location.pathname == '/security/login'
    login()

  if location.pathname == '/game/dashboard/'
    setTimeout((-> $('#quick_match').click()), 500)
