'use strict'

describe 'Service: Postertype', () ->

  # load the service's module
  beforeEach module 'LittlebeegeofrontendApp'

  # instantiate service
  Postertype = {}
  beforeEach inject (_Postertype_) ->
    Postertype := _Postertype_

  it 'should do something', () ->
    expect(!!Postertype).toBe true
