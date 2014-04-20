'use strict'

{map, filter, head, sort-with} = require 'prelude-ls'

cache_list = 
  data: []

_SCALE_BY_ZOOM = [
  262144 # 0
  131072 # 1
  65536  # 2
  32768  # 3
  16384  # 4
  8192   # 5
  4096   # 6
  2048   # 7
  1024   # 8
  512    # 9
  256    # 10
  128    # 11
  64     # 12
  32     # 13
  16     # 14
  8      # 15
  4      # 16
  2      # 17
  1      # 18
]


angular.module 'LittleBeeGeoFrontend'
  .service 'reportList', <[ constants ]> ++ (constants) ->
    console.log 'constants:', constants
    diffByLatLon = (a, b) ->
      google.maps.geometry.spherical.computeDistanceBetween a.latLng, b.latLng

    _check_same_point = (params, the_list, zoom, is_remove_same_point) ->
      if the_list.data is void or not the_list.data.length then return params

      console.log 'the_list.data.length:', the_list.data.length

      sortWithDiffByLatLon = (x, y) ->
        (diffByLatLon x, params) - (diffByLatLon y, params)

      min_diff_by_latlon_data = the_list.data |> sort-with sortWithDiffByLatLon |> head

      min_diff_by_latlon = diffByLatLon min_diff_by_latlon_data, params

      threshold_dist_same_point = constants.THRESHOLD_DIST_SAME_POINT * _SCALE_BY_ZOOM[zoom]

      console.log 'min_diff_by_latlon_data:', min_diff_by_latlon_data, 'min_diff_by_latlon:', min_diff_by_latlon, 'threshold_dist_same_point:', threshold_dist_same_point

      if min_diff_by_latlon >  threshold_dist_same_point then return params

      if is_remove_same_point
        filterMinDiffByLatLonData = (x) ->
          (diffByLatLon x, params) > min_diff_by_latlon

        the_list.data = the_list.data |> filter filterMinDiffByLatLonData
        console.log 'after remove_data: the_list:', the_list

      result = if is_remove_same_point then void else min_diff_by_latlon_data

    # Public API here
    do 
      setMarker: (params, zoom, is_remove_same_point=true) ->
        #the_list: {data: []}
        the_marker = _check_same_point params, cache_list, zoom, is_remove_same_point

        if the_marker is not void
          cache_list.data ++= [the_marker]

        console.log 'after setMarker: params:', params, 'the_marker:', the_marker, 'cache_list.data:', cache_list.data

      getList: ->
        cache_list.data

      clearList: ->
        cache_list.data = []