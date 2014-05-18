# Declare app level module which depends on filters, and services
'use strict'

window.onGoogleReady = ->
  console.log 'onGoogleReady: start'
  angular.bootstrap window.document, <[ LittleBeeGeoCrawlerApp ]>

angular.module 'LittleBeeGeoCrawlerApp' <[ ngRoute ngCookies ngResource ui.map ui.event ui.select2 ]>
  .config <[ $routeProvider $locationProvider ]> ++ ($routeProvider, $locationProvider, config) ->
    $routeProvider
      .when '/google_address' templateUrl: '/views/google_address.html'
      .when '/versions' templateUrl: '/views/versions.html'
    # Catch all
    .otherwise redirectTo: '/google_address'

    # Without serve side support html5 must be disabled.
    $locationProvider.html5Mode false
