from flask import Flask, request, jsonify
from flask_cors import CORS
import oracledb

app = Flask(__name__)
CORS(app)

dsn = "db.freesql.com:1521/23ai_mb9q7"
DB_USER = "SQL_IVNYV40WHRFD2EJHK5UGR3EYK0"
DB_PASSWORD = "4N7A2#28R2Ui0HJXOQXMZJXMVF4L94"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("message", "").strip().lower()

        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=dsn
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT PLACE_NAME, DESCRIPTION
            FROM PLACES
            WHERE LOWER(PLACE_NAME) LIKE :q
               OR LOWER(DESCRIPTION) LIKE :q
            FETCH FIRST 5 ROWS ONLY
        """, q=f"%{question}%")

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        if rows:
            reply = "وجدت لك هذه الأماكن:\n\n"

            for row in rows:
                try:
                    desc = str(row[1]) if row[1] else ""
                except:
                    desc = ""

                reply += f"• {row[0]} - {desc}\n"

        else:
            reply = """لم أجد نتيجة مطابقة 🌿

جرّب البحث عن:
• أبها
• جازان
• نجران
• الباحة
• منتزه
• مطعم
• كافيه
"""

        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "reply": "حصلت مشكلة بسيطة 🌿 جرّب مرة ثانية أو ابحث باسم منطقة مثل أبها أو جازان."
        })

if __name__ == "__main__":
    app.run(debug=True)