'use strict'

{CONFIG} = window.LittleBeeGeoCrawler

{map} = require 'prelude-ls'

cached_data = 
  data_timestamp: new Date!getTime!
  data: []

is_first = true

angular.module 'LittleBeeGeoCrawlerApp'
  .factory 'addressInfo', <[ $resource ]> ++ ($resource) -> do
    getData: ->
      if not is_first
        return cached_data.data

      is_first := false

      url = 'http://' + CONFIG.BACKEND_HOST + '/get/google_address'

      _query_success = (data) ->
        console.log '_query_success: data:', data
        cached_data.data = data.result |> map _update_with_taiwan

        cached_data.data_timestamp = new Date!getTime!
        console.log 'cached_data:', cached_data

      _update_with_taiwan = ->
        it.county_and_town = '台灣' + it.county_and_town
        it.google_address = ['台灣' + each_address for each_address in it.google_address]
        it

      QueryData = $resource url

      n = CONFIG.N_ADDRESS
      console.log 'to _query_success: n:', n
      QueryData.get {n}, _query_success

      cached_data.data

    getDataTimestamp: ->
      cached_data.data