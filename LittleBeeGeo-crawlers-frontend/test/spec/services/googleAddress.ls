'use strict'

describe 'Service: Googleaddress', () ->

  # load the service's module
  beforeEach module 'LittlebeegeocrawlerApp'

  # instantiate service
  Googleaddress = {}
  beforeEach inject (_Googleaddress_) ->
    Googleaddress := _Googleaddress_

  it 'should do something', () ->
    expect(!!Googleaddress).toBe true
