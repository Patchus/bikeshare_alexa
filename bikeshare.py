# This Bikeshare application uses the bikeshare XML feed to see if there are any bikes near you
# It then takes that information and feeds it into an Alexa APP.
 
from __future__ import print_function
import datetime as dt
from dateutil import tz
import urllib2
# This piece is tricky, you have to install this locally in the directory, otherwise it will not run
import xmltodict 

def bikestations():
    file = urllib2.urlopen('https://feeds.capitalbikeshare.com/stations/stations.xml')
    data = file.read()
    file.close()

    data = xmltodict.parse(data)
    return data

current_data = bikestations()

### This is where you would put you pickup stations or your drop off stations

pickup_stations = {'Station Name':Station Number} 
dropoff_stations = {'Station Name':Station Number} 

def lambda_handler(event, context):

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
 

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
 
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
 
 
def on_session_started(session_started_request, session):
    ## Called when the session starts 
 
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
 
 
def on_launch(launch_request, session):
    ## Called when the user launches the skill without specifying what they want
 
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()  
 
 
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
 
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
 
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
 
    # Dispatch to your skill's intent handlers
    if intent_name == "PickUp":
        return canipickup(intent, session)
    elif intent_name == "DropOff":
        return canidropoff(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")
 
 
def on_session_ended(session_ended_request, session):
    ##  Called when the user ends the session.
    ##  Is not called when the skill returns should_end_session=true
    
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    
 
# --------------- Functions that control the skill's behavior ------------------
 
 
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
 
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Bikeshare Application. " \
                    "Please ask me for the stations by saying, " \
                    "Can I pickup or Can I drop off"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me the time by saying, " \
                    "Ask Bikeshare if i can pick up a bike"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
 
 
def canipickup(intent, session):
    ### This is the meat of the code. It goes through the XML and sees if there are bikes in your
    ###  approved station list. If any of the stations have a bike it will tell you which ones
    ###  If no bikes are free, it will apologize and let you know
    
 
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    
    total_bikes = 0
    good_stations = []
    for station in xrange(0,len(current_data['stations']['station'])):    
        if int(current_data['stations']['station'][station]['terminalName']) in pickup_stations.values():
            station_data = current_data['stations']['station'][station]

            if current_data['stations']['station'][station]['nbBikes'] > 4:
                good_stations.append(str("{} bikes at {}".format(int(station_data['nbBikes']),station_data['name'])))
                total_bikes = int(current_data['stations']['station'][station]['nbBikes'])
                
            elif current_data['stations']['station'][station]['nbBikes'] > 0:
                good_stations.append(str("Yeah, but there are only {} bikes at {}".format(int(station_data['nbBikes']),station_data['name'])))
                total_bikes = int(current_data['stations']['station'][station]['nbBikes']) 
    speech_output = 'Yes there are '
    if total_bikes == 0:
        speech_output = 'Sorry there are no bikes'
    else:
        for station in good_stations:
            speech_output += ' {}'.format(station)
 
    speech_output = speech_output.replace('&','and')   
    reprompt_text = "Please ask me for the time by saying, " \
                        "Alexa what time is it"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def canidropoff(intent, session):
    ### This is the meat of the code. It goes through the XML and sees if there are docks in your
    ###  approved station list. If any of the stations have a bike it will tell you which ones
    ###  If no bikes are free, it will apologize and let you know
 
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    
    total_bikes = 0
    good_stations = []
    for station in xrange(0,len(current_data['stations']['station'])):    
        if int(current_data['stations']['station'][station]['terminalName']) in dropoff_stations.values():
            station_data = current_data['stations']['station'][station]
            
            if current_data['stations']['station'][station]['nbEmptyDocks'] > 4:
                good_stations.append(str("{} docks at {}".format(int(station_data['nbEmptyDocks']),station_data['name'])))
                total_bikes = int(current_data['stations']['station'][station]['nbEmptyDocks'])
                
            if current_data['stations']['station'][station]['nbEmptyDocks'] > 0:
                good_stations.append(str("{} docks at {}".format(int(station_data['nbEmptyDocks']),station_data['name'])))
                total_bikes = int(current_data['stations']['station'][station]['nbEmptyDocks'])

    speech_output = 'Yes there are '
    if total_bikes == 0:
        speech_output = 'Sorry there are no docks'
    else:
        for station in good_stations:
            speech_output += ' {}'.format(station)
 
    speech_output = speech_output.replace('&',' and ') 
    reprompt_text = "Please ask me for the time by saying, " \
                        "Alexa what time is it"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
 
 
# --------------- Helpers that build all of the responses ----------------------
 
 
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
 
 
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
