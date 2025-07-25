from flask import Flask, request, jsonify
import requests, fitz, io

app = Flask(__name__)

@app.route("/", methods=["POST"])
def parse_pdf():
    data = request.get_json()
    file_url = data.get("url")
    if not file_url:
        return jsonify({"error": "Missing 'url'"}), 400

    resp = requests.get(file_url)
    if resp.status_code != 200:
        return jsonify({"error": "Failed download"}), 502

    doc = fitz.open(stream=io.BytesIO(resp.content), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    doc.close()

    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
