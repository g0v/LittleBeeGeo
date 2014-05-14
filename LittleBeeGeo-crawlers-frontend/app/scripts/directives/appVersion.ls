'use strict'

angular.module 'LittleBeeGeoCrawlerApp'
  .directive 'appVersion', <[ version ]> ++ (version) -> do
    link: (scope, element, attrs) ->
      element.text 'the version is' + version
