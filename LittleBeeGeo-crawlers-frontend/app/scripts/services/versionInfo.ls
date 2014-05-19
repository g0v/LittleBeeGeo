'use strict'

{CONFIG} = window.LittleBeeGeoCrawler

cached_data = 
  data_timestamp: new Date!getTime!
  data: []

is_first = true

angular.module 'LittleBeeGeoCrawlerApp'
  .factory 'versionInfo', <[ $resource $http ]> ++ ($resource, $http) -> do
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

    upadteVersion: (data) ->
      csv_key = data.csv_key
      ad_versions = data.ad_versions

      console.log 'csv_key:', csv_key, 'ad_versions': ad_versions

      url = 'http://' + CONFIG.BACKEND_HOST + '/post/ad_version'

      _post_success = (the_data, status, headers, config) ->
        console.log 'the_data:', the_data, 'status:', status, 'headers:', headers, 'config:', config

      $http.post url, {csv_key, ad_versions}
        .success _post_success
