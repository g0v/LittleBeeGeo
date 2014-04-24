'use strict'

describe 'Controller: AdUploadCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'LittleBeeGeoFrontend'

  AdUploadCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    AdUploadCtrl := $controller 'AdUploadCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
