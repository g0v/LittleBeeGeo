'use strict'

empty-success = (items) ->
  console.log 'empty-success: items:', items


empty-dismissed = ->
  console.log 'empty-dismissed'


angular.module 'LittleBeeGeoFrontend'
  .controller 'AppCtrl', <[ $scope $location $resource $rootScope version $modal ]> ++ ($scope, $location, $resource, $rootScope, version, $modal) ->
    $scope <<< {version}

    $scope.$watch (-> $location.path!), (active-nav-id, orig-active-nav-id) ->
      console.log '$location.path():', $location.path!, 'active-nav-id:', active-nav-id, 'orig-active-nav-id', orig-active-nav-id
      $scope <<< {active-nav-id}

    $scope.getClass = (id) ->
      if $scope.active-nav-id is id then 'active' else ''

    $scope.pageTitle = '小蜜蜂回報'

    $scope.onHowtoReport = ->
      modalInstance = $modal.open do
        templateUrl: '/views/howto_report.html'

    $scope.onHowtoAddPoster = ->
      modalInstance = $modal.open do
        templateUrl: '/views/howto_add_poster.html'
