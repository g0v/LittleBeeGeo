'use strict'

describe 'Service: Jsondata', () ->

  # load the service's module
  beforeEach module 'AngularBrunchSeedLivescriptBowerApp'

  # instantiate service
  Jsondata = {}
  beforeEach inject (_Jsondata_) ->
    Jsondata := _Jsondata_

  it 'should do something', () ->
    expect(!!Jsondata).toBe true
