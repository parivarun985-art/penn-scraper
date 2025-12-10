import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_manufacturer_part(url: str) -> str | None:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    node = soup.find(string=re.compile(r"Manufacturer Part", re.I))
    if not node:
        return None

    text = node.strip()

    if ":" in text:
        return text.split(":", 1)[1].strip()

    m = re.search(r"#\s*([A-Za-z0-9\-]+)", text)
    return m.group(1) if m else None


@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing url"}), 400

    part = get_manufacturer_part(url)
    return jsonify({"url": url, "manufacturer_part": part})
