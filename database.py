from pymongo import MongoClient

client = MongoClient("mongodb+srv://sivagnanamcm2006:sivagnanamcm2006@trackterms.ohrscao.mongodb.net/?appName=TrackTerms/")

db = client["trackterms"]

collection = db["documents"]