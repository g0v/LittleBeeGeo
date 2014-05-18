'use strict'

describe 'Service: Versioninfo', () ->

  # load the service's module
  beforeEach module 'LittlebeegeocrawlerApp'

  # instantiate service
  Versioninfo = {}
  beforeEach inject (_Versioninfo_) ->
    Versioninfo := _Versioninfo_

  it 'should do something', () ->
    expect(!!Versioninfo).toBe true
