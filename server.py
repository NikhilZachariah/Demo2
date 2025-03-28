from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# File Path
EXCEL_FILE = "data.xlsx"

# Ensure file exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Age", "Email"])
    df.to_excel(EXCEL_FILE, index=False)

# Route to save user data
@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    df = pd.read_excel(EXCEL_FILE)
    new_data = pd.DataFrame([data])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    return jsonify({"message": "Data saved successfully"}), 200

# Route to fetch user details
@app.route('/search', methods=['GET'])
def search_data():
    name = request.args.get("name", "").strip().lower()
    df = pd.read_excel(EXCEL_FILE)
    person = df[df["Name"].str.lower() == name]
    
    if not person.empty:
        return person.to_json(orient="records"), 200
    return jsonify({"message": "Person not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
