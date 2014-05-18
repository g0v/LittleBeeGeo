'use strict'

{CONFIG} = window.LittleBeeGeoCrawler

cached_data = 
  data_timestamp: new Date!getTime!
  data: []

is_first = true

angular.module 'LittleBeeGeoCrawlerApp'
  .factory 'versionInfo', <[ $resource ]> ++ ($resource ) -> do
    getData: ->
      if not is_first
        return cached_data.data

      is_first := false

      url = 'http://' + CONFIG.BACKEND_HOST + '/get/versions'

      _query_success = (data) ->
        console.log '_query_success: data:', data
        cached_data.data = data.result

        cached_data.data_timestamp = new Date!getTime!
        console.log 'cached_data:', cached_data

      QueryData = $resource url

      n = CONFIG.N_VERSIONS
      console.log 'to _query_success: n:', n
      QueryData.get {n}, _query_success

      cached_data.data

    getDataTimestamp: ->
      cached_data.data
