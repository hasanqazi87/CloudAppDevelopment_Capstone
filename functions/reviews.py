from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request
import atexit

#Add your Cloudant service credentials here
cloudant_username = 'd65e5e43-83be-4e04-bf34-e149095716c3-bluemix'
cloudant_api_key = 'Fjv8WWZ6EdoU-NUry203SFlRsHxmZiP8GbQ66ivXdXd1'
cloudant_url = 'https://d65e5e43-83be-4e04-bf34-e149095716c3-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()
print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/review', methods=['GET'])
def get_reviews():
    dealership_id = request.args.get('dealerId')

    # Check if "id" parameter is missing
    if dealership_id is None:
        return jsonify({"error": "Missing 'dealerId' parameter in the URL"}), 400

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be an integer"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    try:
        result = db.get_query_result(selector)
    except:
        return jsonify({'error': 'Something went wrong on the server.'}), 500
    if not result:
        return jsonify({'error': f'dealer ID {dealership_id} does not exist.'}), 404

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    return jsonify(data_list)


@app.route('/api/review', methods=['POST'])
def post_review():
    if not request.json:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Save the review data as a new document in the Cloudant database
    try:
        db.create_document(review_data)
    except:
        return jsonify({'error': 'Something went wrong on the server.'}), 500

    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
