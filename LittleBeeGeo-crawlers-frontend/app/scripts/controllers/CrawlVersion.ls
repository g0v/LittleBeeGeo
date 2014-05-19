'use strict'

{CONFIG} = window.LittleBeeGeoCrawler

{values} = require 'prelude-ls'

cached_result = []

angular.module 'LittleBeeGeoCrawlerApp'
  .controller 'CrawlVersionCtrl',  <[ $scope versionInfo adData ]> ++ ($scope, versionInfo, adData) ->

    $scope.Ads = [{"name": ""}]
    $scope.$watch (-> adData.getDataTimestamp!), ->
      ad_data = adData.getData!

      console.log 'CrawVersionCtrl: adData changed: ad_data:', ad_data

      $scope.Ads = [{"name": "", "the_type": ""}] ++ values ad_data

    $scope.$watch (-> versionInfo.getDataTimestamp!), ->
      the_data = versionInfo.getData!
      if not the_data.length
        return

      $scope.total_versions = the_data.length
      $scope.current_idx = 0
      cached_result := the_data

    $scope.$watch (-> $scope.current_idx), (new_val) ->
      if not $scope.total_versions
        return

      the_data = cached_result[new_val]
      $scope.current_data = the_data
      the_datetime = new Date the_data.deliver_time
      $scope.version_text = the_data.version_text + '(' + the_datetime.toLocaleString! + ')'
      if $scope.current_data.ad_versions is not void
        $scope.ad_versions = $scope.current_data.ad_versions
      else
        $scope.ad_versions = []

    $scope.ad_versions = []
    $scope.$watch (-> $scope.ad_versions.length), ->
      console.log '$scope.ad_versions:', $scope.ad_versions

    $scope.formatAd = (data) ->
      console.log 'formatAd: data:', data
      '<table><tr><td class="poster-img"><img class="flag" src="http://' + CONFIG.BEE_BACKEND_HOST + '/get/thumbnail/' + data.element[0].id + '"/></td><td>' + data.text + '</td><tr>'

    $scope.onPreRecord = ->
      $scope.current_data.ad_versions = $scope.ad_versions
      _pre_record!

    $scope.onGoodRecord = ->
      $scope.current_data.ad_versions = $scope.ad_versions
      versionInfo.updateVersion $scope.current_data
      _next_record!

    $scope.onNextRecord = ->
      $scope.current_data.ad_versions = $scope.ad_versions
      _next_record!

    _pre_record = ->
      console.log '_pre_record: start'
      if not $scope.total_versions
        return

      $scope.current_idx -= 1
      if $scope.current_idx < 0
        $scope.current_idx = $scope.total_versions - 1

    _next_record = ->
      console.log '_next_record: start'
      if not $scope.total_versions
        return

      $scope.current_idx += 1
      if $scope.current_idx >= $scope.total_versions
        $scope.current_idx = 0
