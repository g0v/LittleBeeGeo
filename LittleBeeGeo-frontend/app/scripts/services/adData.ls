'use strict'

cached_data = 
  data: [
    * name: \Bee140405
    * name: \Bee140405-黑白
    * name: \服貿x醫療
    * name: \馬政府正在騙我們的事
    * name: \政院版/民間版差異比較表
    * name: \服貿對看病有什麼影響
    * name: \服貿你服不服
  ]
  data_timestamp: new Date!getTime!

angular.module 'LittleBeeGeoFrontend'
  .factory 'adData', <[]> ++ -> do
    getData: ->
      cached_data.data

    getDataTimestamp: ->
      cached_data.data_timestamp