'use strict'

{initial, last} = require 'prelude-ls'

{CONFIG} = window.LittleBeeGeoCrawler

console.log 'adData: CONFIG:', CONFIG

cached_data = 
  data: {}
  data_timestamp: new Date!getTime!

is_first = true

angular.module 'LittleBeeGeoCrawlerApp'
  .factory 'adData', <[ $resource $http constants ]> ++ ($resource, $http, constants) ->
    _get_data = ->
      console.log 'adData._get_data: start'
      if not is_first
        return cached_data.data

      is_first := false

      url = 'http://' + CONFIG.BEE_BACKEND_HOST + '/get/adData'
      num_query = constants.NUM_QUERY

      cached_data.data

      query_success = (the_data, getResponseHeaders) ->
        console.log 'adData._get_data.query_success: the_data:', the_data, 'length:', the_data.length, 'getResponseHeaders:', getResponseHeaders!

        new_data = if the_data.length == num_query then initial the_data else the_data

        new_data_dict = {[each_data.the_id, each_data] for each_data in new_data}

        cached_data.data <<< new_data_dict
        cached_data.data_timestamp = new Date!getTime!

        console.log 'adData._get_data.query_success: cached_data.data:', cached_data.data

        if the_data.length == num_query
          last_data = last the_data
          console.log 'last_data:', last_data
          next_id = last_data.json_id

          console.log 'next_id:', next_id, 'last_data:', last_data

          query_data next_id

      query_data = (next_id) ->
          NewQueryData = $resource url
          NewQueryData.query {num_query, next_id}, query_success

      console.log 'adData._get_data: url:', url, 'num_query:', num_query
      QueryData = $resource url
      QueryData.query {num_query}, query_success

      cached_data.data

    do
      getDataTimestamp: ->
        cached_data.data_timestamp

      reGetData: ->
        is_first := true
        _get_data!

      getData: ->
        _get_data!
