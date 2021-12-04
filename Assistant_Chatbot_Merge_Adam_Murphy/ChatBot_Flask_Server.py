#ChatBot_Flask_Server.py
#
#NAME
#
#        ChatBot_Flask_Server - file and controller for the Virtual Assistant 
#                               when it is being run on the flask user interface
#
#SYNOPSIS
#
#        ChatBot_Flask_Server.py
#
#            chatterbot              --> library that includes all chatbot functions for 
#                                        initialization, training, and interactivity 
#
#            Assistant_Chatbot_Merge --> file housing the majority of the functions utilized 
#                                        by the Virtual Assistant, as well as the individual 
#                                        chatbot instance. Can be used to run without 
#                                        the flask server.
#
#            flask                   --> web local host based user interface, utilizes html and style 
#                                        sheets to create a more visually pleasing display, sets up a 
#                                        local server on the current machine if desired 
#
#            webbrowser              --> allows python to open web pages in user's 
#                                        default browser option.
#
#            os                      --> standard python library for opening, reading, and 
#                                        writing files 
#
#            render_template         --> flask function to render a template based on a provided 
#                                        html file, said html file can then call a style sheet to 
#                                        further customize its' appearance
#
#            request                 --> allow the localhost instance/flask server to 
#                                        ask for and receive user input
#
#DESCRIPTION
#
#        This file houses all of the flask server specific functions, and also sets up and 
#        initializes the flask local host server that the Virtual Assistant will be deployed 
#        upon. It contains the typical main function to run from, and is the intended launch 
#        location of the Virtual Assistant program, though there are other methods available. 
#        This file also links all of the user interface files together in order to produce 
#        an aesthetically appealing Virtual Assistant.
#
#RETURNS
#
#        Opens a terminal instance launcher to ask for the user's startup preference 
#        between voice or text control, and then launches the flask user interface 
#        on the localhost server, in addition to opening the localhost server in 
#        the default webbrowser. The Virtual Assistant program can then be interacted 
#        with through the webbrowser, or the server can be shutdown 
#        at any time through the terminal via 'Ctrl + C'.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        6:19pm 7/16/2021                                                          #

from chatterbot import ChatBot
from Assistant_Chatbot_Merge import GoogleLaunch, GoogleQuery, DayOfTheWeek, WhatTime, FromWikipedia, NameResponse, NoteQuery, Help
from Assistant_Chatbot_Merge import OpenEmail, PlayAudioFile, ListenCheck, Speak, TextOrSpeech, dialogueBot, SetAlarm, LaunchProgram
from flask import Flask, render_template, request
import webbrowser
import os

#initializing the object for the server to run off of
chatbotApp = Flask(__name__)

#sets the folder for where to look for html templates
chatbotApp.static_folder = 'static'

#global variable necessary to set the control mode between text and speech
voice = 0

#ChatBot_Flask_Server::Home() ChatBot_Flask_Server::Home()
#
#NAME
#
#        ChatBot_Flask_Server::Home - starts the server and renders it via 
#                                     the linked html template
#
#SYNOPSIS
#
#        obj Chatbot_Flask_Server::Home()
#
#            render_template            --> flask function to render a page based on 
#                                           the provided html template, in this 
#                                           case 'Local_Host_ChatBot.html'
#
#DESCRIPTION
#
#        Simple built-in flask function to render and initialize our server based 
#        on the provided html template. The default location we are using to 
#        access this server is localhost within your webbrowser.
#
#RETURNS
#
#        Returns an object containing all of the parameters designated in the 
#        template html file, and is used to set up the server visually 
#        and functionally prior to launch.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        12:35pm 6/06/2021                                                          #

#routes set places for the html template to pull from when writing functions
@chatbotApp.route("/")
def Home():
    return render_template("Local_Host_ChatBot.html")

#ChatBot_Flask_Server::Home()

