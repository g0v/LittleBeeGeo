'use strict'

describe 'Service: geoAccelGyro', () ->

  # load the service's module
  beforeEach module 'LittleBeeGeoFrontend'

  # instantiate service
  geoAccelGyro = {}
  beforeEach inject (_geoAccelGyro_) ->
    geoAccelGyro := _geoAccelGyro_

  it 'should do something', () ->
    expect(!!geoAccelGyro).toBe true
