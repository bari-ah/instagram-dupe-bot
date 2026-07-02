import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. The main Home Route (Fixes 404 if TikTok tests the base domain)
@app.route('/', methods=['GET', 'POST'])
def home():
    return "DupeBot Backend is running successfully!", 200

# 2. Your TikTok Verification File Route
@app.route('/tiktokKDLcbFzR3QjRYcYdQIigJOB2Fgiz4WSm.txt', methods=['GET'])
def verify_tiktok_domain():
    return "tiktok-developers-site-verification=KDLcbFzR3QjRYcYdQIigJOB2Fgiz4WSm", 200

# 3. The Live Webhook Data Route
@app.route('/tiktok-webhook', methods=['GET', 'POST'])
def handle_tiktok_events():
    # If TikTok sends a verification ping, reply with success
    if request.method == 'GET':
        return "Webhook Endpoint Active", 200
        
    data = request.json
    print("Received webhook event:", data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)