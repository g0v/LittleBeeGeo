'use strict'

{keys} = require 'prelude-ls'
angular.module 'LittleBeeGeoCrawlerApp'
  .factory 'googleAddress', <[ $http ]> ++ ($http)-> do
    getGeo: (data, $scope) ->
      if data.is_processed_geo
        return

      data.is_processed_geo = true
      data.google_address_map = {}
      google_address_list = data.google_address

      if not google_address_list or not google_address_list.length
        data.geo = {}
        return

      _get_success = (the_data, status, headers, config, statusText) ->
        console.log 'googleAddress: _get_success: the_data:', the_data, 'status:', status, 'headers:', headers!, 'config:', config, 'statusText:', statusText

        my_data = config.my_data
        my_scope = config.my_scope
        the_status = the_data.status
        if the_status != 'OK'
          console.log '[ERROR] googleAddress: unable to get google address: the_status:', the_status, 'the_data:', the_data
          my_data.is_process_geo_error = 'status: ' + the_status + 'query_data: ' + JSON.stringify the_data
          my_data.is_process_geo_done = true
          my_scope.error_msg = my_data.is_process_geo_error
          return 

        {county, town, latlon} = _parse_geo the_data

        if not my_data.county
          my_data <<< {county}

        if not my_data.town
          my_data <<< {town}

        address = config.params.address
        console.log 'googleAddress: before setup: my_data:', my_data, 'address:', address
        my_data.google_address_map[address] = latlon

        is_all_done = true
        google_address_map_keys = keys my_data.google_address_map
        for each_address in my_data.google_address
          if each_address not in google_address_map_keys
            is_all_done = false
            break

        if is_all_done
          my_data.is_process_geo_done = true
          if my_scope.current_data.csv_key == my_data.csv_key
            my_scope.is_process_geo_done = true

        console.log 'googleAddress: after setup: my_data:', my_data, 'scope:', my_scope

      _parse_geo = (the_data) ->
        the_first_data = the_data.results[0]
        console.log 'the_first_data:', the_first_data

        county = _parse_geo_county the_first_data.address_components
        town = _parse_geo_town the_first_data.address_components

        latlon = the_first_data.geometry.location

        {county, town, latlon}

      _parse_geo_county = (address_components) ->
        for each_component in address_components
          short_name = each_component.short_name
          the_types = each_component.types
          for each_type in the_types
            if each_type == 'administrative_area_level_2'
              return short_name

      _parse_geo_town = (address_components) ->
        for each_component in address_components
          short_name = each_component.short_name
          the_types = each_component.types
          for each_type in the_types
            if each_type == 'locality'
              return short_name

      url = 'https://maps.googleapis.com/maps/api/geocode/json'
      language = 'zh-tw'
      for address in google_address_list
        address = address
        $http.get url, {method: \GET, params: {address, language}, my_data: data, my_scope: $scope}
          .success _get_success
