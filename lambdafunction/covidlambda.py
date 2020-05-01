""" COVID Lambda function """

import logging
import json
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SIMPLE_CARD = "Corona Informator"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def person_or_people(amount):
    """ define the output word for amount of people """
    if int(amount) == 0:
        crowd = ""
    elif int(amount) == 1:
        crowd = "person"
    else:
        crowd = "people"
    return crowd

def get_data(country):
    """ Get data from api """
    urlbase = 'https://corona.lmao.ninja/'
    if country == "all":
        url = '{}v2/all'.format(
            urlbase
        )
    else:
        url = '{}v2/countries/{}'.format(
            urlbase,
            country
        )
    getdata = requests.get(url)
    return getdata.json()

def create_response_all(payload, range):
    """ Create response for Alexa with world data"""
    response_start = "Global information"
    if range == "all":
        response_line = "Cases {}, deaths {}, recovered {}, active {}, tests {}".format(
            payload['cases'],
            payload['deaths'],
            payload['recovered'],
            payload['active'],
            payload['tests']
        )
        message = "{}. {}".format(
            response_start,
            response_line
        )
    else:
        message = "{}. There is {} people {} at the moment.".format(
            response_start,
            payload[range],
            range)
    return message

def create_response_country(payload, range, country):
    """ Create response for Alexa with specific country """
    response_start = "Information for {}".format(
        payload['country']
    )
    if range == "all":
        response_line = ("All cases {}, "
                         "today {}, "
                         "active cases {}, "
                         "in critical state {}, "
                         "deaths today {}, "
                         "all deaths {}, "
                         "recovered {}. "
                         "Cases per million {}, "
                         "deaths per million {}. "
                         "Executed tests {}, "
                         "which means {} tests per milion.").format(
                             payload['cases'],
                             payload['todayCases'],
                             payload['active'],
                             payload['critical'],
                             payload['todayDeaths'],
                             payload['deaths'],
                             payload['recovered'],
                             payload['casesPerOneMillion'],
                             payload['deathsPerOneMillion'],
                             payload['tests'],
                             payload['testsPerOneMillion']
                             )
    else:
        states = {
            'todayCases': ['today cases', 'today infected'],
            'cases': ['cases', 'infected'],
            'active': ['active'],
            'critical': ['critical'],
            'deaths': ['fatalities', 'deaths', 'casualties'],
            'todayDeaths': ['today', 'current'],
            'recovered': ['recovered'],
            'tests': ['tests', 'tested', 'checked']
        }
        for states_key in states:
            aliases = states[states_key]
            if range in aliases:
                requested_state = states_key
        response_line = "There is {} {} in the category {} at the moment.".format(
            payload[requested_state],
            person_or_people(payload[requested_state]),
            range)

    message = "{}. {}".format(
        response_start,
        response_line
    )
    return message

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("You can ask about current situation with "
                       "Corona virus. You can ask about country and "
                       "specific data, like recoveries or active cases.")

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(SIMPLE_CARD, speech_text)).set_should_end_session(
                False)
        return handler_input.response_builder.response

class InfoIntentHandler(AbstractRequestHandler):
    """Handler for COVID info Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("InfoIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots

        countries = slots['Country']
        if not countries.value:
            country = "all"
        else:
            country = countries.value

        details = slots['Detail']
        if not details.value:
            range = "all"
        else:
            range = details.value

        response = get_data(country)
        if country == "all":
            speak = create_response_all(response, range)
        else:
            speak = create_response_country(response, range, country)

        speech_text = speak

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(SIMPLE_CARD, speech_text)).set_should_end_session(
                True)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("You can ask about any country, "
                       "and specific data."
                       "When you do not specify country, you can retrieve: "
                       "cases, deaths, recovered and active. "
                       "When you specify country, the information available are: "
                       "cases, today cases, active, critical, deaths, "
                       "today deaths and recovered.")

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                SIMPLE_CARD, speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(SIMPLE_CARD, speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "There is an error, and Corona Informator "
            "does not understand you")
        reprompt = "Ask again!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(InfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
