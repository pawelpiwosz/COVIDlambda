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
      "name": "AMAZON.HelpIntent"
    }
  }
        }
    @pytest.fixture
    def context(self):
        return 

    def test_lambda_handler(self, event, context):
        result = handler(event, context)
        assert result == {
            'response': {'card': {'content': 'You can ask about any country, and specific '
                                   'data.When you do not specify country, you '
                                   'can retrieve: cases, deaths, recovered and '
                                   'active. When you specify country, the '
                                   'information available are: cases, today '
                                   'cases, active, critical, deaths, today '
                                   'deaths and recovered.',
                        'title': 'Corona Informator',
                        'type': 'Simple'},
               'outputSpeech': {'ssml': '<speak>You can ask about any country, '
                                        'and specific data.When you do not '
                                        'specify country, you can retrieve: '
                                        'cases, deaths, recovered and active. '
                                        'When you specify country, the '
                                        'information available are: cases, '
                                        'today cases, active, critical, deaths, '
                                        'today deaths and recovered.</speak>',
                                'type': 'SSML'},
               'reprompt': {'outputSpeech': {'ssml': '<speak>You can ask about '
                                                     'any country, and specific '
                                                     'data.When you do not '
                                                     'specify country, you can '
                                                     'retrieve: cases, deaths, '
                                                     'recovered and active. '
                                                     'When you specify country, '
                                                     'the information available '
                                                     'are: cases, today cases, '
                                                     'active, critical, deaths, '
                                                     'today deaths and '
                                                     'recovered.</speak>',
                                             'type': 'SSML'}},
               'shouldEndSession': False},
  'userAgent': 'ask-python/1.9.0 Python/3.8.2',
  'version': '1.0'
        }