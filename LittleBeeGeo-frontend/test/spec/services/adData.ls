'use strict'

describe 'Service: Addata', () ->

  # load the service's module
  beforeEach module 'LittlebeegeofrontendApp'

  # instantiate service
  Addata = {}
  beforeEach inject (_Addata_) ->
    Addata := _Addata_

  it 'should do something', () ->
    expect(!!Addata).toBe true
