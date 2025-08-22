from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect Flask to MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/telehealth"
mongo = PyMongo(app)

# Routes
@app.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = []
    for appt in mongo.db.appointments.find():
        appointments.append({
            "_id": str(appt["_id"]),
            "patient": appt["patient"],
            "doctor": appt["doctor"],
            "date": appt["date"],
            "time": appt["time"],
            "notes": appt["notes"]
        })
    return jsonify(appointments)

@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    new_appt = {
        "patient": data["patient"],
        "doctor": data["doctor"],
        "date": data["date"],
        "time": data["time"],
        "notes": data.get("notes", "")
    }
    result = mongo.db.appointments.insert_one(new_appt)
    return jsonify({"msg": "Appointment created", "id": str(result.inserted_id)})

@app.route("/appointments/<id>", methods=["DELETE"])
def delete_appointment(id):
    mongo.db.appointments.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
