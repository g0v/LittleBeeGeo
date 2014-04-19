'use strict'

{initial, last} = require 'prelude-ls'

cached_data = 
  data: {}

is_first = true

angular.module 'LittleBeeGeoFrontend'
  .factory 'jsonData', <[ $resource ]> ++ ($resource) -> do
    getData: ->
      if not is_first
        return cached_data.data

      is_first := false

      cached_data.data
