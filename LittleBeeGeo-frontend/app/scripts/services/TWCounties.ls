'use strict'

angular.module 'LittleBeeGeoFrontend'
  .factory 'TWCounties', <[]> ++ -> do
    getCounties: ->
      [
        * name: \台北市
        * name: \新北市
        * name: \台中市
        * name: \台南市
        * name: \高雄市
        * name: \桃園縣
        * name: \新竹市
        * name: \新竹縣
        * name: \苗栗縣
        * name: \彰化縣
        * name: \雲林縣
        * name: \嘉義市
        * name: \嘉義縣
        * name: \澎湖縣
        * name: \屏東縣
        * name: \宜蘭縣
        * name: \花蓮縣
        * name: \台東縣
        * name: \金門縣
        * name: \連江縣
      ]
