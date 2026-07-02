import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple data lookup for your MVP
PRODUCT_DATABASE = {
    "drunkelephant": {
        "name": "Drunk Elephant Protini Cream",
        "dupe": "The Ordinary Natural Moisturizing Factors",
        "link": "https://amzn.to/3YourAffiliateLink1"
    },
    "soldejaneiro": {
        "name": "Sol de Janeiro Cheirosa 68",
        "dupe": "In The Stars by Bath & Body Works",
        "link": "https://amzn.to/3YourAffiliateLink2"
    }
}

@app.route('/tiktok-webhook', methods=['POST'])
def handle_tiktok_events():
    """Listens for live comments on your TikTok videos"""
    data = request.json
    
    # Verify this is a comment event from TikTok
    if data and data.get('event') == 'video.comment.create':
        content = data.get('content', {})
        comment_text = content.get('text', '').lower()
        user_openid = content.get('user_openid') # Unique identifier of the commenter
        
        # Keywords to scan for
        trigger_words = ["dupe", "link", "cheap", "alternative"]
        if any(word in comment_text for word in trigger_words):
            
            # Find matching dupe
            matched_link = "https://amzn.to/GeneralListLink"
            matched_dupe = "our budget alternative list"
            
            for key, item in PRODUCT_DATABASE.items():
                if key in comment_text:
                    matched_link = item['link']
                    matched_dupe = item['dupe']
                    break
            
            print(f"Trigger found! Sending link {matched_link} to TikTok user {user_openid}")
            # Here your code will call TikTok's send message API using their direct tokens
            
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)