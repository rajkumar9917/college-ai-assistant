import json
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import CollegeInfo, Message
from groq import Groq


# ✅ Groq Client Safe Init
client = Groq(api_key=settings.GROQ_API_KEY)


# 🔹 Chat Page
def chat_page(request):
    return render(request, "chat/chatbot.html")


# 🔥 Text Cleaning Function (important upgrade)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


# 🤖 SMART DB MATCHING (UPGRADED)
def find_best_match(user_message):
    user_message = clean_text(user_message)
    user_words = set(user_message.split())

    best_match = None
    best_score = 0

    for item in CollegeInfo.objects.all():
        db_question = clean_text(item.question)
        db_words = set(db_question.split())

        # ✅ Exact match boost
        if user_message == db_question:
            return item, 100

        # 🔥 Common words score
        score = len(user_words & db_words)

        # 🔥 Partial matching (powerful)
        for word in user_words:
            for db_word in db_words:
                if word in db_word or db_word in word:
                    score += 0.5

        # 🔥 Length normalization (smart)
        if len(db_words) > 0:
            score = score / len(db_words)

        if score > best_score:
            best_score = score
            best_match = item

    return best_match, best_score


# 🔹 Chat API
@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."})

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"reply": "Please enter a message."})

        # ✅ Save user message
        Message.objects.create(text=user_message, is_user=True)

        # ============================
        # 🔥 1️⃣ DATABASE SEARCH
        # ============================
        best_match, best_score = find_best_match(user_message)

        # 🎯 Smart threshold
        if best_match and best_score >= 0.3:
            ai_reply = best_match.answer

        else:
            # ============================
            # 🤖 2️⃣ GROQ AI (FULL POWER)
            # ============================
            try:
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a smart AI assistant.

You help students with:
- college
- admissions
- exams
- results
- courses
- general knowledge

Give clear, short and helpful answers.
If question is general, still answer it normally."""
                        },
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                    temperature=0.7,
                    max_tokens=500
                )

                ai_reply = response.choices[0].message.content.strip()

            except Exception as e:
                            print("GROQ ERROR:", e)
                            ai_reply = f"AI Error: {str(e)}"

        # ============================
        # ✅ Save AI response
        # ============================
        Message.objects.create(text=ai_reply, is_user=False)

        return JsonResponse({"reply": ai_reply})

    except Exception:
        return JsonResponse({"reply": "Server error. Please try again."})


# 🤖 SMART OFFLINE FALLBACK
def smart_fallback(message):
    message = message.lower()

    fallback = {
        "hod": "HOD information is available in the department office.",
        "admission": "Admissions usually start in July.",
        "fees": "Fee details are available at the accounts office.",
        "courses": "We offer BCA, BBA, BA, BSc and more.",
        "exam": "Exam schedules are released on the official website.",
        "result": "Results are available on the university portal.",
        "college": "This college provides quality education and facilities.",
    }

    for key in fallback:
        if key in message:
            return fallback[key]

    return "I’m not sure, but you can contact the college office for help."