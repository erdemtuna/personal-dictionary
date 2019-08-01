#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json
from DataToPDF import DataToPDF

client = MongoClient(
    '<YOUR MONGODB CREDENTIAL')
db = client.get_database('YOUR DICT')
trans = db.translations

# print(trans.count_documents({}))

dict_keys = ('word', 'means', 'use')
states = ('1', 'word', '2', 'pdf', '3', 'quit')
more_words = ('y', 'yes', 'n', 'no')

QUIT = False

while not (QUIT):
    # determine the state
    user_in = input('Word(1) or Export PDF(2) or  Quit(3): ')
    # turn input to lowercase
    user_low = user_in.lower()
    # array of json objects
    temp_array = []
    # user wants to enter new word
    if(user_low == states[0] or user_low == states[1]):
        # want to continue adding words?
        more = True
        while(more):
            # the temporary json object to store user input
            temp_json = {}
            for key in dict_keys:
                if(key == dict_keys[0]):
                    # get the original word
                    word_in = input('Enter original word: ')
                    # dump to json in all lowercase
                    temp_json[key] = word_in.lower()
                elif(key == dict_keys[1]):
                    # get the translation
                    means_in = input('Enter the translation: ')
                    # dump to json in all lowercase
                    temp_json[key] = means_in.lower()
                elif(key == dict_keys[2]):
                    # get the sample sentence
                    use_in = str(input('Enter the sample sentence: '))
                    # dump to json
                    temp_json[key] = use_in
                    command_in = input(
                        'Want to add more words? (Y)es or (N)o?')
                    command_low = command_in.lower()
                    # user doesn't want to add more words
                    if(command_low != more_words[0] and command_low != more_words[1]):
                        more = False
                    # dump json object to json array
                    temp_array.append(temp_json)
        # convert array to json array
        json_array = json.loads(json.dumps(
            temp_array, ensure_ascii=False).encode('utf8'))
        # insert to database
        print(json_array)
        trans.insert_many(json_array)
    # user wants to quit
    elif(user_low == states[4] or user_low == states[5]):
        QUIT = True
        print('Quit Successful.')
    # user wants to export data to pdf
    elif(user_low == states[2] or user_low == states[3]):
        t = DataToPDF(trans.find())
        t.run()
        QUIT = True
        print('Export Successful.')
    # not a valid command
    else:
        print('Not a valid command')
