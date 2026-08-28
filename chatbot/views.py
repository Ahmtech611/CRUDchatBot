from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .forms import LoginForm
from .models import SystemUser
import os
import re
import json
import joblib


# Now first load ML model :

ML_DIR = os.path.join(os.path.dirname(__file__), "Machine_Learning_Logic")

model = joblib.load(os.path.join(ML_DIR, "model.pkl"))
vectorizer = joblib.load(os.path.join(ML_DIR, "vectorizer.pkl"))

CONFIDENCE_THRESHOLD = 0.4


def predict_intent(message):
    vec = vectorizer.transform([message])
    prediction = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    confidence = max(proba)
    
    
    if confidence < CONFIDENCE_THRESHOLD:
        return "unknown", 
    confidence
    return prediction, confidence

email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
phone_pattern = r'\+?\d[\d\s]{7,15}'

def extract_email(text):
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(phone_pattern, text)
    return match.group(0).strip() if match else None

def extract_update_info(text):
    
    # Email-based update :
    email_pattern_update = r"(?:update|change)\s+([\w\.-]+@[\w\.-]+\.\w+)'?s?\s+([\w\s]+?)\s+to\s+(.+)"
    match = re.search(email_pattern_update, text, re.IGNORECASE)
    if match:
        return {"identifier": match.group(1), "type": "email", "field": match.group(2).strip(), "value": match.group(3).strip()}

    # Name-based update and its non greedy :
    
    name_pattern_update = r"(?:update|change)\s+(\w+?)'?s\s+([\w\s]+?)\s+to\s+(.+)"
    match = re.search(name_pattern_update, text, re.IGNORECASE)
    if match:
        return {"identifier": match.group(1), "type": "name", "field": match.group(2).strip(), "value": match.group(3).strip()}

    return None

FIELD_MAP = {
    "phone": "phone",
    "phone number": "phone",
    "city": "city",
    "email": "email",
    "email addres" : "email",
}

def handle_add_user(message):
    email = extract_email(message)
    phone = extract_phone(message)
    name = extract_name(message)

    if not email:
        return "Sorry, I couldn't find an email in your message."
    if not name:
        name = email.split("@")[0]

    if SystemUser.objects.filter(email=email).exists():
        return f"A user with email {email} already exists."

    SystemUser.objects.create(name=name, email=email, phone=phone)
    return f"User {name} ({email}) added successfully."


def handle_remove_user(message):
    email = extract_email(message)
    if not email:
        return "Sorry, I couldn't find an email to remove."

    deleted, _ = SystemUser.objects.filter(email=email).delete()
    if deleted:
        return f"User {email} removed successfully."
    return f"No user found with email {email}."


def handle_update_user(message):
    info = extract_update_info(message)
    if not info:
        return "Sorry, I couldn't understand what to update."

    field_raw = info["field"].lower()
    value = info["value"]
    field = FIELD_MAP.get(field_raw)

    if not field:
        return f"Sorry, I don't know how to update '{field_raw}'."

    if info["type"] == "email":
        user = SystemUser.objects.filter(email__iexact=info["identifier"]).first()
    else:
        user = SystemUser.objects.filter(name__iexact=info["identifier"]).first()

    if not user:
        return f"No user found matching {info['identifier']}."

    setattr(user, field, value)
    user.save()
    return f"Updated {info['identifier']}'s {field} to {value}."

def process_message(message):
    intent, confidence = predict_intent(message)

    if intent == "add_user":
        return handle_add_user(message)
    elif intent == "remove_user":
        return handle_remove_user(message)
    elif intent == "update_user":
        return handle_update_user(message)
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"
    
 
def extract_name(text):
    match = re.search(r"named (\w+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# login view :

def login_view(request):
    error = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if SystemUser.objects.filter(email=email).exists():
                request.session["user_email"] = email
                return redirect("chat_view")
            else:
                error = "Email not found in system."
    else:
        form = LoginForm()
    return render(request, "chatbot/login.html", {"form": form, "error": error})


def chat_view(request):
    if "user_email" not in request.session:
        return redirect("login_view")

    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")
        response_text = process_message(message)
        return JsonResponse({"response": response_text})

    return render(request, "chatbot/chat.html", {"email": request.session["user_email"]})