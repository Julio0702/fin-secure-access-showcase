import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

# --- WAF (WEB APPLICATION FIREWALL) ---
import re

WAF_RULES = {
    'SQL_INJECTION': [
        r"(?i)\bUNION\b.*\bSELECT\b", 
        r"(?i)\b(OR|AND)\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?", 
        r"(?i)\bDROP\s+TABLE\b", 
        r"(?i)--"
    ],
    'XSS': [
        r"(?i)<script.*?>", 
        r"(?i)javascript:", 
        r"(?i)onerror=", 
        r"(?i)onload="
    ]
}

@app.before_request
def waf_middleware():
    """
    Mini-WAF to intercept and inspect all incoming requests for malicious payloads.
    """
    # 1. Helper Function to scan a string
    def scan_payload(value, source):
        if not isinstance(value, str): 
            value = str(value)
        for threat_type, patterns in WAF_RULES.items():
            for pattern in patterns:
                if re.search(pattern, value):
                    print(f"!!! WAF BLOCKED: {threat_type} detected in {source} (Payload: {value}) !!!")
                    return threat_type
        return None

    try:
        # 2. Inspect Query Parameters
        for key, val in request.args.items():
            threat = scan_payload(val, f"Query Param '{key}'")
            if threat: 
                msg = "Security Warning: Your input contains blocked characters (e.g., ' or --). Please remove them." if threat == 'SQL_INJECTION' else "Security Warning: Invalid script tags detected."
                return jsonify({"status": "blocked", "message": msg, "threat": threat}), 403

        # 3. Inspect JSON Body
        if request.is_json and request.get_json(silent=True):
            data = request.get_json(silent=True)
            for key, val in data.items():
                threat = scan_payload(val, f"Body Field '{key}'")
                if threat:
                     msg = "Security Warning: Your input contains blocked characters (e.g., ' or --). Please remove them." if threat == 'SQL_INJECTION' else "Security Warning: Invalid script tags detected."
                     return jsonify({"status": "blocked", "message": msg, "threat": threat}), 403

        # 4. Inspect Headers (Simple Bot Protection)
        ua = request.headers.get('User-Agent', '').lower()
        if 'curl' in ua or 'python-requests' in ua:
             return jsonify({"status": "blocked", "message": "Security Warning: Automated access is not allowed."}), 403

    except Exception as e:
        print(f"WAF Error: {e}")
        # Fail safe: In production, might block. Here, we log and proceed to avoid breaking valid traffic on error.
        pass 

# --- SECURITY: VELOCITY TRACKER ---
last_action_time = {}

# --- LOAD MODELS ---
try:
    model_creditcard = joblib.load('model_creditcard.joblib')
    print("Model A (Credit Card Expert) loaded.")
except:
    model_creditcard = None

try:
    model_paysim = joblib.load('model_paysim.joblib')
    print("Model B (PaySim Expert) loaded.")
except:
    model_paysim = None

try:
    paysim_scaler = joblib.load('paysim_scaler.joblib')
    print("PaySim Scaler loaded.")
except:
    paysim_scaler = None

# --- FEATURE LISTS (FIXED ORDER) ---
# CRITICAL FIX: The order must match the training notebook exactly (Scaled_Amount, Scaled_Time, Hour)
FEATURES_CREDITCARD = [
    'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
    'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
    'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 
    'Scaled_Amount', 'Scaled_Time', 'Hour' 
]

FEATURES_PAYSIM = [
    'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest',
    'amount_gt_oldbalanceOrg', 'newbalanceOrig_is_zero', 'oldbalanceDest_is_zero',
    'type_CASH_IN', 'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER'
]

NUMERICAL_FEATURES_PAYSIM = [
    'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'
]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data: return jsonify({'error': 'No data'}), 400

    user_id = data.get('userID', 'anonymous')
    transaction_type = data.get('transactionType')
    amount = float(data.get('amount', 0))
    current_time = time.time()
    
    # Velocity Check
    if user_id in last_action_time:
        if current_time - last_action_time[user_id] < 1:
            return jsonify({
                'prediction': 'Fraudulent', 
                'confidence': 1.0, 
                'model_used': 'Security Gateway: Velocity Check',
                'error': 'Action too frequent. Please wait 1 second.'
            }), 429
    last_action_time[user_id] = current_time

    try:
        # Rule Engine
        if 9000 <= amount < 10000:
             return jsonify({'prediction': 'Fraudulent', 'confidence': 0.85, 'model_used': 'Rule-Engine (Structuring Detect)'})

        if amount > 50000:
             return jsonify({'prediction': 'Fraudulent', 'confidence': 0.99, 'model_used': 'Rule-Engine (High Value)'})

        # AI Engine
        prediction = [0]
        confidence = 0.0
        model_used = "Simulated AI"

        if transaction_type == 'credit_card':
            if model_creditcard:
                # Create DataFrame with correct columns
                sim_data = np.random.rand(1, len(FEATURES_CREDITCARD))
                df = pd.DataFrame(sim_data, columns=FEATURES_CREDITCARD)
                
                # Demo fraud simulation logic
                if amount > 15000: 
                    df['V14'] = -5.0
                    df['V12'] = -5.0

                df['Scaled_Amount'] = (amount - 100) / 250
                df['Hour'] = pd.Timestamp.now().hour
                
                # Ensure column order matches training exactly
                df = df[FEATURES_CREDITCARD]
                
                prediction = model_creditcard.predict(df)
                confidence = model_creditcard.predict_proba(df)[0][prediction[0]]
                model_used = "AI: Credit Card Expert"
            else:
                 prediction = [1] if amount > 15000 else [0]
                 confidence = 0.92
                 model_used = "Simulation (Model Missing)"

        elif transaction_type == 'p2p_transfer':
            if model_paysim and paysim_scaler:
                 old_bal = 50000
                 data_dict = {
                    'amount': amount, 'oldbalanceOrg': old_bal, 'newbalanceOrig': max(0, old_bal - amount),
                    'oldbalanceDest': 0, 'newbalanceDest': 0,
                    'amount_gt_oldbalanceOrg': int(amount > old_bal), 
                    'newbalanceOrig_is_zero': int(amount >= old_bal),
                    'oldbalanceDest_is_zero': 1,
                    'type_CASH_IN': 0, 'type_CASH_OUT': 0, 'type_DEBIT': 0, 'type_PAYMENT': 0, 'type_TRANSFER': 1
                 }
                 df = pd.DataFrame([data_dict], columns=FEATURES_PAYSIM)
                 df[NUMERICAL_FEATURES_PAYSIM] = paysim_scaler.transform(df[NUMERICAL_FEATURES_PAYSIM])
                 
                 prediction = model_paysim.predict(df)
                 confidence = model_paysim.predict_proba(df)[0][prediction[0]]
                 model_used = "AI: P2P Expert"
            else:
                 prediction = [1] if amount > 20000 else [0]
                 confidence = 0.95
                 model_used = "Simulation (Model Missing)"

        return jsonify({
            'prediction': 'Fraudulent' if prediction[0] else 'Legitimate',
            'confidence': float(confidence),
            'model_used': model_used
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return send_from_directory('.', 'live_fraud_detection_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)