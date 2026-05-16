from pymongo import MongoClient

client = MongoClient("mongodb+srv://sivagnanamcm2006:sivagnanam@trackterms.ohrscao.mongodb.net/?appName=TrackTerms/")

db = client["trackterms"]

collection = db["documents"]