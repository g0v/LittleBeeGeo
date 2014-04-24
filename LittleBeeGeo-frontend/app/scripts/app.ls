# Declare app level module which depends on filters, and services
'use strict'

window.onGoogleReady = ->
  console.log 'onGoogleReady: start'
  angular.bootstrap window.document, <[ LittleBeeGeoFrontend ]>

angular.module 'LittleBeeGeoFrontend' <[ ngRoute ngCookies ngResource ui.map ui.event ui.bootstrap ui.select2 angularFileUpload ]>
  .config <[ $routeProvider $locationProvider ]> ++ ($routeProvider, $locationProvider, config) ->
    $routeProvider
      .when '/view1' templateUrl: '/views/partial1.html'
      .when '/view2' templateUrl: '/views/partial2.html'
      .when '/map' templateUrl: '/views/map.html'
      .when '/poster' templateUrl: '/views/poster.html'
    # Catch all
    .otherwise redirectTo: '/map'

    # Without serve side support html5 must be disabled.
    $locationProvider.html5Mode false
