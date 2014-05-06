'use strict'

describe 'Service: Geodata', () ->

  # load the service's module
  beforeEach module 'LittlebeegeofrontendApp'

  # instantiate service
  Geodata = {}
  beforeEach inject (_Geodata_) ->
    Geodata := _Geodata_

  it 'should do something', () ->
    expect(!!Geodata).toBe true
