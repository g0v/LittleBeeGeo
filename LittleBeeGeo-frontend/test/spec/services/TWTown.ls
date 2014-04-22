'use strict'

describe 'Service: Twtown', () ->

  # load the service's module
  beforeEach module 'LittlebeegeofrontendApp'

  # instantiate service
  Twtown = {}
  beforeEach inject (_Twtown_) ->
    Twtown := _Twtown_

  it 'should do something', () ->
    expect(!!Twtown).toBe true
