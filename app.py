
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_sql", methods=["POST"])
def generate_sql():
    raw_data = request.json.get("raw_data", "")
    prompt = f"""
You are an expert SQL developer.
Given the following raw CSV-like data (first row = column names), generate:
1. A CREATE TABLE statement with correct SQL data types.
2. INSERT INTO statements for all rows.
Use the table name 'my_table'.
Return only the SQL code.

Data:
{raw_data}
"""
    try:
        response = model.generate_content(prompt)
        return jsonify({"sql": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
