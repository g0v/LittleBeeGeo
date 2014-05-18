'use strict'

describe 'Service: Constants', () ->

  # load the service's module
  beforeEach module 'LittlebeegeocrawlerApp'

  # instantiate service
  Constants = {}
  beforeEach inject (_Constants_) ->
    Constants := _Constants_

  it 'should do something', () ->
    expect(!!Constants).toBe true
