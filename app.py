import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# You will get these tokens for free from developers.facebook.com
VERIFY_TOKEN = "your_secure_local_verify_token"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

# A hardcoded dictionary for the MVP so you don't even need a database to test it
PRODUCT_DATABASE = {
    "drunkelephant": {
        "name": "Drunk Elephant Protini Cream",
        "dupe": "The Ordinary Natural Moisturizing Factors",
        "link": "https://amzn.to/3YourAffiliateLink1" # Replace with creator's link
    },
    "soldejaneiro": {
        "name": "Sol de Janeiro Cheirosa 68",
        "dupe": "In The Stars by Bath & Body Works",
        "link": "https://amzn.to/3YourAffiliateLink2"
    }
}

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Handles the initial authentication handshake when connecting to Meta Dev Console"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def handle_instagram_events():
    """Listens to live comments on the influencer's account"""
    data = request.json
    
    # Check if the incoming event is a comment update
    if data.get('object') == 'instagram':
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'comments':
                    comment_data = change.get('value', {})
                    comment_text = comment_data.get('text', '').lower()
                    sender_id = comment_data.get('from', {}).get('id')
                    comment_id = comment_data.get('id')
                    
                    # Keywords to scan for
                    trigger_words = ["dupe", "link", "cheap", "alternative", "where to buy"]
                    if any(word in comment_text for word in trigger_words):
                        process_automation(sender_id, comment_text, comment_id)
                        
    return jsonify({"status": "success"}), 200

def process_automation(recipient_id, text, comment_id):
    """Determines what product is referenced and fires the auto-DM"""
    matched_link = None
    matched_dupe = None
    
    # Simple search string match to find which product to deliver
    for key, item in PRODUCT_DATABASE.items():
        if key in text:
            matched_link = item['link']
            matched_dupe = item['dupe']
            break
            
    # Default fallback if they just typed "link please" without a specific product name
    if not matched_link:
        matched_dupe = "our curated drugstore alternative list"
        matched_link = "https://amzn.to/GeneralListLink"

    # Construct the payload using Meta's official Graph API schema
    url = f"https://graph.instagram.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": f"Hey there! Thanks for your comment. You can find the chemical dupe ({matched_dupe}) right here: {matched_link}"
        }
    }
    
    # Send the automated Direct Message securely
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Successfully automated a DM to user {recipient_id}")
    except Exception as e:
        print(f"Error handling automated trigger: {str(e)}")

if __name__ == '__main__':
    app.run(port=5000)