'use strict'

{map, fold, fold1, mean, join} = require 'prelude-ls'

LEGENDS = <[ ]>

# LEGEND_STRING = 

# LEGEND_COLOR =
  

angular.module 'LittleBeeGeoFrontend'
  .controller 'MapCtrl',  <[ $scope geoAccelGyro jsonData ]> ++ ($scope, geoAccelGyro, jsonData) ->
    geo = geoAccelGyro.getGeo!

    $scope.mapOptions = 
      center: new google.maps.LatLng geo.lat, geo.lon
      zoom: 14
      mapTypeId: google.maps.MapTypeId.ROADMAP

    is_first_map_center = true
    $scope.$on 'geoAccelGyro:event', (e, data) ->

      if data.event != 'devicegeo'
          return

      if not is_first_map_center
          return

      console.log 'to set is_first_map_center as false'
      is_first_map_center := false

      $scope.myMap.setCenter (new google.maps.LatLng data.lat, data.lon)

    $scope.$watch (-> Object.keys(jsonData.getData!).length), ->
      the_data = jsonData.getData!
