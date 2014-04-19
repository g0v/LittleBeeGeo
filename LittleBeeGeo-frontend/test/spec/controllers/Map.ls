'use strict'

describe 'Controller: MapCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'LittleBeeGeoFrontend'

  MapCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    MapCtrl := $controller 'MapCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
