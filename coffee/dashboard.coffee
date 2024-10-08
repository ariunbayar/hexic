class Dashboard
  ajax: (url, data, successFunc = ->) ->
    $.ajax({
      url: url
      dataType: "json"
      data: data
      cache: false
      error: (xhr, msg) ->
      success: successFunc
    })

  quick_match: () ->
    btn = $('#quick_match')
    max_request = 5
    num_requested = 0

    find_opponent = (callback)=>
      btn.html('Searching...')
      if num_requested >= max_request
        console.log "Max #{max_request} requests exceeded"
        btn.html('Quick Match')
        return
      num_requested += 1
      @ajax @quick_match_url, {}, (rval)->
        if rval.opponent_id
          btn.html('Quick Match')
          callback(rval.redirect_url)
        else
          # retry mechanism
          setTimeout((-> find_opponent(callback)), 3000)

    begin_match = (redirect_url)->
      window.location = redirect_url

    find_opponent(begin_match)

@init_dashboard = (quick_match_url) ->
  dashboard = new Dashboard()
  dashboard.quick_match_url = quick_match_url
  $('#quick_match').click(-> dashboard.quick_match())
