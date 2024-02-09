from pymongo import MongoClient


def get_database(file_path, an):
   

 
   # Open the file in read mode
   with open(file_path, 'r') as file:
      # Read the entire content of the file
      file_content = file.read()

   
      # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
      client = MongoClient(file_content)
      
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[an]

