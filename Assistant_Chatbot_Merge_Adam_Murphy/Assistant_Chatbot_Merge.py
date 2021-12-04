#Assistant_Chatbot_Merge.py
#
#NAME
#
#        Assistant_Chatbot_Merge - Creates chatbot instance and houses all related functions for the 
#                                  virtual assistant and chatbot being merged together.
#
#SYNOPSIS
#
#        Assistant_Chatbot_Merge.py
#
#            webbrowser            --> allows python to open web pages in user's 
#                                      default browser option.
#
#            speech_recognition    --> simple speech to text library to allow 
#                                      voice control of the chatbot and virtual 
#                                      assistant
#
#            pyttsx3               --> takes the input from chatbot or virtual assistant 
#                                      and synthesizes its' "voice" for the user to hear
#
#            datetime              --> standard python library for receiving the time 
#                                      of day as well as the date
#
#            wikipedia             --> allows python to parse wikipedia for search results 
#                                      and return either a webpage or a string of the page 
#                                      contents
#
#            os                    --> standard python library for opening, reading, and 
#                                      writing files 
#                                      
#            chatterbot            --> library that includes all chatbot functions for 
#                                      initialization, training, and interactivity 
#                                      
#            ChatBot               --> chatterbot subset that allows construction of a 
#                                      chatbot object, including setting all parameters 
#                                      for its response type 
#                                      
#            ListTrainer           --> chatterbot subset that trains the chatbot instance 
#                                      utilizing a provided text or yml file with dialogue 
#                                      options provided in a list format 
#                                      
#            ChatterbotCorpusTrainer --> chatterbot subset that trains the chatbot using 
#                                        accessible data corpus from the web or provided 
#                                        by the user, more robust than ListTrainer but takes longer 
#                                        
#            UbuntuCorpusTrainer   --> chatterbot subset that trains using an available online 
#                                      Ubuntu Dialogue Corpus, which is a massive dataset. If the 
#                                      corpus has already been downloaded it skips that step 
#                                      
#            LevenshteinDistance   --> chatterbot dialogue library and setting that determines the 
#                                      algorithm the chatbot uses to decide response similarity, in 
#                                      this instance the algorithm is Levenshtein Distance 
#                                      (the mathematical formula) 
#                                      
#            flask                 --> web local host based user interface, utilizes html and style 
#                                      sheets to create a more visually pleasing display, sets up a 
#                                      local server on the current machine if desired 
#                                      
#            request               --> flask function that enables a hosted web server to send 
#                                      information back to the machine it is being run on 
#                                      
#            time                  --> python standard library for setting alarms and scheduling 
#                                      operations 
#                                      
#            subprocess            --> python API for spawning processes, threads, and running 
#                                      separate programs from within the current one
#
#DESCRIPTION
#
#        This file serves to house the majority of the functions 
#        executed by the Virtual Assitant 
#        portion of the project, and ties them all to 
#        the ChatBot instance so that they can later 
#        be employed to the flask localhost server. 
#        It has its' own main function in order to allow 
#        the user to run the Virtual Assistant and ChatBot 
#        merge together without the flask user 
#        interface if they desire to have it running in the background. 
#
#        This file also contains the means for the terminal or the flask user interface to parse 
#        audio from the user's microphone into usable text.
#
#RETURNS
#
#        Opens a terminal instance running both the ChatBot 
#        and Virtual Assistant at the same time, 
#        and allows for two separate modes: text-based, 
#        or speech-based for control. The Terminal 
#        will print out the basic responses instead of the 
#        flask user interface if run here.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        8:19pm 8/12/2021                                                          #

import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from os.path import join
from flask import Flask, request
import time
import subprocess


#Assistant_Chatbot_Merge::ListenCheck() Assistant_Chatbot_Merge::ListenCheck()
#
#NAME
#
#        Assistant_Chatbot_Merge::ListenCheck - recognizes microphone audio from user, determines 
#                                               the correct language, and converts it into a string 
#                                               for use by the Virtual Assistant and ChatBot.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::ListenCheck()
#
#            recognized       --> storage variable for audio from microphone
#
#            source           --> audio input, a microphone in this case
#
#            audio            --> storage variable for cleaned and parsed 
#                                 audio after passing source to recognized
#
#            query            --> audio converted to appropriate language 
#                                 (english in this case) and cleaned up as 
#                                 a string for use by ChatBot and Virtual Assistant
#
#DESCRIPTION
#
#        This function will attempt to listen for user audio input when using the 
#        voice control mode of the Virtual Assistant, when it detects audio input 
#        from the user's microphone it will attempt to understand the language and 
#        parse it into a readable and usable string variable for the 
#        Virtual Assistant or ChatBot to respond to.
#
#RETURNS
#
#        Returns a "query" variable that houses the parsed string of text for 
#        the Virtual Assistant or ChatBot to determine a response to.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        7:23pm 3/25/2021                                                          #

def ListenCheck():

    recognized = sr.Recognizer()

    with sr.Microphone() as source:

        print('Listening')

        recognized.pause_threshold = 1.0
        audio = recognized.listen(source)

        try:

            print("Recognizing")

            query = recognized.recognize_google(audio, language = 'en-in')
            print("Recognized command = ", query)

        except Exception as e:

            print(type(e), e)
            print("Error recognizing, please repeat command or statement.")
            return "None"

        return query

#Assistant_Chatbot_Merge::ListenCheck()

