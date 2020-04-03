from lambdafunction.covidlambda import *
import pytest
from pytest_lambda import (
   disabled_fixture,
   error_fixture,
   lambda_fixture,
   not_implemented_fixture,
   static_fixture,
)
class TestServiceHandler:
    @pytest.fixture
    def event(self):
        return {
            "request": {
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.1234",
    "timestamp": "2016-10-27T21:06:28Z",
    "locale": "en-US",
    "intent": {
      "name": "InfoIntent",
      "slots": {
        "Country": {
          "name": "Country",
          "value": "all"
        },
        "Detail": {
          "name": "Detail",
          "value": "all"
        }
      }
    }
  }
        }

    @pytest.fixture
    def context(self):
        return 

    def test_lambda_handler(self, event, context):
        result = handler(event, context)
        #self.assertContains(result, testedagainst)
        assert result == {
            'response': {'card': {'title': 'Corona Informator'}}
        }