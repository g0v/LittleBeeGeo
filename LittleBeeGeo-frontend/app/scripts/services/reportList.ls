'use strict'

{map, filter, head, sort-with} = require 'prelude-ls'

cache_list = 
  data: []


angular.module 'LittleBeeGeoFrontend'
  .service 'reportList', <[ constants ]> ++ (constants) ->
    console.log 'constants:', constants
    diffByPixel = (a, b) ->
      xa = a.pixel.x
      ya = a.pixel.y
      xb = b.pixel.x
      yb = b.pixel.y
      diff_x = xa - xb
      diff_y = ya - yb
      Math.sqrt (diff_x * diff_x + diff_y * diff_y)

    _remove_same_point = (params, the_list) ->
      sortWithDiffByPixel = (x, y) ->
        (diffByPixel x, params) - (diffByPixel y, params)

      if the_list.data is void or not the_list.data.length then return false

      console.log 'the_list.data.length:', the_list.data.length

      min_diff_by_px_data = the_list.data |> sort-with sortWithDiffByPixel |> head

      min_diff_by_px = diffByPixel min_diff_by_px_data, params

      console.log 'min_diff_by_px_data:', min_diff_by_px_data, 'min_diff_by_px:', min_diff_by_px, 'constants.THRESHOLD_DIST_SAME_POINT:', constants.THRESHOLD_DIST_SAME_POINT

      if min_diff_by_px > constants.THRESHOLD_DIST_SAME_POINT then return false

      filterMinDiffByPixelData = (x) ->
        (diffByPixel x, params) > min_diff_by_px

      the_list.data = the_list.data |> filter filterMinDiffByPixelData

      console.log 'after remove_data: the_list:', the_list

      true

    # Public API here
    do 
      setMarker: (params) ->
        #the_list: {data: []}
        if not _remove_same_point params, cache_list
          cache_list.data ++= [params]

        console.log 'after setMarker: params:', params, 'cache_list.data:', cache_list.data

      getList: ->
        cache_list.data

      clearList: ->
        cache_list.data = []