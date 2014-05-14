'use strict'

describe 'Controller: CrawladdressCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'LittleBeeGeoCrawlerApp'

  CrawladdressCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    CrawladdressCtrl := $controller 'CrawladdressCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
