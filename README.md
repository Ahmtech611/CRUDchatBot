

Admin Chatbot  - User Management Console :

A natural-language admin chatbot that lets a logged-in admin **add, remove, and update system users** through plain chat commands instead of a traditional form-based UI.

Built as a technical assignment for **WP Bridate** (Sialkot) — Data Scientist / ML role.

---

## Overview

Instead of clicking through add/edit/delete forms, an admin can simply type:

```
can you add the user "john.smith@xyz.com" with phone number "+92332"
can you remove the user "john.smith@xyz.com"
can you update samanthas city to Cordoba
```

...and the chatbot understands the **intent** (add / remove / update), extracts the **relevant data** (email, phone, name, field, value) from the sentence, and performs the corresponding database operation — then replies with a confirmation message.

---

## Tech Stack

| Layer                 | Technology                                                   |
| --------------------- | ------------------------------------------------------------ |
| Intent Classification | Python, scikit-learn (TF-IDF + Multinomial Naive Bayes)      |
| Entity Extraction     | Python`re` (regex)                                         |
| Backend               | Django 4.2                                                   |
| Database              | SQLite                                                       |
| Frontend              | Django templates, vanilla JavaScript (fetch/AJAX), plain CSS |
| Auth                  | Custom email-based auto-login (session-based, no password)   |

---

## How It Works

```
User types a command
    
 1. JavaScript fetch() → POST /chat/
      
 2. Django view: process_message()
      
 3. ML model predicts intent (add_user / remove_user / update_user / unknown)
      
 4. Regex extracts entities (email, phone, name, field, value)
      
 5. Matching handler runs the DB operation (SystemUser model)
      
 6. JSON response → rendered as a chat bubble
```

### 1. Intent Classification (`chatbot/ml/train_model.py`)

- Training data: 4 intents (`add_user`, `remove_user`, `update_user`, `unknown`), 50 example phrases each, covering varied real-world phrasing (with/without quotes, "with email", possessive names, etc.)
- Vectorization: `TfidfVectorizer(ngram_range=(1, 2))` — unigrams + bigrams, so phrases like *"with email"* are captured, not just single words.
- Classifier: `MultinomialNB`
- Model is evaluated on an 80/20 split first, then **retrained on the full dataset** and saved with `joblib` for production use.
- A confidence threshold (0.4) prevents low-confidence guesses — anything below it falls back to a clarification message instead of a wrong action.

### 2. Entity Extraction (`chatbot/views.py`)

Regex handles the structured parts of a command:

- `extract_email()` — pulls an email address from the message
- `extract_phone()` — pulls a phone number
- `extract_name()` — pulls a name after "named X"
- `extract_update_info()` — handles both `update <name>'s <field> to <value>` and `update <email>'s <field> to <value>` patterns

### 3. Database Operations

Each intent has its own small handler function (`handle_add_user`, `handle_remove_user`, `handle_update_user`) that performs the actual `SystemUser` create/delete/update, with duplicate and not-found checks so the bot never crashes on bad input — it always replies with a clear message.

### 4. Auth Flow

- Login form asks only for an **email address** (no password), per the assignment spec.
- If the email exists in the `SystemUser` table, a session is created and the admin is redirected to the chat console.
- If not, a clear error is shown.

## Setup & Run

```bash
# 1. Install dependencies
pip install django scikit-learn joblib --break-system-packages

# 2. Train the intent classification model
python chatbot/ml/train_model.py

# 3. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create an admin user + at least one SystemUser (via /admin/) to log in with
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/login/`, sign in with a `SystemUser` email, and start chatting at `/chat/`.

---

## Example Commands (from assignment spec)

```
can you add the user "john.smith@xyz.com" with phone number "+92332"
can you remove the user "john.smith@xyz.com"
can you update samanthas city to Cordoba
```

All three are handled correctly end-to-end, along with variations (quoted/unquoted, "with email" phrasing, missing data, duplicate entries, and unrelated/unknown messages).

---

## Design Notes & Trade-offs

- **SQLite over MS SQL Server** — chosen deliberately to keep setup fast and dependency-free for a short assignment window; not a reflection of production preference.
- **Update matches by name (with email as a fallback)** — mirrors the assignment's own example (`"update samanthas city to Cordoba"` has no email), while still supporting email-based updates for more reliable matching.
- **Regex over ML for entity extraction** — emails/phone numbers/names are structured enough that regex is both simpler and more reliable than training a separate NER model for a project of this scope.
- **Chat history is not persisted** — only the current session's messages are shown in the UI. `SystemUser` data itself *is* persisted in SQLite. A `ChatHistory` model (per-user saved conversations) would be a natural next step for a production version.

## Possible Future Improvements

- Persist chat history per admin user (sidebar with past conversations)
- Expand training data further / add a lightweight NER model for entity extraction
- Support multi-field updates in a single command
- Role-based permissions for different admins
