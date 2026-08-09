from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/api/verify-upi', methods=['GET', 'POST'])
def verify_upi():
    try:
        if request.method == 'GET':
            upi_id = request.args.get('upi')
        else:
            data = request.get_json()
            upi_id = data.get('upi') if data else None
        
        if not upi_id:
            return jsonify({
                "error": "UPI ID required",
                "developer": "@Oriss01",
                "credit": "Digittalphantom",
                "message": "Please provide 'upi' parameter"
            }), 400

        url = "https://www.amazon.in/apay/money-transfer/verify-vpa/v2"
        
        payload = {
            "recipientVpa": upi_id,
            "clientContext": {
                "pageType": "EAP",
                "useCase": "SEND_MONEY"
            }
        }

        headers = {
            'User-Agent': "Amazon.com/30.22.0.300 (Android/15/V2509)",
            'Accept': "application/json; charset=utf-8",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua': "\"Not:A-Brand\";v=\"99\", \"Android WebView\";v=\"145\", \"Chromium\";v=\"145\"",
            'sec-ch-ua-mobile': "?1",
            'content-type': "application/json; charset=utf-8",
            'origin': "https://www.amazon.in",
            'x-requested-with': "in.amazon.mShop.android.shopping",
            'referer': "https://www.amazon.in/apay/money-transfer/assets/ap4-eap/index.html",
            'accept-language': "en-IN,en-US;q=0.9,en;q=0.8",
            'Cookie': os.getenv('AMAZON_COOKIE', '')
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        try:
            result = response.json()
        except:
            result = {"raw_response": response.text}
        
        result["developer"] = "@Oriss01"
        result["credit"] = "Digittalphantom"
        result["api_source"] = "Amazon Pay UPI Verification"
        
        return jsonify(result), response.status_code
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "developer": "@Oriss01",
            "credit": "Digittalphantom"
        }), 500

@app.route('/')
def home():
    return jsonify({
        "message": "UPI Verification API",
        "developer": "@Oriss01",
        "credit": "Digittalphantom",
        "usage": "GET /api/verify-upi?upi=YOUR_UPI_ID",
        "example": "/api/verify-upi?upi=9313111694@axl"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
