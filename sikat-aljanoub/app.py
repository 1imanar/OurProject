from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
import time

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini_with_retry(prompt, retries=3, delay=3):
    last_error = None

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response

        except Exception as e:
            last_error = e

            error_text = str(e)

            # إذا كان الخطأ مؤقت مثل 503، يعيد المحاولة
            if "503" in error_text or "UNAVAILABLE" in error_text:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue

            # أي خطأ ثاني يوقف مباشرة
            raise e

    raise last_error


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "اكتبي سؤالك أول."}), 400

        system_prompt = """
أنت مرشد سياحي ذكي لموقع اسمه سكة الجنوب.
مهمتك تساعد المستخدم في السياحة في جنوب السعودية.
ركز على:
- عسير
- جازان
- نجران
- الباحة

خلك واضح ومرتب وبالعربي.
"""

        full_prompt = f"{system_prompt}\n\nسؤال المستخدم: {user_message}"

        response = ask_gemini_with_retry(full_prompt)

        return jsonify({"reply": response.text})

    except Exception as e:
        error_text = str(e)

        if "503" in error_text or "UNAVAILABLE" in error_text:
            return jsonify({
                "reply": "الخدمة عليها ضغط الآن، جربي بعد شوي."
            }), 500

        return jsonify({
            "reply": f"صار خطأ: {error_text}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)