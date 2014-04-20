'use strict'

cached_data =
  data: {lat: 24.5, lon: 121.5}
  data_timestamp: new Date!getTime!

angular.module 'LittleBeeGeoFrontend'
  .factory 'geoAccelGyro', <[ $rootScope $window ]> ++ ($rootScope, $window) ->
    console.log 'to set send-event'

    $window.ondeviceorientation = (event) ->
      yaw = event.alpha
      pitch = event.beta
      roll = event.gamma

      $rootScope.$apply -> do
        $rootScope.$broadcast 'geoAccelGyro:event', {'event': 'deviceorientation', yaw, pitch, roll}

    $window.ondevicemotion = (event) ->
      move_x = event.acceleration.x
      move_y = event.acceleration.y
      move_z = event.acceleration.z

      $rootScope.$apply -> do
        $rootScope.$broadcast 'geoAccelGyro:event', {'event': 'devicemotion', move_x, move_y, move_z}

    getGeoCallback = (position) ->
      lat = position.coords.latitude
      lon = position.coords.longitude

      cached_data.data <<< {lat, lon}
      cached_data.data_timestamp = new Date!getTime!

      console.log 'got currentPosition: position:', position

      $rootScope.$apply -> 
        $rootScope.$broadcast 'geoAccelGyro:event', {'event': 'devicegeo', lat, lon}

    navigator.geolocation.watchPosition getGeoCallback

    do 
      getGeo: -> 
        cached_data.data

      getDataTimestamp: ->
        cached_data.data_timestamp