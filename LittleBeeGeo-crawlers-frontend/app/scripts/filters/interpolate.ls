'use strict'

angular.module 'LittleBeeGeoCrawler'
  .filter 'interpolate', <[version]> ++ (version) ->
    (text) ->
      String(text)replace /\%VERSION\%/mg version
