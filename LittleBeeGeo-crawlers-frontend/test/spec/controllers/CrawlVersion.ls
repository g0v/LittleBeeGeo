'use strict'

describe 'Controller: CrawlversionCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'LittleBeeGeoCrawlerApp'

  CrawlversionCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    CrawlversionCtrl := $controller 'CrawlversionCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
