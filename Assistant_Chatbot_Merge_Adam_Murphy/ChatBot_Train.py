#ChatBot_Train.py
#
#NAME
#
#        ChatBot_Train - file and controller to allow the user to train the ChatBot with 
#                        whatever database they would like, by default has the chatterbot 
#                        ListTrainer and UbuntuCorpusTrainer being used with the 
#                        databases in the local installation directory.
#
#SYNOPSIS
#
#        ChatBot_Train.py
#
#            chatterbot              --> library that includes all chatbot functions for 
#                                        initialization, training, and interactivity 
#
#            Assistant_Chatbot_Merge --> file housing the majority of the functions utilized 
#                                        by the Virtual Assistant, as well as the individual 
#                                        chatbot instance. Can be used to run without 
#                                        the flask server.
#
#            ChatterBotCorpusTrainer --> Trains the chatbot using webbased corpus's set in the 
#                                        chatterbot library, the user can utilize and install 
#                                        their own corpus to run from as well if they want to, 
#                                        languages can be chosen from though most options 
#                                        are very bare bones
#
#            UbuntuCorpusTrainer     --> Downloads and trains off of the Ubuntu Dialogue corpus, 
#                                        this is a very large corpus and takes an extremely 
#                                        long time to both download as well as train
#
#            LevenshteinDistance     --> algorithm for deciding chatbot response similarity, 
#                                        dictates how the chatbot responds to the user after 
#                                        training has been complete 
#
#            os                      --> standard python library for opening, reading, and 
#                                        writing files
#
#            dialogueBot             --> necessary chatbot object being passed through 
#                                        for the trainer to train
#
#DESCRIPTION
#
#        This file is to be used to train the chatbot instance used within the 
#        Virtual Assistant, it can be modified to train the chatbot with different 
#        databases. If the chatbot needs to be wiped the database can be 
#        deleted from the program's local directory.
#
#RETURNS
#
#        This is a program so it doesn't technically have a return, 
#        however it creates a database for the chatbot to use when 
#        it is deciding its' responses.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        7:00pm 4/27/2021                                                          #

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from os.path import join
from Assistant_Chatbot_Merge import dialogueBot

#ChatBot_Train::ChatterbotTrain(a_DialogueBot) ChatBot_Train::ChatterbotTrain(a_DialogueBot)
#
#NAME
#
#        ChatBot_Train::ChatterbotTrain - runs through the provided trainers and 
#                                         databases and creates a database for 
#                                         the chatbot to create responses from
#
#SYNOPSIS
#
#        void ChatBot_Train::ChatterbotTrain(a_DialogueBot)
#
#            a_DialogueBot            --> variable passed from the 
#                                         Assistant_Chatbot_Merge file that 
#                                         holds the chatbot initialization 
#                                         and settings
#
#            trainingData             --> object to open and store the database 
#                                         file being used to train the chatbot instance
#
#            trainer1                 --> object to process and train the chatbot 
#                                         via the ListTrainer utilizing the database 
#                                         passed from trainingData
#
#            trainer2                 --> similar to trainer1 this is an object to 
#                                         process and train the chatbot utilizing 
#                                         the Ubuntu Dialogue Corpus
#
#DESCRIPTION
#
#        Standard chatterbot training function that utilizes both the ListTrainer 
#        to use my personal dialogue database, as well as the Ubuntu Dialogue Corpus 
#        to get an even larger sample set. The trainers can be easily altered, 
#        and to change the ListTrainer all that need be done is alter the file 
#        being used for training.
#
#RETURNS
#
#        No explicit return type to be saved into a variable or object. 
#        Instead creates a sql database that the chatbot polls from when it is 
#        attempting to determine response similarity and formulate something 
#        to print to the terminal and user interface.
#
#AUTHOR
#
#        Adam Murphy
#
#DATE
#
#        3:30pm 8/05/2021                                                          #

def ChatterbotTrain(a_DialogueBot):

    #movie_lines.txt is by default in the installation directory of this program
    trainingData = open('cornell movie-dialogs corpus/movie_lines.txt').read().splitlines()

    trainer1 = ListTrainer(a_DialogueBot)
    trainer1.train(trainingData)
    trainer1.train("chatterbot.corpus.english")

    trainer2 = UbuntuCorpusTrainer(a_DialogueBot)
    trainer2.train()

#ChatBot_Train::ChatterbotTrain(a_DialogueBot)

if __name__ == "__main__":
    ChatterbotTrain(dialogueBot)

#ChatBot_Train.py
