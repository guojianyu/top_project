from bson.objectid import ObjectId
import db_oprate
obj = db_oprate.collection_db()
a = obj.find_data(obj.tb,{},1)
for i in a:
    _id = i["_id"]
    _id = str(_id)
    print (type(_id))
    break

_id = ObjectId(_id)
a = obj.find_data(obj.tb,{"_id":_id},1)
for i in a:
    print (i)