#Assistant_Chatbot_Merge::Speak(a_Audio) Assistant_Chatbot_Merge::Speak(a_Audio)
#
#NAME
#
#        Assistant_Chatbot_Merge::Speak - takes a returned string from the ChatBot 
#                                         or Virtual Assistant and synthesizes it to 
#                                         speech for audio play. Active whether the 
#                                         ChatBot is in voice control mode or not.
#
#SYNOPSIS
#
#        void Assistant_Chatbot_Merge::Speak(string a_Audio)
#
#            a_Audio          --> text string returned by the ChatBot or 
#                                 Virtual Assistant to be converted into playable audio
#
#            speechResource   --> audio synthesizer intilialization, has subsections of 
#                                 "voices", and "voice" to determine what the audio playback 
#                                 sounds like
#
#            voices           --> voice synthesizer options for audio playback, different 
#                                 array elements correspond to different narrators
#
#DESCRIPTION
#
#        This function will attempt to receive a string from the ChatBot or 
#        Virtual Assistant instance and convert it into a playable audio instance. 
#        Effectively synthesizing text to speech so that the Bot can be replied to 
#        without directly looking at the UI for the written statement.
#
#RETURNS
#
#        Does not return a specific variable for output or storage, instead plays 
#        an audio wavform that it temporarily creates based on the string provided 
#        by a_Audio when the function is called.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        9:45pm 3/26/2021                                                          #

def Speak(a_Audio):

    speechResource = pyttsx3.init()
    voices = speechResource.getProperty('voices')
    speechResource.setProperty('voice', voices[1].id)

    speechResource.say(a_Audio)
    speechResource.runAndWait()

#Assistant_Chatbot_Merge::Speak(a_Audio)

#Assistant_Chatbot_Merge::TextOrSpeech() Assistant_Chatbot_Merge::TextOrSpeech()
#
#NAME
#
#        Assistant_Chatbot_Merge::TextOrSpeech - receives user input for a numerical 
#                                                value of '1' or '2' to determine the 
#                                                starting mode of the Virtual Assistant 
#                                                (text or voice). Loops until the correct 
#                                                input is provided. The returned integer 
#                                                is utilized by: 
#                                                Assistant_Chatbot_Merge::Assist(a_Answer) 
#                                                and Assistant_Chatbot_Merge::LaunchAssistant()
#
#SYNOPSIS
#
#        int Assistant_Chatbot_Merge::TextOrSpeech()
#
#            answer           --> storage variable for user input of an 
#                                 integer between '1' and '2'
#
#DESCRIPTION
#
#        This function will prompt the user for terminal input to decide whether 
#        the Virtual Assistant boots up in voice control or text control mode. 
#        The chosen state can be altered at any time while the program is running. 
#        It simply asks a question and returns an associated integer value of 
#        '1' or '2' for Assist(a_Answer) to utilize.
#
#RETURNS
#
#        Returns an integer value of '1' or '2' to be utilized by 
#        Assistant_Chatbot_Merge::LaunchAssistant()
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        3:05pm 4/17/2021                                                          #

def TextOrSpeech():

    answer = input("Please input 1 for Text, or 2 for Speech: ")

    if answer == "1":

        return 1

    elif answer == "2":

        return 2

    else:

        print("Invalid Response...")
        TextOrSpeech()

#Assistant_Chatbot_Merge::TextOrSpeech()

#Assistant_Chatbot_Merge::LaunchAssistant() Assistant_Chatbot_Merge::LaunchAssistant()
#
#NAME
#
#        Assistant_Chatbot_Merge::LaunchAssistant - calls Assistant_Chatbot_Merge::TextOrSpeech() 
#                                                   to obtain a prompted value of '1' or '2' from 
#                                                   the user in order to decide which variant of 
#                                                   Assistant_Chatbot_Merge::Assist(a_Answer) 
#                                                   to initialize
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::LaunchAssistant()
#
#            answer           --> storage variable for the integer returned by TextOrSpeech()
#
#            TextOrSpeech()   --> function to prompt user for integer input in the terminal
#
#            Assist(a_Answer) --> function with two separate variants depending on which 
#                                 variation of the Virtual Assistant is initialized first, 
#                                 decided upon the integer variable answer's value
#
#DESCRIPTION
#
#        This function will call the TextOrSpeech() function to receive an integer value 
#        from the user, and then passes it along to the Assist(a_Answer) function in 
#        order to decide the start state of the Virtual Assistant 
#        (text or voice control).
#
#RETURNS
#
#        No explicitly returned variable. Instead calls one of the two variations 
#        of Assist(a_Answer) depending on the integer variable it received 
#        from TextOrSpeech().
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        11:35pm 8/29/2021                                                          #

def LaunchAssistant():

    answer = TextOrSpeech()

    if answer == 1:

        Assist(1)

    elif answer == 2:

        Assist(2)

#Assistant_Chatbot_Merge::LaunchAssistant()

#Assistant_Chatbot_Merge::DayOfTheWeek() Assistant_Chatbot_Merge::DayOfTheWeek()
#
#NAME
#
#        Assistant_Chatbot_Merge::DayOfTheWeek - when prompted by the user provides 
#                                                the current day of the week both in 
#                                                text format in terminal, in text 
#                                                format in the flask user interface, 
#                                                as well as through audio.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::DayOfTheWeek()
#
#            currentDay       --> storage variable for the numerical value of 
#                                 the current day of the week gotten from the 
#                                 datetime library + 1 to account for indexing
#
#            dictionaryDay    --> dictionary of each day of the week with a 
#                                 numerical value assigned to each, assigned 
#                                 by two linked list of integers and strings
#
#            printableDay     --> storage variable for string returned by cross 
#                                 referencing dictionaryDay by currentDay
#
#DESCRIPTION
#
#        This function will attempt to determine today's current date via the 
#        datetime library and return it as a string to be printed and spoken by 
#        the Virtual Assistant in both the terminal as well as the flask 
#        user interface.
#
#RETURNS
#
#        Returns a string to be passed to the flask user interface that can be 
#        printed in the Virtual Assistant chat bubble. The string contains 
#        the current day of the week assuming datetime has no issues.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        11:00pm 3/26/2021                                                          #

