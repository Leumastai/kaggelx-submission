"""
This module contains all functions related to MongoDB
"""


import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


def initialise_mongo_cloud_db_client(mongodb_username, mongodb_password, mongodb_cluster):

    uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@{mongodb_cluster}.y5yol6w.mongodb.net/?retryWrites=true&w=majority"
    
    # Create a new client and connect to the server
    client = MongoClient(uri)
    return client


def input_data_into_mongo_db_collection(
    client, db_name, collection_name, input_data_dict
):
    """
    This function takes a client, database_name, collections_name, and input_data_dict
    and pushes that data onto the db collection
    """
    # Connect to the specific collection
    db = client[db_name]
    collection = db[collection_name]

    # Add data to the collection
    collection.insert_many(input_data_dict)

  
def input_document_list_into_mongo_db_collection(client, db_name, collection_name, document_list):
    """
    This function takes a client, database_name, collections_name, and input_data_dict
    and pushes that data onto the db collection
    """
    # Connect to the specific collection
    db = client[db_name]
    collection = db[collection_name]
    
    # Add data to the collection
    collection.insert_many(document_list)
    
    
def get_all_documents_from_mongo_collection(client, db_name, collection_name):
    """
    This function returns a generator of all the documents in a collection
    """
    # Connect to the specific collection
    db = client[db_name]
    collection = db[collection_name]

    all_docs_gen = collection.find({})
    
    return all_docs_gen


def get_document_dict_for_mongo_db_collection_by_object_id(client, db_name, collection_name, object_id):
    
    # Initialise the db connection
    db = client[db_name]
    collection = db[collection_name]
    
    # Read in the document given the object id
    doc_dict = collection.find_one({"_id" : ObjectId(object_id)})
    
    return doc_dict


def search_mongo_collection_by_key_and_search_term(client, db_name, collection_name, key_name, search_term, match_type = 'full'):
    """
    This is a function that looks for a value in a key in a collection in a db
    """
    db = client[db_name]
    collection = db[collection_name]
    
    if match_type == 'full':
        search_results_gen = collection.find({key_name:search_term})
    elif match_type == 'partial':
        search_results_gen = collection.find({key_name: {'$regex' : search_term}})
        
    return search_results_gen


def search_mongo_collection_by_multiple_key_and_search_term(client, db_name, collection_name, key_list, search_term_list):
    """
    This function searches for a mongo collection by taking a list of keys and their corresponding search terms
    """
    search_dict = {}

    for i in range(len(key_list)):
        key = key_list[i]
        search_term = search_term_list[i]
        s_dict = {key:search_term}
        search_dict.update(s_dict)

    db = client[db_name]
    collection = db[collection_name]
    search_results_gen = collection.find(search_dict)
    
    return search_results_gen


def update_mongo_collection_document(client, db_name, collection_name, content_id, input_data_dict):
    """
    This function takes a client, database_name, collections_name, and input_data_dict
    and pushes that data onto the db collection
    """
    # Connect to the specific collection
    db = client[db_name]
    collection = db[collection_name]
    
    # Update the document
    query = {"_id" : ObjectId(content_id) }
    result = collection.replace_one(query, input_data_dict)
    
    
def update_mongo_collection_document_by_str_id(client, db_name, collection_name, content_id, input_data_dict):
    """
    This is for cases where we have explicitly declared the
    """
    """
    This function takes a client, database_name, collections_name, and input_data_dict
    and pushes that data onto the db collection
    """
    # Connect to the specific collection
    db = client[db_name]
    collection = db[collection_name]
    
    # Update the document
    query = {"_id" : content_id}
    result = collection.replace_one(query, input_data_dict)