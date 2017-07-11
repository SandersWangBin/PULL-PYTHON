#!/usr/bin/env python

from TestCaseBase import TestCasePull

tcPullReg = TestCasePull("TestCasePullRegexp")
TC_01_NAME = "PULL REGEXP EXPRESSION TEST 01";
PULL_EXAMPLE_01 = """r'\{"message": "([a-zA-Z]+)\s[^{|^}]+'([a-zA-Z0-9_-]+)'"\}'.PULL({0}=='Created';{1}==['ExampleObj01','ExampleObj02'])"""
JSON_EXAMPLE_01_TRUE = """[{"message": "Created example object 'ExampleObj01'"}, {"message": "Created example object 'ExampleObj02'"}]"""
JSON_EXAMPLE_01_FALSE = """[{"message": "Failed to created 'ExampleObj01'"}, {"message": "Created example object 'ExampleObj02'"}]"""
tcPullReg.checkUsePull(TC_01_NAME, PULL_EXAMPLE_01, JSON_EXAMPLE_01_TRUE, True)
tcPullReg.checkUsePull(TC_01_NAME, PULL_EXAMPLE_01, JSON_EXAMPLE_01_FALSE, False)

TC_02_NAME = "PULL REGEXP EXPRESSION TEST 02";
PULL_EXAMPLE_02 = """r'\{"ID":\s*([0-9]+).*"NAME":\s*(.*)\s*\}'.PULL({0}==10;{1}<>"OBJ[0-9]+")"""
JSON_EXAMPLE_02_TRUE = """{"ID": 10, "NAME": "OBJ010"}"""
tcPullReg.checkUsePull(TC_02_NAME, PULL_EXAMPLE_02, JSON_EXAMPLE_02_TRUE, True)

TC_03_NAME = "PULL REGEXP EXPRESSION TEST 03";
PULL_EXAMPLE_03 = """r'\{"ID":\s*([0-9]+)\s*,\s*"NAME":\s*"([A-Z0-9]+)"\s*\}'.PULL({0}==[10,15];{1}==["OBJ010","OBJ015"])"""
JSON_EXAMPLE_03_TRUE = """[{"ID": 10, "NAME": "OBJ010"}, {"ID": 15, "NAME": "OBJ015"}]"""
JSON_EXAMPLE_03_FALSE = """[{"ID": 11, "NAME": "OBJ011"}, {"ID": 15, "NAME": "OBJ015"}]"""
tcPullReg.checkUsePull(TC_03_NAME, PULL_EXAMPLE_03, JSON_EXAMPLE_03_TRUE, True)
tcPullReg.checkUsePull(TC_03_NAME, PULL_EXAMPLE_03, JSON_EXAMPLE_03_FALSE, False)

TC_04_NAME = "PULL REGEXP EXPRESSION TEST 04";
PULL_EXAMPLE_04 = """r'\{"operation":\s*\{\s*"status": ([0-9]*),[a-zA-Z0-9:,\s"]*"endpoint": "([a-zA-Z]*)",[a-zA-Z0-9:,\s"]*"type": "([a-zA-Z]*)",[a-zA-Z0-9:,\s"]*"id": "([a-zA-Z0-9\._-]*)"\}'.PULL({0}==201;{2}=="create";{1}==["groups","metrics",                 "reports",   "groups","metrics",                   "reports"];{3}==["HTTP",  "HTTP.response.error.rate","web_report","HTTP2", "HTTP.response.error.rate.2","web_2_report"])"""
JSON_EXAMPLE_04_TRUE = """{"items": [{"operation": {"status": 201, "successful": true, "endpoint": "groups", "type": "create", "id": "HTTP"}}, {"operation": {"status": 201, "successful": true, "endpoint": "metrics", "type": "create", "id": "HTTP.response.error.rate"}}, {"operation": {"status": 201, "successful": true, "endpoint": "reports", "type": "create", "id": "web_report"}}, {"operation": {"status": 201, "successful": true, "endpoint": "groups", "type": "create", "id": "HTTP2"}}, {"operation": {"status": 201, "successful": true, "endpoint": "metrics", "type": "create", "id": "HTTP.response.error.rate.2"}}, {"operation": {"status": 201, "successful": true, "endpoint": "reports", "type": "create", "id": "web_2_report"}}], "errors": false}"""
JSON_EXAMPLE_04_FALSE = """{"items": [{"operation": {"status": 201, "successful": true, "endpoint": "groups", "type": "create", "id": "HTTP"}}, {"operation": {"status": 201, "successful": true, "endpoint": "metrics", "type": "create", "id": "HTTP.response.error.rate"}}, {"operation": {"status": 201, "successful": true, "endpoint": "reports", "type": "create", "id": "web_report"}}, {"operation": {"status": 201, "successful": true, "endpoint": "groups", "type": "create", "id": "HTTP2"}}, {"operation": {"status": 400, "successful": true, "endpoint": "metrics", "type": "create", "id": "HTTP.response.error.rate.2"}}, {"operation": {"status": 501, "successful": true, "endpoint": "reports", "type": "create", "id": "web_2_report"}}], "errors": true}"""
tcPullReg.checkUsePull(TC_04_NAME, PULL_EXAMPLE_04, JSON_EXAMPLE_04_TRUE, True)
tcPullReg.checkUsePull(TC_04_NAME, PULL_EXAMPLE_04, JSON_EXAMPLE_04_FALSE, False)

print tcPullReg


tcPullChain = TestCasePull("TestCasePullChain")
TC_01_NAME = "PULL CHAIN EXPRESSION TEST 01"
PULL_CHAIN_01 = "f'Rule_JsonCK_01.pull'.PULL(PULL_EXAMPLE_01)"
tcPullChain.checkUsePullChain(TC_01_NAME, PULL_CHAIN_01, JSON_EXAMPLE_01_TRUE, True)
tcPullChain.checkUsePullChain(TC_01_NAME, PULL_CHAIN_01, JSON_EXAMPLE_01_FALSE, False)

TC_02_NAME = "PULL CHAIN EXPRESSION TEST 02"
PULL_CHAIN_02 = "f'Rule_JsonCK_01.pull'.PULL(PULL_EXAMPLE_02)"
tcPullChain.checkUsePullChain(TC_02_NAME, PULL_CHAIN_02, JSON_EXAMPLE_02_TRUE, True)

TC_03_NAME = "PULL CHAIN EXPRESSION TEST 03"
PULL_CHAIN_03 = "f'Rule_JsonCK_01.pull'.PULL(PULL_EXAMPLE_02_01 + PULL_EXAMPLE_02_02)"
tcPullChain.checkUsePullChain(TC_03_NAME, PULL_CHAIN_03, JSON_EXAMPLE_03_TRUE, True)
tcPullChain.checkUsePullChain(TC_03_NAME, PULL_CHAIN_03, JSON_EXAMPLE_03_FALSE, False)

print tcPullChain