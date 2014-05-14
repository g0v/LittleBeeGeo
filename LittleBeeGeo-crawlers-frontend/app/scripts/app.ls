# Declare app level module which depends on filters, and services
'use strict'

window.onGoogleReady = ->
  console.log 'onGoogleReady: start'
  angular.bootstrap window.document, <[ LittleBeeGeoCrawlerApp ]>

angular.module 'LittleBeeGeoCrawlerApp' <[ ngRoute ngCookies ngResource ui.map ui.event ]>
  .config <[ $routeProvider $locationProvider ]> ++ ($routeProvider, $locationProvider, config) ->
    $routeProvider
      .when '/view1' templateUrl: '/views/partial1.html'
      .when '/view2' templateUrl: '/views/partial2.html'
      .when '/google_address' templateUrl: '/views/google_address.html'
    # Catch all
    .otherwise redirectTo: '/view1'

    # Without serve side support html5 must be disabled.
    $locationProvider.html5Mode false