def DayOfTheWeek():

    currentDay = datetime.datetime.today().weekday() + 1

    dictionaryDay = {1: 'Monday', 
                     2: 'Tuesday', 
                     3: 'Wednesday', 
                     4: 'Thursday', 
                     5: 'Friday', 
                     6: 'Saturday', 
                     7: 'Sunday'}

    if currentDay in dictionaryDay.keys():

        printableDay = dictionaryDay[currentDay]

        print(printableDay)
        Speak("Today is " + printableDay)
        return str("Today is " + printableDay)

#Assistant_Chatbot_Merge::DayOfTheWeek()

#Assistant_Chatbot_Merge::WhatTime() Assistant_Chatbot_Merge::WhatTime()
#
#NAME
#
#        Assistant_Chatbot_Merge::WhatTime - when prompted by the user provides 
#                                            the current time in military time 
#                                            both through the flask user interface, 
#                                            the terminal, as well as audio playback.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::WhatTime()
#
#            currentTime      --> storage variable for the current time passed 
#                                 from the datetime library in 00:00:00 format
#
#            hour             --> storage variable for the hour portion of currentTime
#
#            minute           --> storage variable for the minute portion of currentTime
#
#DESCRIPTION
#
#        This function will attempt to use the datetime library to determine the 
#        current time in military time. It then splits the provided information into 
#        just hours and minutes in order to ignore seconds and miliseconds. This value 
#        is then used as audio playback and returned as a string to 
#        the Virtual Assistant.
#
#RETURNS
#
#        Returns a string to the flask user interface and Virtual Assistant to be 
#        printed out on the localhost server. Also provides audio playback of the 
#        string it is returning for the user.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        11:45pm 3/26/2021                                                          #

def WhatTime():
    currentTime = str(datetime.datetime.now())

    print(currentTime)

    hour = currentTime[11:13]
    minute = currentTime[14:16]

    Speak("It is " + hour + " hours and " + minute + " minutes.")
    return str("It is " + hour + " hours and " + minute + " minutes.")

#Assistant_Chatbot_Merge::WhatTime()

#Assistant_Chatbot_Merge::Greeting() Assistant_Chatbot_Merge::Greeting()
#
#NAME
#
#        Assistant_Chatbot_Merge::Greeting - when the chatbot is initialized 
#                                            prints a greeting in the terminal 
#                                            and provides audio playback to let 
#                                            the user know the Virtual Assistant 
#                                            has started up.
#
#SYNOPSIS
#
#        void Assistant_Chatbot_Merge::Greeting()
#
#            print            --> standard terminal text print function for python
#
#            Speak            --> synthesizes the provided text into audio playback
#
#DESCRIPTION
#
#        This function will write greetings text to the terminal and provide audio 
#        feedback when the Virtual Assistant is intialized as confirmation that 
#        the program has started correctly.
#
#RETURNS
#
#        Returns nothing, simply prints to terminal and plays synthesized audio.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        4:15pm 4/01/2021                                                          #

def Greeting():

    print("Greetings, I am your Virtual Assistant. How can I be of assistance?")
    Speak("Greetings, I am your Virtual Assistant. How can I be of assistance?")

#Assistant_Chatbot_Merge::Greeting()

#Assistant_Chatbot_Merge::GoogleLaunch() Assistant_Chatbot_Merge::GoogleLaunch()
#
#NAME
#
#        Assistant_Chatbot_Merge::GoogleLaunch - when prompted by the user launches 
#                                                "google.com" from the user's default 
#                                                browser. Also provides audio feedback 
#                                                and prints to the flask user interface.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::GoogleLaunch()
#
#            webbrowser       --> instance call to launch default browser with the 
#                                 url in the provided string
#
#            Speak            --> synthesizes the provided text to audio playback
#
#DESCRIPTION
#
#        This function will attempt to open "google.com" using the user's default 
#        web browser. It will also print to the terminal, the flask user interface, 
#        and will provide audio playback of the current action.
#
#RETURNS
#
#        Returns a string for the flask user interface to print for the Virtual Assistant. 
#        Otherwise just opens the default webbrowser to "google.com".
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        3:05pm 4/11/2021                                                          #

def GoogleLaunch():

    print("Launching google.com")
    Speak("Launching Google dot Com")

    webbrowser.open("www.google.com")
    return str("Launching google.com")

#Assistant_Chatbot_Merge::GoogleLaunch()

#Assistant_Chatbot_Merge::GoogleQuery(a_Query) Assistant_Chatbot_Merge::GoogleQuery(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::GoogleQuery - when prompted by the user parses a string to 
#                                               remove "google" and then google search the 
#                                               topic of choice. This is being done using 
#                                               letmegooglethatforyou, 
#                                               so that the url being 
#                                               opened by webbrowser never change when the search 
#                                               results change. Making it cross compatible. 
#                                               If no 
#                                               browser is open it will open a new one, 
#                                               otherwise 
#                                               it creates a new tab. 
#                                               Provides audio feedback of 
#                                               the current search and prints to the flask 
#                                               user interface.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::GoogleQuery(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant 
#                                 to the function that is edited to replace the 
#                                 "google" term in the string so that it can be fit 
#                                 into the webbrowser search with no issues.
#
#            Speak            --> function to synthesize a string and output 
#                                 it as audio playback
#
#            webbrowser       --> library to launch specific urls in the 
#                                 default browser from python
#
#DESCRIPTION
#
#        This function will attempt to open a new web browser or browser tab with 
#        the requested url. In this case it is letmegooglethat with the split 
#        a_Query tagged onto the end so that it googles the requested topic 
#        for the user.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant, to be printed out in the flask 
#        user interface on the localhost server. Also provides audio playback 
#        as well as launches a browser tab with the requested information.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        7:36pm 4/12/2021                                                          #

