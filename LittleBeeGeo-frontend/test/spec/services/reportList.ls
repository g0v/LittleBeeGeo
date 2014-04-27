'use strict'

describe 'Service: reportList', () ->

  # load the service's module
  beforeEach module 'LittleBeeGeoFrontend'

  # instantiate service
  reportList = {}
  beforeEach inject (_reportList_) ->
    reportList := _reportList_

  it 'should do something', () ->
    expect(!!reportList).toBe true
