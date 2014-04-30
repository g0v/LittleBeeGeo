'use strict'

cached_data = 
  data: [
    * name: \服貿x電信
    * name: \服貿x醫療
    * name: \服貿x房價
    * name: \服貿x農業
    * name: \服貿x食安
    * name: \政府x民間
    * name: \割闌尾
    * name: \監督條例相關
    * name: \公民憲政會議
    * name: \自由經濟示範區
    * name: \服貿
    * name: \其他
  ]
  data_timestamp: new Date!getTime!

angular.module 'LittleBeeGeoFrontend'
  .factory 'posterType', <[]> ++ -> do
    getData: ->
      cached_data.data

    getDataTimestamp: ->
      cached_data.data_timestamp
