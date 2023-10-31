from flask import Flask, jsonify, request

app = Flask(__name__)

sensor_data = [
    {
        "timestamp": "2023-05-28T10:30:00",
        "temperature": 25.5,
        "humidity": 60.2,
        "pressure": 1012.3
    },
    {
        "timestamp": "2023-05-28T10:35:00",
        "temperature": 25.8,
        "humidity": 59.8,
        "pressure": 1012.7
    },
    {
        "timestamp": "2023-05-28T10:40:00",
        "temperature": 26.1,
        "humidity": 59.5,
        "pressure": 1012.9
    }
]


@app.route('/average-temperature', methods=['GET'])
def get_average_temperature():
    total_temp = sum(data['temperature'] for data in sensor_data)
    avg_temp = total_temp / len(sensor_data) if sensor_data else 0
    return jsonify({"average_temperature": avg_temp})


@app.route('/sensor-data', methods=['POST'])
def add_sensor_data():
    # Get the JSON data from the request
    new_data = request.json

    # Validate that all required fields are present
    required_fields = ["timestamp", "temperature", "humidity", "pressure"]
    if not all(field in new_data for field in required_fields):
        return jsonify({"message": "Missing required data in request body"}), 400

    # Append the new data to the sensor_data list
    sensor_data.append(new_data)
    return jsonify(new_data), 201


@app.route('/sensor-data/<timestamp>', methods=['PUT'])
def update_sensor_data(timestamp):
    # Find the index of the entry with the matching timestamp
    index_to_update = next((i for i, entry in enumerate(sensor_data) if entry['timestamp'] == timestamp), None)

    # If not found, return an error message
    if index_to_update is None:
        return jsonify({"message": "No sensor data found for the provided timestamp"}), 404

    # Get the updated data from the request body
    updated_data = request.json

    # Update the sensor data entry at the found index with the new values
    for key in updated_data:
        if key in sensor_data[index_to_update]:
            sensor_data[index_to_update][key] = updated_data[key]

    # Return the updated sensor data entry
    return jsonify(sensor_data[index_to_update]), 200


if __name__ == '__main__':
    app.run(debug=True)