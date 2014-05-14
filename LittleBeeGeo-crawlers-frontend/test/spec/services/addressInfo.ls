'use strict'

describe 'Service: Addressinfo', () ->

  # load the service's module
  beforeEach module 'LittlebeegeocrawlerApp'

  # instantiate service
  Addressinfo = {}
  beforeEach inject (_Addressinfo_) ->
    Addressinfo := _Addressinfo_

  it 'should do something', () ->
    expect(!!Addressinfo).toBe true
