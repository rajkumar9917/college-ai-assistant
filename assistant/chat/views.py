import json
import re

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import CollegeInfo, Message
from groq import Groq


client = Groq(api_key=settings.GROQ_API_KEY)


def chat_page(request):
    return render(request, "chat/chatbot.html")


# ==========================
# CLEAN USER TEXT
# ==========================

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()


# ==========================
# BETTER DATABASE SEARCH
# ==========================

def find_best_match(user_message):

    user_message = clean_text(user_message)

    if not user_message:
        return None,0

    best_match = None
    best_score = 0

    for item in CollegeInfo.objects.all():

        db_question = clean_text(item.question)

        # exact match
        if user_message == db_question:
            return item,100

        user_words = set(user_message.split())
        db_words = set(db_question.split())

        common = user_words.intersection(db_words)

        # minimum 2 same words
        if len(common) < 2:
            continue

        score = len(common)/max(
            len(user_words),
            len(db_words)
        )

        if score > best_score:
            best_score=score
            best_match=item

    return best_match,best_score


# ==========================
# SMALL CHAT
# ==========================

def small_talk(message):

    msg=message.lower()

    replies={

        "hello":"Hello! Kaise help kar sakta hu?",
        "hi":"Hi! Pucho jo puchna hai.",
        "hey":"Hey!",
        "thanks":"You're welcome.",
        "thank you":"Welcome.",
        "good morning":"Good Morning",
        "good night":"Good Night",
        "bye":"Bye, have a great day."
    }

    for key,val in replies.items():

        if key in msg:
            return val

    return None


# ==========================
# FALLBACK
# ==========================

def smart_fallback(message):

    message=message.lower()

    fallback={

        "hod":"Department office se HOD details mil jayengi.",

        "admission":"Admissions usually July me start hote hain.",

        "fees":"Fee details accounts office me available hain.",

        "exam":"Exam schedule official website par upload hota hai.",

        "result":"Results DBRAU portal par available hote hain.",

        "college":"Agra College 1823 me established hua tha.",

        "scholarship":"Scholarship forms administration block me verify hote hain."
    }

    for key,val in fallback.items():

        if key in message:
            return val

    return "Official information not available. Contact college administration."


# ==========================
# API
# ==========================

@csrf_exempt
def chat_api(request):

    if request.method!="POST":

        return JsonResponse(
            {"reply":"Invalid request"}
        )


    try:

        data=json.loads(request.body)

        user_message=data.get(
            "message",""
        ).strip()


        if not user_message:

            return JsonResponse(
                {"reply":"Enter message"}
            )


        Message.objects.create(
            text=user_message,
            is_user=True
        )


        # small chat first

        chat_reply=small_talk(
            user_message
        )

        if chat_reply:

            Message.objects.create(
                text=chat_reply,
                is_user=False
            )

            return JsonResponse(
                {"reply":chat_reply}
            )


        # database search

        best_match,best_score=\
            find_best_match(
            user_message
        )


        if best_match and best_score>=0.75:

            ai_reply=best_match.answer


        else:

            try:

                system_prompt="""

You are official AI Assistant of Agra College.

Rules:

Reply in user's language.

Answer short.

Do not repeat question.

You know:

Agra College
DBRAU
Agra City
India GK
Basic Education
Courses
Admissions
Results
Scholarships

Examples:

Who is PM of India?
Narendra Modi.

Who is CM of UP?
Yogi Adityanath.

Agra College established?
1823.

DBRAU established?
1927.

Taj Mahal kaha hai?
Agra Uttar Pradesh.

Unknown:
Official information not available.

"""

                response=client.chat.completions.create(

                    model="llama-3.1-8b-instant",

                    messages=[

                        {
                            "role":"system",
                            "content":system_prompt
                        },

                        {
                            "role":"user",
                            "content":user_message
                        }

                    ],

                    temperature=.3,

                    max_tokens=300

                )


                ai_reply=response.choices[
                    0
                ].message.content.strip()


            except Exception as e:

                print(
                    "GROQ ERROR:",
                    e
                )

                ai_reply=smart_fallback(
                    user_message
                )


        Message.objects.create(
            text=ai_reply,
            is_user=False
        )


        return JsonResponse(
            {"reply":ai_reply}
        )


    except Exception as e:

        print(
            "SERVER ERROR:",
            e
        )

        return JsonResponse(
            {
                "reply":"Server Error. Please try again."
            }
        )