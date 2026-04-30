from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

PSPCL_TOKEN = os.getenv("PSPCL_TOKEN")

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def proxy_request():
    print("--- [GET /] HIT ---")
    url = "https://distribution.pspcl.in/returns/module.php?to=Consumers.getDistricts&lang=en"
    print(f"[GET /] Sending request to: {url}")
    try:
        resp = requests.get(url, timeout=10)
        print(f"[GET /] Response status: {resp.status_code}")
        print(f"[GET /] Response text (first 300 chars): {resp.text[:300]}")
        data = resp.json()
        print(f"[GET /] Parsed JSON successfully, returning {len(data)} items")
    except requests.exceptions.Timeout:
        print("[GET /] ERROR: Request timed out")
        return jsonify({"error": "Upstream request timed out"}), 504
    except requests.exceptions.RequestException as e:
        print(f"[GET /] ERROR: Request failed: {e}")
        return jsonify({"error": str(e)}), 502
    except ValueError:
        print(f"[GET /] Could not parse JSON, returning raw text")
        data = {"response": resp.text}
    return jsonify(data)


@app.route('/divisions', methods=['GET'])
def get_divisions():
    district_id = request.args.get('id')
    print(f"--- [GET /divisions] HIT --- id={district_id}")
    if not district_id:
        print("[GET /divisions] ERROR: Missing district id")
        return jsonify({"error": "Missing district id"}), 400
    url = f"https://distribution.pspcl.in/returns/module.php?to=Consumers.getDivisions&id={district_id}"
    print(f"[GET /divisions] Sending request to: {url}")
    try:
        resp = requests.get(url, timeout=10)
        print(f"[GET /divisions] Response status: {resp.status_code}")
        print(f"[GET /divisions] Response text (first 300 chars): {resp.text[:300]}")
        data = resp.json()
        print(f"[GET /divisions] Parsed JSON successfully, returning {len(data)} items")
    except requests.exceptions.Timeout:
        print("[GET /divisions] ERROR: Request timed out")
        return jsonify({"error": "Upstream request timed out"}), 504
    except requests.exceptions.RequestException as e:
        print(f"[GET /divisions] ERROR: Request failed: {e}")
        return jsonify({"error": str(e)}), 502
    except ValueError:
        print(f"[GET /divisions] Could not parse JSON, returning raw text")
        data = {"response": resp.text}
    return jsonify(data)


@app.route('/subdivisions', methods=['GET'])
def get_subdivisions():
    division_id = request.args.get('id')
    print(f"--- [GET /subdivisions] HIT --- id={division_id}")
    if not division_id:
        print("[GET /subdivisions] ERROR: Missing division id")
        return jsonify({"error": "Missing district id"}), 400
    url = f"https://distribution.pspcl.in/returns/module.php?to=Consumers.getSubDivisions&id={division_id}"
    print(f"[GET /subdivisions] Sending request to: {url}")
    try:
        resp = requests.get(url, timeout=10)
        print(f"[GET /subdivisions] Response status: {resp.status_code}")
        print(f"[GET /subdivisions] Response text (first 300 chars): {resp.text[:300]}")
        data = resp.json()
        print(f"[GET /subdivisions] Parsed JSON successfully, returning {len(data)} items")
    except requests.exceptions.Timeout:
        print("[GET /subdivisions] ERROR: Request timed out")
        return jsonify({"error": "Upstream request timed out"}), 504
    except requests.exceptions.RequestException as e:
        print(f"[GET /subdivisions] ERROR: Request failed: {e}")
        return jsonify({"error": str(e)}), 502
    except ValueError:
        print(f"[GET /subdivisions] Could not parse JSON, returning raw text")
        data = {"response": resp.text}
    return jsonify(data)


@app.route('/check_supply', methods=['GET'])
def get_supply_status():
    subdivision_id = request.args.get('id')
    print(f"--- [GET /check_supply] HIT --- id={subdivision_id}")
    if not subdivision_id:
        print("[GET /check_supply] ERROR: Missing subdivision id")
        return jsonify({"error": "Missing district id"}), 400
    url = f"https://distribution.pspcl.in/returns/module.php?to=NCC.apiGetOfflineFeedersinSD&token={PSPCL_TOKEN}&sdid={subdivision_id}"
    print(f"[GET /check_supply] Sending request to: {url}")
    try:
        resp = requests.get(url, timeout=10)
        print(f"[GET /check_supply] Response status: {resp.status_code}")
        print(f"[GET /check_supply] Response text (first 300 chars): {resp.text[:300]}")
        data = str(resp.text).split('(')[1].split(')')[0]
        print(f"[GET /check_supply] Parsed supply data successfully")
    except IndexError:
        print(f"[GET /check_supply] ERROR: Could not parse response — unexpected format. Full text: {resp.text[:500]}")
        return jsonify({"error": "Unexpected response format from upstream"}), 502
    except requests.exceptions.Timeout:
        print("[GET /check_supply] ERROR: Request timed out")
        return jsonify({"error": "Upstream request timed out"}), 504
    except requests.exceptions.RequestException as e:
        print(f"[GET /check_supply] ERROR: Request failed: {e}")
        return jsonify({"error": str(e)}), 502
    return jsonify(data)

@app.route('/raw', methods=['GET'])
def raw_check_supply():
    subdivision_id = request.args.get('id')
    if not subdivision_id:
        return "Missing subdivision id", 400
    url = f"https://distribution.pspcl.in/returns/module.php?to=NCC.apiGetOfflineFeedersinSD&token={PSPCL_TOKEN}&sdid={subdivision_id}"
    try:
        resp = requests.get(url, timeout=10)
        return resp.text, resp.status_code
    except requests.exceptions.RequestException as e:
        return str(e), 502

if __name__ == '__main__':
    app.run()