def GoogleQuery(a_Query):

    a_Query = a_Query.replace("google", "")

    print("Googling: " + a_Query)
    Speak("Googling: " + a_Query)

    webbrowser.open("https://letmegooglethat.com/?q=" + a_Query)

    return str("Googling: " + a_Query)

#Assistant_Chatbot_Merge::GoogleQuery(a_Query)

#Assistant_Chatbot_Merge::GoodbyeStatement(a_Query) Assistant_Chatbot_Merge::GoodbyeStatement(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::GoodbyeStatement - when prompted by the user via the "goodbye" 
#                                                    command, prompts the user back to confirm 
#                                                    that they actually do want to close the 
#                                                    program or if 
#                                                    they would like to cancel 
#                                                    the action. Following through with the 
#                                                    process stops the 
#                                                    localhost server and 
#                                                    Virtual Assistant from functioning. 
#                                                    Refreshing the page will confirm this 
#                                                    if need be.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::GoodbyeStatement(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant 
#                                 to the function to confirm that the user started 
#                                 the goodbye exit action. The variable is then 
#                                 repurposed for their response between 'Y' or 'N' 
#                                 and returned to the flask user interface or 
#                                 terminal for the appropriate action.
#
#            Speak            --> function to synthesize a string and output 
#                                 it as audio playback
#
#DESCRIPTION
#
#        This function will attempt to prompt the user ton confirm if they want 
#        to exit the Virtual Assistant program or not. Whether the user elects 
#        to cancel or proceed the decision is passed back to the Virtual Assistant 
#        or Terminal to be acted upon. 'Y' will summarily close the program and 
#        server, while 'N' cancels the goodbye action.
#
#RETURNS
#
#        Returns a string to the Virtual Assitant or Terminal, so that it can 
#        decide whether to close the localhost server, or cancel the action 
#        depending on the response. Provides audio playback and prints to the 
#        terminal as well as the flask user interface.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        9:30pm 9/12/2021                                                          #

def GoodbyeStatement(a_Query):

    print("Are you sure you want to say Goodbye? Please input Y to confirm, or N to cancel: ")
    Speak("Are you sure you want to say Goodbye?")

    for i in range(5):

        a_Query = input()

        if a_Query == 'Y':

            print("Goodbye! Until next time.")
            Speak("Goodbye! Until next time.")

            return a_Query
    
        elif a_Query == 'N':

            print("Shutdown Request Canceled.")
            Speak("Shutdown Request Canceled.")

            return a_Query
            
        elif (a_Query != 'Y' and a_Query != 'N'):

            print("Invalid Input Received, Please Try Again (Y/N): ")
            Speak("Invalid Input Received, Please Try Again.")

            i = 0

#Assistant_Chatbot_Merge::GoodbyeStatement(a_Query)

#Assistant_Chatbot_Merge::GoodbyeStatementVoice(a_Query) Assistant_Chatbot_Merge::GoodbyeStatementVoice(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::GoodbyeStatementVoice - when prompted by the user requests whether 
#                                                         they want to continue with or cancel the 
#                                                         exit action for the 
#                                                         localhost server or terminal. 
#                                                         This variant of the function uses voice command 
#                                                         instead of text input for when the 
#                                                         Virtual Assistant is in voice control mode.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::GoodbyeStatementVoice(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant 
#                                 to the function to confirm whether the user wants 
#                                 to exit the program or cancel the action. 
#                                 Repurposed after the fact for the user's voice 
#                                 command input between 'yes' and 'no'.
#
#            Speak            --> function to synthesize a string and output 
#                                 it as audio playback
#
#DESCRIPTION
#
#        This function will attempt to prompt the user if they want to close the 
#        localhost server/terminal or cancel the goodbye action they started.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant or Terminal to be used to determine 
#        whether the program will close or continue. Also provides audio playback 
#        of which selection the user chose. If an incorrect selection has been given 
#        it will reprompt the user.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        9:40pm 9/12/2021                                                          #

def GoodbyeStatementVoice(a_Query):

    print("Are you sure you want to say Goodbye? Please input Y to confirm, or N to cancel: ")
    Speak("Are you sure you want to say Goodbye? Please state yes to confirm, or no to cancel: ")

    for i in range(5):

        a_Query = ListenCheck().lower()

        if a_Query == "yes":

            print("Goodbye! Until next time.")
            Speak("Goodbye! Until next time.")

            return a_Query

        elif a_Query == "no":

            print("Shutdown Request Canceled.")
            Speak("Shutdown Request Canceled.")

            return a_Query

        elif (a_Query != "yes" and a_Query != "no"):

            print("Invalid Input Received, Please Try Again (Y/N): ")
            Speak("Invalid Input Received, Please Try Again.")

            i = 0

#Assistant_Chatbot_Merge::GoodbyeStatementVoice(a_Query)

#Assistant_Chatbot_Merge::FromWikipedia(a_Query) Assistant_Chatbot_Merge::FromWikipedia(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::FromWikipedia - when prompted by the user will use the 
#                                                 wikipedia python library to search for 
#                                                 the highest similariy webpage to the 
#                                                 string provided in a_Query. It then 
#                                                 provides the user with basic information 
#                                                 about that topic based on what wikipedia 
#                                                 has stored on their website. Does not 
#                                                 function without internet.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::FromWikipedia(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant. 
#                                 The included string data is parsed to remove 
#                                 "wikipedia" from the string and is then used with 
#                                 the wikipedia library to search for the topic most 
#                                 similar to the string a_Query.
#
#            result           --> string variable storing the first sentence of the 
#                                 article pulled up by the wikipedia function using 
#                                 a_Query as a search term
#
#DESCRIPTION
#
#        This function will attempt to poll from the wikipedia online database and 
#        receive the first sentence from the starting paragraph at the top of the 
#        page matching whatever search term has been provided. It will play the 
#        information back in audio form as well as will print it into the 
#        flask user interface.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant of the first sentence of the 
#        polled wikipedia page. This information is also provided in audio 
#        playback format for the user through the terminal. The polled sentence 
#        is then printed to the flask user interface.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        2:22pm 5/01/2021                                                          #

