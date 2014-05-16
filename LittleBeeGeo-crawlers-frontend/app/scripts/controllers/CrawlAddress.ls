'use strict'

{CONFIG} = window.LittleBeeGeoCrawler

{fold1, map, mean} = require 'prelude-ls'

INIT_LAT = 24.0
INIT_LON = 121.5

cached_result = []

COLOR_REPORT = \#0F8
ICON_REPORT = \report.png
COLOR_REPORT_PATH = \#0FF
COLOR_CURRENT_POSITION = \#000
ICON_CURRENT_POSITION = \img/bee3.png
ICON_BEEZ_POSITION = \img/littlebeeflower3.png


angular.module 'LittleBeeGeoCrawlerApp'
  .controller 'CrawlAddressCtrl',  <[ $scope addressInfo googleAddress ]> ++ ($scope, addressInfo, googleAddress) ->

    $scope.mapOptions = 
      center: new google.maps.LatLng INIT_LAT, INIT_LON
      zoom: 7
      draggableCursor: 'pointer' 
      draggingCursor: 'pointer' 
      mapTypeId: google.maps.MapTypeId.ROADMAP
      disableDefaultUI: true
    $scope.zoom = 7

    $scope.$watch (-> addressInfo.getDataTimestamp!), ->
      the_data = addressInfo.getData!
      if not the_data.length
        return
      $scope.total_address = the_data.length
      $scope.current_idx = 0
      cached_result := the_data

      console.log 'CrawlAddress: addressInfo changed: the_data:', the_data

    $scope.$watch (-> $scope.current_idx), (new_val) ->
      if not $scope.total_address
        return

      the_data = cached_result[new_val]
      $scope.current_data = the_data
      console.log 'new current_idx:', new_val, 'the_data:', the_data
      $scope.address_text = the_data.county_and_town + ' ' + the_data.address
      $scope.error_msg = ''
      $scope.is_process_geo_done = false
      googleAddress.getGeo the_data, $scope

    $scope.$watch (-> $scope.is_process_geo_done), (new_val, orig_val) ->
      console.log 'CrawlAddress: scope.is_process_geo_done new_val:', new_val, 'orig_val:', orig_val
      if new_val
        _update_map $scope.current_data
      else
        if $scope.current_data and $scope.current_data.is_process_geo_done
          $scope.is_process_geo_done = true
          if $scope.current_data.is_process_geo_error
            $scope.error_msg = $scope.current_data.is_process_geo_error
          _update_map $scope.current_data

    _update_map = (data) ->
      console.log 'CrawlAddress: _update_map: data:', data

      _remove_marker_from_googlemap $scope.report_marker

      data.geo = _parse_data_geojson data

      if not data.geo
        return 

      $scope.report_marker = _add_marker_to_googlemap data.geo, COLOR_REPORT

      center_marker = _calc_center_marker data.geo

      console.log 'CrawlAddress: center_marker:', center_marker

      $scope.myMap.setCenter (new google.maps.LatLng center_marker[1], center_marker[0])

      $scope.myMap.setZoom(16)

    _parse_data_geojson = (data) ->
      google_address = data.google_address
      if not google_address
        return {}
        
      google_address_map = data.google_address_map

      if google_address.length == 1
        return {"type": "Point", "coordinates": _coordinate google_address_map[google_address]}
      else
        coordinates = [_coordinate google_address_map[address] for address in google_address]

        coordinates = _remove_redundant_coordinates coordinates

        if coordinates.length == 1
          return {"type": "Point", "coordinates": coordinates[0]}

        return {"type": "LineString", "coordinates": coordinates}

    _coordinate = (latlon) ->
      return [latlon.lng, latlon.lat]

    _remove_redundant_coordinates = (coordinates) ->
      pre_lat = ''
      pre_lon = ''

      results = []
      for each_coordinate in coordinates
        each_lon = each_coordinate[0].toFixed 5
        each_lat = each_coordinate[1].toFixed 5

        if each_lon == pre_lon and each_lat == pre_lat
          continue

        results ++= [each_coordinate]

        pre_lon = each_lon
        pre_lat = each_lat

      return results

    _remove_marker_from_googlemap = (marker) ->
      if not marker
        return

      marker.setMap void

    _add_marker_to_googlemap = (geo, color) ->
      the_type = geo.type
      the_coordinates = geo.coordinates

      switch the_type
      | 'Polygon'    => _parse_polygon the_coordinates, color
      | 'LineString' => _parse_line_string the_coordinates, color
      | 'Point'      => _parse_point the_coordinates, color

    _calc_center_marker = (geo) ->
      the_type = geo.type
      the_coordinates = geo.coordinates
      switch the_type
      | 'Point'      => the_coordinates
      | 'LineString' => _calc_center_marker_line_string the_coordinates

    _calc_center_marker_line_string = (coordinates) ->
      len = coordinates.length
      if not len
        return [INIT_LON, INIT_LAT]

      result = coordinates |> fold1 (a, b) -> [a[0] + b[0], a[1] + b[1]]
        |> map -> it / len

    _parse_polygon = (coordinates, color, value) ->
      polygon_opts = 
        map: $scope.myMap,
        paths: [_parse_path coord for coord in coordinates]
        fillColor: color
        strokeColor: color

      polygon = new google.maps.Polygon polygon_opts
      polygon._value = value
      polygon

    _parse_line_string = (coordinates, color, value) ->
      polyline_opts = 
        map: $scope.myMap
        path: _parse_path coordinates
        fillColor: color
        strokeColor: color

      polyline = new google.maps.Polyline polyline_opts
      polyline._value = value
      console.log '_parse_line_string: polyline_opts:', polyline_opts, 'polyline:', polyline
      polyline

    _parse_point = (coordinates, color, value) ->
      console.log '_parse_point: coordinates:', coordinates, 'color:', color, 'value:', value

      beez =
        url: ICON_BEEZ_POSITION
        size: new google.maps.Size 50, 70
        scaledSize: new google.maps.Size 25, 35
        origin: new google.maps.Point 0, 0
        anchor: new google.maps.Point 12, 12

      marker_opts = 
        map: $scope.myMap
        position: new google.maps.LatLng coordinates[1], coordinates[0]
        fillColor: color
        strokeColor: color
        icon: beez

      marker = new google.maps.Marker marker_opts
      marker._value = value
      marker

    _parse_path = (coordinates) ->
      console.log '_parse_path: coordinates', coordinates
      [new google.maps.LatLng coord[1], coord[0] for coord in coordinates]


    $scope.$watch (-> $scope.myMap), (new_val, orig_val) ->

    $scope.onMapIdle = -> 

    $scope.onPreRecord = ->
      if not $scope.total_address
        return

      $scope.current_idx -= 1
      if $scope.current_idx < 0
        $scope.current_idx = $scope.total_address - 1

    $scope.onNextRecord = ->
      if not $scope.total_address
        return

      $scope.current_idx += 1
      if $scope.current_idx >= $scope.total_address
        $scope.current_idx = 0

    $scope <<< {current_idx: -1, total_address: 0, current_data: {}}