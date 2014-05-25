'use strict'

describe 'Controller: SheetCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'LittleBeeGeoFrontendApp'

  SheetCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    SheetCtrl := $controller 'SheetCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