def FromWikipedia(a_Query):

    a_Query = a_Query.replace("wikipedia", "")

    print("Searching wikipedia for " + a_Query)
    Speak("Searching wikipedia for " + a_Query)

    result = wikipedia.summary(a_Query, sentences=1)

    print("According to wikipedia: ")
    Speak("According to wikipedia")

    print(result)
    Speak(result)

    return str("According to wikipedia: " + result)

#Assistant_Chatbot_Merge::FromWikipedia(a_Query)

#Assistant_Chatbot_Merge::NameResponse() Assistant_Chatbot_Merge::NameResponse()
#
#NAME
#
#        Assistant_Chatbot_Merge::NameResponse - when prompted by the user for the 
#                                                virtual assistant's name provides 
#                                                the requested information as well 
#                                                as tells them about the HELP function 
#                                                for a list of commands.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::NameResponse()
#
#            Speak            --> function to synthesize a string and output 
#                                 it as audio playback
#
#DESCRIPTION
#
#        This function will both print and speak the provided line of dialogue below, 
#        as well as will pass the line of dialogue to the localhost server to be 
#        printed out there as well.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant to be printed out in the 
#        flask user interface. Also provides audio playback.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        12:01pm 6/06/2021                                                          #

def NameResponse():

    print("I am your virtual desktop assistant Vai, feel free to ask me anything. If you need help use the command HELP for options.")
    Speak("I am your virtual desktop assistant Vai, feel free to ask me anything. If you need help use the command HELP for options.")

    return str("I am your virtual desktop assistant Vai, feel free to ask me anything. If you need help use the command HELP for options.")

#Assistant_Chatbot_Merge::NameResponse()

#Assistant_Chatbot_Merge::NoteQuery(a_Query) Assistant_Chatbot_Merge::NoteQuery(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::NoteQuery - when prompted by the user parses the passed 
#                                             string a_Query to remove the command words 
#                                             and then saves them to a text file saved 
#                                             in the installation directory.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::NoteQuery(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant 
#                                 to the function that is split so that select words 
#                                 can be chosen to be saved in the text file.
#
#            removalWords     --> list of words to ignore after splitting a_Query
#
#            queryWords       --> string list of the split words from a_Query
#
#            noteWords        --> string list of the strings in queryWords 
#                                 minus anything also present in removalWords
#
#            note             --> string variable of all the strings in 
#                                 noteWords joined together into a single string 
#                                 instead of a list
#
#            textFile         --> object used to open and write the 'note' string 
#                                 to the designated 'assistant_Note.txt' file
#
#DESCRIPTION
#
#        This function will attempt to parse from user input a string to be saved 
#        to the text file in the installation directory underneath the 'notes' folder.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant to let the user know their note 
#        has been recorded. Also saves their input string minus 'make', 'a', 'note' 
#        to the designated text file. Provides audio playback of the 
#        confirmation statement.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        11:36pm 9/06/2021                                                          #

def NoteQuery(a_Query):

    removalWords = ['make', 'a', 'note']
    queryWords = a_Query.split()

    noteWords = [word for word in queryWords if word.lower() not in removalWords]
    note = ' '.join(noteWords)

    textFile = open(join("notes", "assistant_Note.txt"), "a+")

    textFile.write(note + "\r\n")
    textFile.close()

    print("The note has been recorded and saved in the notes folder in the installation directory.")
    Speak("The note has been recorded and saved in the notes folder in the installation directory.")

    print(a_Query)
    
    return str("The note has been recorded and saved in the notes folder in the installation directory.")

#Assistant_Chatbot_Merge::NoteQuery(a_Query)

#Assistant_Chatbot_Merge::NoteQueryVoice(a_Query) Assistant_Chatbot_Merge::NoteQueryVoice(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::NoteQueryVoice - when prompted by the user reprompts them for a 
#                                                  second audio statement that the program can 
#                                                  parse into a string to be saved in the text file 
#                                                  in the local installation directory.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::NoteQueryVoice(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant to start the 
#                                 function. Reused to store the user's microphone input for the 
#                                 note that is to be recorded.
#
#            textFile         --> object to store, open, close, and write to the designated text 
#                                 file in the 'notes' directory of the local installation
#
#DESCRIPTION
#
#        This function will attempt to open a text file from the 'notes' directory and will save 
#        the user's prompted audio input as a string within that text file. Simpler than the 
#        non-voice application as this one can reprompt the user prior to writing the note, 
#        as the other one creates the note instantaneously.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant for user confirmation that their 
#        note has been created. Also provides audio playback and saves their 
#        microphone input to the local text file in 'notes'.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        12:05am 9/07/2021                                                          #

def NoteQueryVoice(a_Query):

    print("What would you like me to make note of?")
    Speak("What would you like me to make note of?")

    textFile = open(join("notes", "assistant_Note.txt"), "a+")

    a_Query = ListenCheck().lower()

    textFile.write(a_Query + "\r\n")
    textFile.close()

    print("The note has been recorded and saved in the notes folder in the installation directory.")
    Speak("The note has been recorded and saved in the notes folder in the installation directory.")

    print(a_Query)
    a_Query = ""
    print(a_Query)

#Assistant_Chatbot_Merge::NoteQueryVoice(a_Query)

