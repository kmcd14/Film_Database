# MongoDB queries

import pymongo

myclient = None

def connect(): # Connect to mongoDB demon
    global myclient
    myclient = pymongo.MongoClient()
    myclient.admin.command('ismaster')
   


# Choice 5 - View moive with subtitles
# Query to create an index and search for films with the language entered by the user
def find(sub_language):
    if (not myclient):
        try:
            connect()
        except Exception as e:
            print('Error could not connect -', e)

   
    db = myclient['movieScriptsDB']
    collection = db['movieScripts']
    collection.create_index('subtitles' ) # Creating an index on subtitles
    results = list(collection.find({'$text':{'$search' : sub_language} })) # turning a text search of the reults into a list, without Mongo was only returning one film to main programme
    return results   
     


# Choice 6 - Add new movie script
# Query to add new script to the collection based on user input
def new_script(scripts):
    if (not myclient):
        try:
            connect()
        except Exception as e:
            print('Error could not connect -', e)

    
    db = myclient['movieScriptsDB']
    try:
        cols = db.get_collection('movieScripts')
        cols.insert_one(scripts)  # Try to insert from values from the dict scripts in main programme
    except pymongo.errors.DuplicateKeyError as e:  
        print('***Error*** Movie script with id {} already exists'.format( scripts['_id'])) # Already exists  
   



    