'use strict'

{last} = require 'prelude-ls'

CONFIG = window.LittleBeeGeo.CONFIG

angular.module 'LittleBeeGeoFrontend'
  .controller 'AdUploadCtrl',  <[ $scope $http $timeout $upload imgInfo posterType ]> ++ ($scope, $http, $timeout, $upload, imgInfo, posterType) ->
    $scope.data = {poster_name: ''}

    $scope.posterTypes = [{"name":""}] ++ posterType.getData!

    $scope.fileReaderSupported = window.FileReader !~= null

    $scope.hasUploader = (index) -> 
      $scope.upload[index] !~= null

    $scope.abort = (index) ->
      $scope.upload[index].abort!
      $scope.upload[index] = null

    $scope.onFileSelect = ($files) ->
      console.log 'onFileSelect: $files:', $files
      $scope.selectedFiles = []
      $scope.progress = []
      $scope.poster_names = []
      if $scope.upload and $scope.upload.length > 0
        for each_upload in $scope.upload
          if each_upload ~= null
            continue
          each_upload.abort!

      if not $files
        return

      $scope.upload = []
      $scope.uploadResult = []
      $scope.selectedFiles = $files
      $scope.poster_names = ["" for each_file in $scope.selectedFiles]
      $scope.dataUrls = []
      for idx, each_file of $files
        console.log 'onFileSelect: idx:', idx, 'each_file:', each_file
        _upload_file each_file, $scope, idx

    $scope.start = (index) ->
      $scope.progress[index] = 0

      _upload_with_file_reader = (index) ->
        file_reader = new FileReader!
        file_reader.onload = (e) ->
          console.log 'onload: e:', e
          http_params = 
            url: 'http://' + CONFIG.BACKEND_HOST + '/post/img/' + index
            method: $scope.httpMethod
            headers: {'Content-Type': $scope.selectedFiles[index].type}
            data: e.target.result
          $scope.upload[index] = ($upload.http http_params).then _upload_file_success, _upload_file_fail, _upload_file_progress

        file_reader

      _upload_file_success = (response) ->
        console.log '_upload_file_succes: response', response

        if not $scope.data.poster_type
          $scope.data.poster_type = (last posterType.getData!).name

        console.log '$scope.data.poster_type:', $scope.data.poster_type

        {filename, the_id, the_idx} = response.data

        data = {filename, the_id}

        if not $scope.data.poster_name
          poster_name = _parse_filename_prefix $scope.selectedFiles[the_idx].name
        else 
          poster_name = $scope.data.poster_name
          if $scope.selectedFiles.length > 1
            poster_name += ' - ' + (parseInt(the_idx) + 1)

        console.log 'the_idx:', the_idx, 'poster_name:', poster_name, 'poster_type:', $scope.data.poster_type, 'poster_type_value:', $scope.data.poster_type_value

        $scope.poster_names[the_idx] = poster_name

        data.the_type = $scope.data.poster_type
        data.name = poster_name

        console.log '_upload_file_success: to postData: data:', data

        imgInfo.postData data

      _upload_file_fail = (response) ->
        console.log '_upload_file_fail: response:', response
            
      _upload_file_progress = (event) ->
        console.log 'progress: event:', event
        $scope.progress[index] = Math.min 100, (parseInt 100.0 * event.loaded / event.total)

      file_reader = _upload_with_file_reader index

      file_reader.readAsArrayBuffer $scope.selectedFiles[index]


    _upload_file = (file, $scope, idx) ->
      console.log '_upload_file: file:', file, 'idx:', idx
      if window.FileReader and file.type.indexOf('image') > -1
        fileReader = new FileReader!
        fileReader.readAsDataURL file
        _set_preview fileReader, idx
      $scope.progress[idx] = -1
      $scope.start idx

    _set_preview = (fileReader, idx) ->
      fileReader.onload = (e) ->
        $timeout ->
          $scope.dataUrls[idx] = e.target.result

    _parse_filename_prefix = (filename) ->
      pattern = /\.[A-Za-z0-9]+$/
      filename.replace pattern, ''