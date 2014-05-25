'use strict'

{map, values, join} = require 'prelude-ls'

angular.module 'LittleBeeGeoFrontend'
  .controller 'SheetCtrl',  <[ $scope jsonData ]> ++ ($scope, jsonData) ->
    $scope.$watch (-> jsonData.getDataTimestamp!), ->
      the_data = jsonData.getData!

      console.log 'the_data:', the_data

      $scope.the_data = values the_data |> map _parse_data

      console.log '$scope.the_data:', $scope.the_data

    _parse_data = (the_data) ->
      the_datetime = new Date the_data['deliver_time'] * 1000
      the_data['deliver_datetime'] = the_datetime.toLocaleString!
      if the_data.ad_versions is void
        the_data.ad_versions = []
      the_data['ad_version_text'] = join ',', the_data.ad_versions

      the_data

    gridOptions = 
      data: 'the_data'
      enablePaging: true
      #pageSizes: [10, 100, 1000]
      #pageSize: 100
      enablePinning: true
      showFilter: true
      enableColumnResize: true
      enableHighlighting: true
      #plugins: [new window.ngGridCsvExportPlugin!]
      sortInfo: 
        fields: <[ time ]>
        directions: <[ asc ]>
      columnDefs: 
        * field: \deliver_datetime
          displayName: \發送時間
        * field: \user_name
          displayName: \暱稱
        * field: \county
          displayName: \縣市
        * field: \town
          displayName: \鄉鎮市區
        * field: \address
          displayName: '路名 (區域)'
        * field: \ad_version_text
          displayName: \檔案版本
        * field: \count
          displayName: \數量
        * field: \deliver_status
          displayName: \發送狀況
        * field: \memo
          displayName: \memo

    $scope <<< {gridOptions}
