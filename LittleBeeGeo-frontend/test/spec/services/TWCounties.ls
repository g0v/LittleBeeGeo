'use strict'

describe 'Service: TWCounties', () ->

  # load the service's module
  beforeEach module 'LittlebeegeofrontendApp'

  # instantiate service
  TWCounties = {}
  beforeEach inject (_TWCounties_) ->
    TWCounties := _TWCounties_

  it 'should do something', () ->
    expect(!!TWCounties).toBe true
