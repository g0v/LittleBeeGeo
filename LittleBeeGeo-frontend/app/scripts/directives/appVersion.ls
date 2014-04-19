'use strict'

angular.module 'LittleBeeGeoFrontend'
  .directive 'appVersion', <[ version ]> ++ (version) -> do
    link: (scope, element, attrs) ->
      element.text 'the version is' + version
