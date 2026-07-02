import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. The main Home Route
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
    if request.method == 'GET':
        return "Webhook Endpoint Active", 200
        
    data = request.json
    print("Received webhook event:", data)
    return jsonify({"status": "success"}), 200

# 4. Terms of Service Page (With TikTok Verification)
@app.route('/terms', methods=['GET'])
def terms_of_service():
    return """
    <html>
    <head>
        <title>Terms of Service</title>
        <!-- tiktok-developers-site-verification=KDLcbFzR3QjRYcYdQIigJOB2Fgiz4WSm -->
    </head>
    <body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
        <p style="color: #ccc; font-size: 10px;">tiktok-developers-site-verification=KDLcbFzR3QjRYcYdQIigJOB2Fgiz4WSm</p>
        <h1>Terms of Service</h1>
        <p>Welcome to DupeBot Backend. By interacting with our automated TikTok service, you agree to these basic terms.</p>
        <h3>1. Service Description</h3>
        <p>Our application automatically provides budget-friendly beauty and skincare alternative recommendations ("dupes") when triggered by user comments on our designated social media content.</p>
        <h3>2. Automated Messaging</h3>
        <p>By leaving a request comment, you acknowledge that our system will automatically transmit the requested information or links back to your platform user profile.</p>
        <h3>3. Limitation of Liability</h3>
        <p>We provide product suggestions for information purposes only. We are not liable for external product quality, merchant behavior, or third-party purchases.</p>
    </body>
    </html>
    """, 200

# 5. Privacy Policy Page (With TikTok Verification)
@app.route('/privacy', methods=['GET'])
def privacy_policy():
    return """
    <html>
    <head>
        <title>Privacy Policy</title>
        <!-- tiktok-developers-site-verification=KDLcbFzR3QjRYcYdQIigJOB2Fgiz4WSm -->
    </head>
    <body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
        <p style="color: #ccc; font-size: 10px;">tiktok-developers-site-verification=KDLcbFzR3QjRYcYdQIigJOB2Fgiz4WSm</p>
        <h1>Privacy Policy</h1>
        <p>Your privacy is important to us. This policy details how our automated service interacts with user data.</p>
        <h3>1. Data We Receive</h3>
        <p>When you comment on our videos, our application receives public webhook data from TikTok containing the comment text, timestamp, and your public platform user identifier.</p>
        <h3>2. How We Use Data</h3>
        <p>We use this incoming event data strictly to process your product request and return the relevant product link. We do not build user profiles or harvest personal tracking details.</p>
        <h3>3. Data Sharing & Retention</h3>
        <p>We do not sell, rent, or trade user comment information with third parties. Data payloads are stored temporarily only to ensure server delivery success and are automatically dropped.</p>
    </body>
    </html>
    """, 200

if __name__ == '__main__':
    app.run(port=5000)