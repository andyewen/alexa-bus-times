from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import skill_logic


sb = SkillBuilder()


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to the Bus Times Checker. Built by Andrew Ewen"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Welcome.", speech_text)
        ).set_should_end_session(False)
        return handler_input.response_builder.response


class SayBusTimesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("say_bus_times")(handler_input)

    def handle(self, handler_input):
        departures = skill_logic.get_departures()

        buses_text = ', '.join(f"{d['routeName']} in {d['minutesToDeparture']} minutes" for d in departures)

        speech_text = 'Your bus times are: ' + buses_text

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Bus times!", speech_text)
        ).set_should_end_session(True)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SayBusTimesIntentHandler())

handler = sb.lambda_handler()
