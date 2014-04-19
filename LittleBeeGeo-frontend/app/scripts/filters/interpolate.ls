'use strict'

angular.module 'LittleBeeGeoFrontend'
  .filter 'interpolate', <[version]> ++ (version) ->
    (text) ->
      String(text)replace /\%VERSION\%/mg version
