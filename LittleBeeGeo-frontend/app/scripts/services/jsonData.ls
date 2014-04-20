'use strict'

{initial, last} = require 'prelude-ls'

CONFIG = window.LittleBeeGeo.CONFIG

cached_data = 
  data: {}
  data_timestamp: new Date!getTime!

is_first = true

angular.module 'LittleBeeGeoFrontend'
  .factory 'jsonData', <[ $resource $http constants ]> ++ ($resource, $http, constants) -> 
    _get_data = ->
      if not is_first
        return cached_data.data

      is_first := false

      url = 'http://' + CONFIG.BACKEND_HOST + '/get/json'
      num_query = constants.NUM_QUERY

      cached_data.data

      query_success = (the_data, getResponseHeaders) ->
        console.log 'the_data:', the_data, 'getResponseHeaders:', getResponseHeaders!

        new_data = if the_data.length == num_query then initial the_data else the_data

        new_data_dict = {[each_data.the_id, each_data] for each_data in new_data}

        cached_data.data <<< new_data_dict
        cached_data.data_timestamp = new Date!getTime!

        if the_data.length == num_query
          last_data = last the_data
          console.log 'last_data:', last_data
          next_id = last_data.json_id

          console.log 'next_id:', next_id, 'last_data:', last_data

          query_data next_id

      query_data = (next_id) ->
          NewQueryData = $resource url
          NewQueryData.query {num_query, next_id}, query_success

      QueryData = $resource url
      QueryData.query {num_query}, query_success

      cached_data.data

    do
      getDataTimestamp: ->
        cached_data.data_timestamp

      reGetData: ->
        is_first := false
        _get_data!

      getData: ->
        _get_data!

      submitData: (data) ->
        console.log 'jsonData: submitData: data:', data

        url = 'http://' + CONFIG.BACKEND_HOST + '/post/json'

        post_success = (the_data, getResponseHeader) ->
          console.log 'the_data:', the_data

        ($http.post url, data, {method: \POST, data}).success post_success