#Assistant_Chatbot_Merge::GetChatbotResponse(a_Query) Assistant_Chatbot_Merge::GetChatbotResponse(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::GetChatbotResponse - when prompted by the user takes their input 
#                                                      and provides it to 
#                                                      the chatbot instance, which 
#                                                      then decides using it library its' response 
#                                                      with the highest similarity using the 
#                                                      Levenshtein Distance. 
#                                                      The best result it then 
#                                                      printed to the terminal. This function is for 
#                                                      using the chatbot without the 
#                                                      flask user interface in offline mode.
#
#SYNOPSIS
#
#        void Assistant_Chatbot_Merge::GetChatbotResponse(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant 
#                                 to the function to the chatbot instance to allow 
#                                 for a response with high similarity to be provided.
#
#            botResponse      --> string storage variable for the chatbot's 
#                                 response based on the contents of a_Query
#
#DESCRIPTION
#
#        This function will attempt to open take the provided user input, whether 
#        voice or text, and will provide a chatbot response with the highest 
#        similarity according to its' database.
#
#RETURNS
#
#        Does not have a strict return, but does provide audio playback of 
#        the response and prints it to the terminal.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        8:05pm 4/23/2021                                                          #

def GetChatbotResponse(a_Query):

    botResponse = dialogueBot.get_response(a_Query)

    print(botResponse)
    Speak(botResponse)

#Assistant_Chatbot_Merge::GetChatbotResponse(a_Query)

#Assistant_Chatbot_Merge::PlayAudioFile(a_Query) Assistant_Chatbot_Merge::PlayAudioFile(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::PlayAudioFile - after creating an audio folder in the C: 
#                                                 directory plays the selected audio file 
#                                                 based on user input
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::PlayAudioFile(a_Query)
#
#            a_Query          --> string variable from the Virtual Assistant edited 
#                                 and saved into the song variable without 'play ', 
#                                 and with the addendum '.mp3'
#
#            song             --> string storage variable for the song name to be 
#                                 played via the startfile(path) function
#
#            startfile        --> os library function to launch the file at the 
#                                 designated path with its' default application, 
#                                 in this instance an audio file
#
#DESCRIPTION
#
#        This function will attempt to parse a song name from user input and 
#        search the path to the default 'audio' directory for it, if it exists 
#        it will launch the file with its' default program
#
#RETURNS
#
#        Returns a string to the Virtual assistant to confirm that the designated 
#        audio file has been played. Also launches said audio file with the 
#        machine's default audio program.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        8:45pm 9/15/2021                                                          #

def PlayAudioFile(a_Query):

    song = a_Query.replace("play ", "") + ".mp3"
    Speak("Playing song labeled: " + song)
    
    os.startfile('C:\\audio\\' + song)

    a_Query = ""

    return str("Playing song labeled: " + song)

#Assistant_Chatbot_Merge::PlayAudioFile(a_Query)

#Assistant_Chatbot_Merge::OpenEmail() Assistant_Chatbot_Merge::OpenEmail()
#
#NAME
#
#        Assistant_Chatbot_Merge::OpenEmail - when prompted by the user launches their 
#                                             gmail using the webbrowser library functions, 
#                                             also provides audio playback.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::OpenEmail()
#
#            Speak            --> function to synthesize a string and output 
#                                 it as audio playback
#
#            webbrowser       --> library to launch specific urls in the 
#                                 default browser from python
#
#DESCRIPTION
#
#        This function will attempt to launch the user's gmail using their default browser, 
#        if they have signed out they will need to sign in on the new tab that opens. 
#        If no browser is currently open it will launch a new instance.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant to be printed for confirmation 
#        that it is attempting to launch their gmail through the webbrowser library. 
#        Also provides audio playback.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        8:45pm 9/15/2021                                                          #

def OpenEmail():

    print("Launching Gmail...")
    Speak("Launching Gmail.")

    webbrowser.open("https://gmail.com")

    return str("Launching Gmail")

#Assistant_Chatbot_Merge::OpenEmail()

#Assistant_Chatbot_Merge::SetAlarm(a_Query) Assistant_Chatbot_Merge::SetAlarm(a_Query)
#
#NAME
#
#        Assistant_Chatbot_Merge::SetAlarm - when prompted by the user attempts to 
#                                            set an alarm at the designated hour in 
#                                            military time.
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::SetAlarm(a_Query)
#
#            a_Query          --> string variable passed from the Virtual Assistant 
#                                 to the function that contains an integer between 
#                                 1 and 24. Used to set the alarm.
#
#            currentTime      --> variable to storm the current time in 00:00:00 
#                                 format
#
#            alarmTime        --> variable to store the alarm time based on the 
#                                 difference between the integer value given in 
#                                 a_Query and currentTime
#
#            alarm            --> string varialbe that stores the name of the 
#                                 alarm sound in the 'audio' file related to 
#                                 the local installation directory
#
#DESCRIPTION
#
#        This function will attempt to set an alarm via the standard sleep() 
#        function based on the value given from a_Query. When the alarm 
#        finishes it will play the designated audio file through the default 
#        audio player. In this instance sleep() does not freeze the program 
#        when running on the localhost as flask is creating multiple threads 
#        and processes.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant to give the user confirmation 
#        that an alarm has been set. When the alarm finishes/goes off plays 
#        the designated audio file.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        9:00pm 9/15/2021                                                          #

def SetAlarm(a_Query):

    print("Setting Alarm")
    Speak("Setting Alarm")

    currentTime = datetime.datetime.now()
    alarmTime = datetime.datetime.combine(currentTime.date(), datetime.time(a_Query, 0, 0))

    time.sleep((alarmTime - currentTime).total_seconds())

    alarm = 'Loud_Alarm_Clock_Buzzer'

    os.startfile('C:\\audio\\' + alarm)

    return str("Setting Alarm for " + str(a_Query) + " hours.")

