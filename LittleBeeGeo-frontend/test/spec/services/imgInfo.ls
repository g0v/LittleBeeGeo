'use strict'

describe 'Service: imgInfo', () ->

  # load the service's module
  beforeEach module 'LittleBeeGeoFontend'

  # instantiate service
  imgInfo = {}
  beforeEach inject (_imgInfo_) ->
    imgInfo := _imgInfo_

  it 'should do something', () ->
    expect(!!imgInfo).toBe true
