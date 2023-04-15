#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import the MongoClient class
from pymongo import MongoClient, errors

# global variables for MongoDB host (default port is 27017)
DOMAIN = 'mongodb://mongo'
PORT = 27017

def create_client():
    # use a try-except indentation to catch MongoClient() errors
    try:
        # try to instantiate a client instance
        client = MongoClient(
            host = [ str(DOMAIN) + ":" + str(PORT) ],
            serverSelectionTimeoutMS = 3000, # 3 second timeout
            username = "root",
            password = "example",
        )

        return client

    except errors.ServerSelectionTimeoutError as err:
        return None