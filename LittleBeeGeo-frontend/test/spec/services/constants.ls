'use strict'

describe 'Service: Constants', () ->

  # load the service's module
  beforeEach module 'LittleBeeGeoFrontend'

  # instantiate service
  constants = {}
  beforeEach inject (_constants_) ->
    constants := _constants_

  it 'should do something', () ->
    expect(!!constants).toBe true