#Assistant_Chatbot_Merge:SetAlarm(a_Query)

#Assistant_Chatbot_Merge::LaunchProgram(a_Path) Assistant_Chatbot_Merge::LaunchProgram(a_Path)
#
#NAME
#
#        Assistant_Chatbot_Merge::LaunchProgram - launches the designated program based on name, 
#                                                 to set a program up to be used 
#                                                 with the Virtual Assistant, 
#                                                 simply add a text file with its name, 
#                                                 with the contents being the path where 
#                                                 each '\' is instead a '\\'
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::LaunchProgram(a_Path)
#
#            a_Path           --> string variable passed from the Virtual Assistant 
#                                 that contains the name of the txt file to open for 
#                                 the desired program
#
#            fileName         --> a_Path appended with a '.txt' on the end
#
#            file             --> object used with os library to open and read 
#                                 from the file matching fileName
#
#            program          --> string varialbe storing the text contained 
#                                 within the filed opened and read by 'file'
#
#            subprocess.call  --> function from the subprocess library that 
#                                 launches the program at the designated path 
#                                 provided by 'program'
#
#DESCRIPTION
#
#        This function will attempt to take the filename from a_Path and open the 
#        corresponding textfile, reading in the file path contained within. 
#        It will then attempt to launch the program at said location.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant to provide the user with 
#        confirmation that it is launching their application. Provides audio 
#        playback and genuinely launches their pgoram if it exists at the 
#        designated location within the provided textfile.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        7:30pm 8/27/2021                                                          #

def LaunchProgram(a_Path):

    fileName = a_Path + ".txt"
    file = open(join("paths", fileName), 'r')

    program = file.read()

    print("Launching Program...")
    Speak("Launching Program")

    subprocess.call([program])

    return str("Launching Program: " + a_Path)

#Assistant_Chatbot_Merge::LaunchProgram(a_Path)

#Assistant_Chatbot_Merge::Help() Assistant_Chatbot_Merge::Help()
#
#NAME
#
#        Assistant_Chatbot_Merge::Help - when prompted by the user returns a list 
#                                        of currently available commands for the 
#                                        Virtual Assistant that can be used
#
#SYNOPSIS
#
#        string Assistant_Chatbot_Merge::Help()
#
#            helpFile         --> object used to open, read, write, and close the 
#                                 text file associated with the command list.
#
#            helpString       --> string variable to store the contents of 
#                                 helpFile to be printed to the flask user interface
#
#DESCRIPTION
#
#        This function will attempt to open the text file help_txt and print it out 
#        to the user in the localhost server so that they can view a commands list 
#        for the Virtual Assistant if they want to know what things it is capable of.
#
#RETURNS
#
#        Returns a string to the Virtual Assistant that it can print out as a 
#        command list for the user to utilize when interacting with the 
#        Virtual Assistant itself.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        5:54pm 9/23/2021                                                          #

def Help():

    helpFile = open(join("help_text", "help_function_text.txt"), 'r')
    helpString = helpFile.read()

    return str(helpString)

#Assistant_Chatbot_Merge::Help()

#Assistant_Chatbot_Merge::Assist(a_Answer) Assistant_Chatbot_Merge::Assist(a_Answer)
#
#NAME
#
#        Assistant_Chatbot_Merge::Assist - function utilized to run the Virtual Assistant 
#                                          in offline mode without the localhost server 
#                                          or flaskUI, allows for text control or voice 
#                                          control upon initialization.
#
#SYNOPSIS
#
#        void Assistant_Chatbot_Merge::Assist(a_Answer)
#
#            a_Answer         --> integer variable passed to the function through 
#                                 user input in the terminal window, can have a value 
#                                 of 1 or 2. Controls the bootup mode of the 
#                                 Virtual Assistant
#
#            query            --> string variable storing user input from the 
#                                 terminal or synthesized from their microphone 
#                                 in voice control mode
#
#DESCRIPTION
#
#        Controller function for the Virtual Assistant when it is not being used on 
#        the flask user interface or localhost server. Determines whether the 
#        program is being operated in text control or voice control mode. Depending 
#        on user input can call any of the functions associated with the 
#        Virtual Assistant or chatbot in order to trigger an action or response.
#
#RETURNS
#
#        Does not explicitly return anything. Some of the functions that Assist(a_Answer) 
#        calls can return a string or integer variable. If no functions are called and 
#        the chatbot is utilized it simply prints the response to the terminal and 
#        provides audio playback. If an invalid response is somehow provided will 
#        raise an exception. Can be used to turn the program off.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        4:30pm 4/11/2021                                                          #

