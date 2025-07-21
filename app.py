from flask import Flask, request, jsonify
import sqlite3, datetime

DB = "tickets_scan.db"
app = Flask(__name__)

# CORS for web scanner
@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json(force=True)
    token = data.get('token')

    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT used_flag FROM tickets_scan WHERE token=?", (token,))
        row = c.fetchone()
        if not row:
            return jsonify(ok=False, message="Invalid code"), 404
        if row[0]:
            return jsonify(ok=False, message="Already used"), 409

        now = datetime.datetime.utcnow().isoformat()
        c.execute(
            "UPDATE tickets_scan SET used_flag=1, used_at=? WHERE token=?",
            (now, token)
        )
        conn.commit()

    return jsonify(ok=True, message="Access granted"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
