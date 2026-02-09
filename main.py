from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def two_sum(nums, target):
    """
    Find two indices where nums[i] + nums[j] = target
    Using hash map for O(n) time complexity
    """
    seen = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in seen:
            return [seen[complement], i]
        seen[nums[i]] = i
    return []

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Two Sum API",
        "endpoint": "/two-sum",
        "method": "POST",
        "example": {
            "request": {
                "nums": [2, 7, 11, 15],
                "target": 9
            },
            "response": {
                "indices": [0, 1]
            }
        }
    })

@app.route('/two-sum', methods=['POST'])
def two_sum_endpoint():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'nums' not in data:
            return jsonify({"error": "Missing 'nums' field"}), 400
        
        if 'target' not in data:
            return jsonify({"error": "Missing 'target' field"}), 400
        
        nums = data['nums']
        target = data['target']
        
        # Validate inputs
        if not isinstance(nums, list):
            return jsonify({"error": "'nums' must be an array"}), 400
        
        if len(nums) < 2:
            return jsonify({"error": "'nums' must have at least 2 elements"}), 400
        
        if len(nums) > 10000:
            return jsonify({"error": "'nums' length exceeds maximum of 10^4"}), 400
        
        if not isinstance(target, (int, float)):
            return jsonify({"error": "'target' must be a number"}), 400
        
        # Find indices
        indices = two_sum(nums, target)
        
        if not indices:
            return jsonify({"error": "No solution found"}), 404
        
        return jsonify({"indices": indices}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)