def Assist(a_Answer):
    Greeting()

    #Provides text control of the Virtual Assistant
    if a_Answer == 1:

        while(True):
            
            query = input()

            if "open google" in query:

                #Attempts to Launch google.com with the default browser
                GoogleLaunch()

                query = ""

                continue

            elif "google" in query:

                #Attempts to search google.com using the provided query term
                GoogleQuery(query)

                query = ""

                continue

            elif "what day is it" in query:

                #Prints out and playsback audio for the day of the week
                DayOfTheWeek()

                query = ""

                continue

            elif "what time is it" in query:

                #Prints out and playsback audio for the time in military time
                WhatTime()

                query = ""

                continue

            elif "goodbye" in query:

                #Checks whether the user really wants to exit the Virtual Assistant
                query = GoodbyeStatement(query)
                
                if query == 'Y':

                    break
                
                elif query == 'N':

                    continue

                else:

                    raise ValueError('Response in Query Invalid After Executing goodbyeStatement(query)')

            elif "from wikipedia" in query:

                #Prints and speaks the first sentence from the 
                #corresponding wikipedia page designated by query
                FromWikipedia(query)

                query = ""

                continue

            elif "who are you" in query:

                #Prints out the bots name and notifies the user of the HELP command
                NameResponse()

                query = ""

                continue
            

            elif "make a note" in query:

                #Parses user input to make a note of anything in the string 
                #except for 'make a note' and saves it in the local 'notes directory'
                NoteQuery(query)

                query = ""

                continue

            else:

                #Pulls a response from the chatbot algorithm based on the query 
                #if it matches no Virtual Assistant Commands
                GetChatbotResponse(query)

                query = ""

                continue


    #Provides voice control of the Virtual Assistant
    elif a_Answer == 2:

        while(True):

            #User input from their microphone instead of the terminal
            query = ListenCheck().lower()

            if "open google" in query:

                GoogleLaunch()

                query = ""

                continue

            elif "google" in query:
            
                GoogleQuery(query)

                query = ""

                continue

            elif "what day is it" in query:

                DayOfTheWeek()

                query = ""

                continue

            elif "what time is it" in query:

                WhatTime()

                query = ""

                continue

            elif "goodbye" in query:

                #Checks whether the user would actually like to exit the 
                #Virtual Assistant via voice control
                query = GoodbyeStatementVoice(query)

                if query == "yes":

                    break

                elif query == "no":

                    continue

                else:

                    raise ValueError('Response in Query Invalid After Executing goodbyeStatementVoice(query).')

            elif "from wikipedia" in query:

                FromWikipedia(query)

                query = ""

                continue

            elif "who are you" in query:

                NameResponse()

                query = ""

                continue
            

            elif "make a note" in query:

                #Prompts the user after stating the command to input 
                #a new statement, which it records in a note in 
                #the'notes' folder of the installation directory
                NoteQueryVoice(query)

                query = ""

                continue

            else:

                GetChatbotResponse(query)

                query = ""

                continue
    else:

        raise Exception('Returned Answer value for TextOrSpeech() Invalid.')

#Assistant_Chatbot_Merge:Assist(a_Answer)

#Assistant_Chatbot_Merge::dialogueBot Assistant_Chatbot_Merge::dialogueBot
#
#NAME
#
#        Assistant_Chatbot_Merge::dialogueBot - object containing the settings 
#                                               and responses for the chatbot 
#                                               portion of the Virtual Assistant
#
#SYNOPSIS
#
#        obj Assistant_Chatbot_Merge::dialogueBot
#
#            statement_comparison_function --> settings containing the desired algorithm 
#                                              to use when determining the chatbot's responses
#
#            utils                         --> setting for picking from chatterbot built-in 
#                                              utility functions, in this case we are removing 
#                                              stopwords like 'uh' or 'the' to get a 
#                                              better response
#
#            parsing                       --> setting that can allow the chatbot to respond 
#                                              with the current date and time if it feels 
#                                              the user is asking for it
#
#            preprocessors                 --> settings for the chatbot to parse through user 
#                                              input that removes unnecessary whitespace from 
#                                              the string, removes escape characters from html 
#                                              links it can see, and can convert hexadecimal 
#                                              to ascii if required.
#
#            filters                       --> filter to skip repetitive responses and 
#                                              provide the previous answer to save 
#                                              computing time
#
#            read_only                     --> prevents the chatbot from editing 
#                                              user input outside of copying the provided 
#                                              string into its' own local variable
#
#            logic_adapters                --> chatterbot settings and functions that enable 
#                                              it to do basic math provided by the user, 
#                                              and to constrain its search parameters even 
#                                              further from the algorithm chosen above. 
#                                              This can help improve the quality of 
#                                              responses provided by the chatbot.
#
#            input_adapter                 --> sets the location for where the 
#                                              chatbot can read user input from
#
#            outputer_adapter              --> sets the location for where the 
#                                              chatbot can send its' responses for 
#                                              printing and audio playback
#
#DESCRIPTION
#
#        This object initializes all settings for our chatbot and dictates how it 
#        works and responds ot user input. Many of these settings can be changed 
#        and have numerous other options available within the chatterbot library. 
#        The most impactful change would be altering the algorithm it is using, 
#        which is likely to provide different responses.
#
#RETURNS
#
#        Since this is an object/data type it does not return any information, 
#        instead it is an instance of out chatbot which we will be passing to the 
#        rest of the program to utilize when a Virtual Assistant function 
#        has not been called by the user.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        1:15pm 3/15/2021                                                          #

dialogueBot = ChatBot(name = 'Vai', 
                        statement_comparison_function = LevenshteinDistance,

                        utils = ['chatterbot.utils.remove_stopwords'],

                        parsing = ['chatterbot.parsing.datetime_parsing'],

                        preprocessors= ['chatterbot.preprocessors.clean_whitespace', 
                                        'chatterbot.preprocessors.unescape_html', 
                                        'chatterbot.preprocessors.convert_to_ascii'],

                        filters = ['chatterbot.filters.RepetitiveResponseFilter'],

                        read_only=True, 

                        logic_adapters= ['chatterbot.logic.MathematicalEvaluation', 
                                        'chatterbot.logic.BestMatch', 
                                        'chatterbot.logic.TimeLogicAdapter',

                                            {'import_path': 'chatterbot.logic.BestMatch',
                                            'default_response': 'I do not understand your statement. Please try again.',
                                            'maximum_similarity_threshold': 0.80
                                            }
                                        ],

                        input_adapter='chatterbot.input.TerminalAdapter',

                        outputer_adapter='chatterbot.output.TerminalAdapter')

#Assistant_Chatbot_Merge::dialogueBot


#Utilized if running Virtual Assistant without the user interface
if __name__ == "__main__":
    LaunchAssistant()

# Assistant_Chatbot_Merge.py