#ChatBot_Flask_Server::GetBotResponse() ChatBot_Flask_Server::GetBotResponse()
#
#NAME
#
#        ChatBot_Flask_Server::GetBotResponse - receives user input from either 
#                                               their microphone or the message 
#                                               bar in the user interface and 
#                                               determines which Virtual Assistant 
#                                               function to call, otherwise will 
#                                               default to a calculated ChatBot 
#                                               response based on the received input. 
#                                               Can also be used to shut the server 
#                                               down or change the control mode from 
#                                               between voice and text.
#
#SYNOPSIS
#
#        string Chatbot_Flask_Server::GetBotResponse()
#
#            voice            --> accessible global variable being used to determine 
#                                 the control type to use, this variable is global 
#                                 because python does not have the ability to create 
#                                 static variables, therefore I need to initialize 
#                                 this variable outside of the function 
#                                 I am calling it in.
#
#DESCRIPTION
#
#        Control function similar to Assist(a_Answer) from Assistant_Chatbot_Merge, 
#        but modified to work within the flask user interface and when receiving 
#        strings from the browser. Provides the ability to choose between the two 
#        separate control modes, text or voice. If a function is called from the 
#        Virtual Assistant it imports the reference from Assistant_Chatbot_Merge, 
#        otherwise it is utilizing the dialogueBot instance that has been imported 
#        to generate a response for the user.
#
#RETURNS
#
#        By default returns a string provided by the chatbot instance of the program, 
#        otherwise it provides strings given to it by the various 
#        Virtual Assistant functions it is calling.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        1:45pm 6/27/2021                                                          #

#Separate route tag for the html to use when writing a function to call GetBotResponse()
@chatbotApp.route("/get")
def GetBotResponse():

    global voice

    for i in range(1):
        if voice == 0:
            
            query = request.args.get('Message')

        elif voice == 1:

            query = str(ListenCheck()).lower()

        else:

            query = request.args.get('Message')

    if "open google" in query:

        return str(GoogleLaunch())

    elif "google" in query:
            
        return str(GoogleQuery(query))

    elif "what day is it" in query:

        return str(DayOfTheWeek())

    elif "what time is it" in query:

        return str(WhatTime())

    elif "from wikipedia" in query:

        return str(FromWikipedia(query))

    elif "who are you" in query:

        return str(NameResponse())

    elif "make a note" in query:

        return str(NoteQuery(query))

    elif "open email" in query:

        return str(OpenEmail())

    elif "set alarm for" in query:

        setTime1 = query.replace("set alarm for ", "")
        setTime2 = setTime1.replace(" hours", "")

        return str(SetAlarm(int(setTime2)))

    elif "launch program" in query:

        filePath = query.replace("launch program ", "")

        return str(LaunchProgram(filePath))

    elif "enable voice" in query:

        voice = 1
        Speak("Voice control enabled.")

        return str("Voice control enabled. Please input any text before speaking to enable microphone.")

    elif "disable voice" in query:

        voice = 0
        Speak("Voice control disabled.")

        return str("Voice control disabled.")

    elif "play" in query:

        return str(PlayAudioFile(query))

    elif "help" in query:

        return str(Help())

    elif "goodbye" in query:

        Speak("Goodbye.")

        os._exit(0)

    else:

        return str(dialogueBot.get_response(query))

#ChatBot_Flask_Server::GetBotResponse()

#ChatBot_Flask_Server::LaunchAssistantFlask(a_Voice) ChatBot_Flask_Server::LaunchAssistantFlask(a_Voice)
#
#NAME
#
#        ChatBot_Flask_Server::LaunchAssistantFlask - takes user input to decide which control 
#                                                     mode to boot the Virtual Assistant up in, 
#                                                     otherwise it launches the corresponding 
#                                                     webpage for the flask server, and runs 
#                                                     the server itself after deciding.
#
#SYNOPSIS
#
#        void Chatbot_Flask_Server::LaunchAssistantFlask(a_Voice)
#
#            a_Voice            --> integer variable that the function modifies 
#                                   to determine starting control type of 
#                                   the Virtual Assistant
#
#            answer             --> interger variable receiving user input from 
#                                   the terminal after calling the TextOrSpeech() 
#                                   function imported from Assistant_Chatbot_Merge
#
#DESCRIPTION
#
#        Standard launch function allowing the user to pick their preferred startup 
#        type via terminal input. Also launches the correct url for the localhost 
#        server so the user does not have to. This function also runs the actual 
#        user interface itself so it is necessary to begin interacting with 
#        the Virtual Assistant.
#
#RETURNS
#
#        No explicit returns are made, simply takes user input, 
#        modifies a variable, launches a webpage, 
#        and then launches the Virtual Assistant server to be interacted with.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        1:43am 9/22/2021                                                          #

def LaunchAssistantFlask(a_Voice):
    
    answer = TextOrSpeech()

    if answer == 1:

        a_Voice = 0
        webbrowser.open("http://127.0.0.1:5000/")
        chatbotApp.run()

    elif answer == 2:

        a_Voice = 1
        webbrowser.open("http://127.0.0.1:5000/")
        chatbotApp.run()

#ChatBot_Flask_Server::LaunchAssistantFlask(a_Voice)


#Simply runs the server and prompts the user for their preferred intial input type
if __name__ == "__main__":

    LaunchAssistantFlask(voice)

#Chatbot_Flask_Server.py
