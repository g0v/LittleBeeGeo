'use strict'

angular.module 'LittleBeeGeoCrawlerApp'
  .filter 'interpolate', <[version]> ++ (version) ->
    (text) ->
      String(text)replace /\%VERSION\%/mg version
