class Dashboard
  constructor: (clicked_elem, url) ->
    @board_id = clicked_elem.attr('board_id')
    @url = url
    data = {'board_id': @board_id}
    @ajax(data, @successFunc)

  successFunc: (json)->
    return 

  ajax: (data, successFunc = ->) ->
    $.ajax({
      url: @url
      dataType: "json"
      data: data
      cache: false
      error: (xhr, msg) ->
      success: (json) ->
        successFunc(json)
    })

@init_dashboard = (clicked_elem, url) ->
  return new Dashboard(clicked_elem, url)
