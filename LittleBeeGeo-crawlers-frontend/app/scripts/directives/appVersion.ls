'use strict'

angular.module 'LittleBeeGeoCrawler'
  .directive 'appVersion', <[ version ]> ++ (version) -> do
    link: (scope, element, attrs) ->
      element.text 'the version is' + version
