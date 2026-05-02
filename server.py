import time
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load our recommendation engine pipeline
from src.pipeline import Pipeline

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing to allow React (port 5173/5174) to communicate with Flask (port 5000)
CORS(app)

print("Initializing BIS Recommendation Engine. Loading dependencies...")
pipe = Pipeline()
print("Pipeline engine loaded and ready!")

@app.route('/search', methods=['POST'])
def search_standards():
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' field in JSON body"}), 400

        query = data['query'].strip()
        if not query:
             return jsonify({"error": "Query cannot be empty"}), 400

        print(f"\nReceived search request: '{query}'")
        
        start_time = time.time()
        
        # Execute recommendation engine logic
        ranked_codes = pipe.run(query)
        
        latency = time.time() - start_time
        print(f"Found {len(ranked_codes)} standards in {latency:.4f}s")
        
        response = {
            "retrieved_standards": ranked_codes,
            "latency_seconds": latency
        }
        
        return jsonify(response), 200

    except Exception as e:
        print(f"Error handling request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error connecting to the engine."}), 500


if __name__ == '__main__':
    # Force Flask to run precisely on port 5000 which the front-end requests.
    print("Starting Flask server on http://localhost:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
