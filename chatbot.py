
import json
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator


# ============================================================
# AGROSENSE-X MULTILINGUAL CHATBOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "diseases.json"

LANGUAGES = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Marathi": "mr",
    "\u0c95\u0ca8\u0ccd\u0ca8\u0ca1": "kn",
    "\u0939\u093f\u0928\u094d\u0926\u0940": "hi",
    "\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41": "te",
    "\u0ba4\u0bae\u0bbf\u0bb4\u0bcd": "ta",
    "\u092e\u0930\u093e\u0920\u0940": "mr",
}

SUPPORTED_LANGUAGES = {
    "en": "English",
    "kn": "Kannada",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "mr": "Marathi",
}

TRANSLATION_COOLDOWN_SECONDS = 30
_translation_blocked_until = 0.0


# ============================================================
# KNOWLEDGE BASE
# ============================================================

def load_knowledge():
    """Load the local crop disease knowledge base."""
    try:
        with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        diseases = data.get("diseases", [])

        if not isinstance(diseases, list):
            return []

        return [
            item for item in diseases
            if isinstance(item, dict)
        ]

    except (OSError, json.JSONDecodeError) as error:
        print(f"Knowledge base loading error: {error}")
        return []


# ============================================================
# LANGUAGE HELPERS
# ============================================================

def resolve_language(language="English"):
    """Resolve language names and supported language codes."""
    if not language:
        return "en"

    value = str(language).strip()

    if value in LANGUAGES:
        return LANGUAGES[value]

    value = value.lower()

    if value in SUPPORTED_LANGUAGES:
        return value

    return "en"


def translate_text(
    text,
    target_language,
    source_language="auto",
):
    """
    Translate text using deep-translator.

    Returns None on failure. After a failure, pause translation
    requests briefly to reduce repeated rate-limit errors.
    """
    global _translation_blocked_until

    if text is None:
        return None

    text = str(text).strip()

    if not text:
        return text

    if source_language == target_language:
        return text

    if time.time() < _translation_blocked_until:
        return None

    try:
        translated = GoogleTranslator(
            source=source_language,
            target=target_language,
        ).translate(text)

        if not translated:
            raise ValueError("The translation service returned no text.")

        return translated

    except Exception as error:
        print(f"Translation unavailable: {error}")

        _translation_blocked_until = (
            time.time() + TRANSLATION_COOLDOWN_SECONDS
        )

        return None


def normalize(text):
    """Normalize English labels and questions for matching."""
    text = str(text or "").lower()
    text = text.replace("___", " ")
    text = text.replace("_", " ")
    text = re.sub(r"[^a-z0-9]+", " ", text)

    return re.sub(r"\s+", " ", text).strip()


# ============================================================
# FIND DISEASE INFORMATION
# ============================================================

def find_disease_info(crop, disease):
    """Find a disease using its crop name and model class label."""
    crop_key = normalize(crop)
    disease_key = normalize(disease)

    if not disease_key:
        return None

    for entry in load_knowledge():
        entry_crop = normalize(entry.get("crop", ""))
        entry_name = normalize(entry.get("name", ""))

        crop_matches = (
            not crop_key or entry_crop == crop_key
        )

        disease_matches = (
            entry_name == disease_key
        )

        if crop_matches and disease_matches:
            return entry

    return None


def search_knowledge(question, prediction=None):
    """Search the local knowledge base using an English question."""
    entries = load_knowledge()

    if not entries:
        return None

    question_key = normalize(question)

    # Use the latest prediction for questions about the current result.
    if isinstance(prediction, dict):
        predicted_crop = prediction.get("crop", "")
        predicted_disease = prediction.get(
            "disease",
            prediction.get("class_name", ""),
        )

        context_phrases = (
            "this disease",
            "this result",
            "my result",
            "this problem",
            "this leaf",
            "treat this",
            "prevent this",
            "what should i do",
        )

        if any(
            phrase in question_key
            for phrase in context_phrases
        ):
            entry = find_disease_info(
                predicted_crop,
                predicted_disease,
            )

            if entry:
                return entry

    # Search disease and crop names.
    matches = []

    for entry in entries:
        disease_name = normalize(entry.get("name", ""))
        crop_name = normalize(entry.get("crop", ""))

        if not disease_name:
            continue

        score = 0

        if disease_name in question_key:
            score += 10

        for word in disease_name.split():
            if len(word) >= 4 and word in question_key:
                score += 2

        if crop_name and crop_name in question_key:
            score += 3

        if score > 0:
            matches.append((score, entry))

    if not matches:
        return None

    matches.sort(key=lambda item: item[0], reverse=True)

    # Avoid an arbitrary selection when the top two diseases tie.
    if len(matches) > 1:
        first_score, first_entry = matches[0]
        second_score, second_entry = matches[1]

        if (
            first_score == second_score
            and normalize(first_entry.get("name", ""))
            != normalize(second_entry.get("name", ""))
        ):
            return None

    return matches[0][1]


# ============================================================
# FARMER-FRIENDLY ANSWERS
# ============================================================

def format_disease_answer(entry, question=""):
    """Build an answer using information from the knowledge base."""
    crop = entry.get("crop", "Unknown crop")
    disease = entry.get("name", "Unknown disease")

    symptoms = entry.get("symptoms", [])
    prevention = entry.get("prevention", [])
    treatment = entry.get("treatment", [])

    question_key = normalize(question)

    asks_symptoms = any(
        word in question_key
        for word in (
            "symptom",
            "symptoms",
            "sign",
            "look like",
            "identify",
        )
    )

    asks_prevention = any(
        word in question_key
        for word in (
            "prevent",
            "prevention",
            "avoid",
            "protect",
        )
    )

    asks_treatment = any(
        word in question_key
        for word in (
            "treat",
            "treatment",
            "cure",
            "medicine",
            "spray",
        )
    )

    show_all = not (
        asks_symptoms
        or asks_prevention
        or asks_treatment
    )

    lines = [
        f"Crop: {crop}",
        f"Possible disease: {disease}",
        "",
        (
            "This is educational guidance. An image-model "
            "prediction alone does not confirm a disease."
        ),
    ]

    if asks_symptoms or show_all:
        lines.extend(["", "Symptoms:"])

        if symptoms:
            lines.extend(f"- {item}" for item in symptoms)
        else:
            lines.append("- No symptom details are available.")

    if asks_prevention or show_all:
        lines.extend(["", "Prevention:"])

        if prevention:
            lines.extend(f"- {item}" for item in prevention)
        else:
            lines.append("- No prevention details are available.")

    if asks_treatment or show_all:
        lines.extend(["", "Treatment and management:"])

        if treatment:
            lines.extend(f"- {item}" for item in treatment)
        else:
            lines.append(
                "- Consult a local agricultural expert "
                "for management advice."
            )

    lines.extend([
        "",
        (
            "Safety: Confirm the disease before applying "
            "pesticides. Use only locally approved products "
            "and follow the product label."
        ),
    ])

    return "\n".join(lines)


# ============================================================
# MAIN CHATBOT FUNCTION
# ============================================================

def get_response(
    user_message,
    prediction=None,
    language="English",
):
    """
    Generate a multilingual crop-health response.

    Compatible with:
        get_response("How can I prevent tomato early blight?")
        get_response("What should I do?", prediction=result)
        get_response("ನನ್ನ ಬೆಳೆಗೆ ಏನು ಮಾಡಬೇಕು?", language="Kannada")
    """
    if not user_message or not str(user_message).strip():
        return "Please ask a question about your crop."

    language_code = resolve_language(language)
    message = str(user_message).strip()

    # Translate the farmer's question to English for searching.
    if language_code == "en":
        english_question = message
    else:
        english_question = translate_text(
            message,
            target_language="en",
            source_language="auto",
        )

    if not english_question:
        return (
            "I could not translate your question right now. "
            "The translation service may be temporarily busy. "
            "Please try again later or ask your question in English."
        )

    question_key = normalize(english_question)

    # Handle greetings.
    greetings = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if question_key in greetings:
        answer = (
            "Hello! I am AgroSense-X, your crop health assistant. "
            "Ask me about crop diseases, symptoms, prevention, "
            "or management guidance."
        )
    else:
        entry = search_knowledge(
            english_question,
            prediction=prediction,
        )

        if entry:
            answer = format_disease_answer(
                entry,
                question=english_question,
            )
        else:
            answer = (
                "I could not confidently match your question to "
                "a disease in the local knowledge base. Please "
                "mention the crop and disease name or describe "
                "the symptoms. You can also analyze a leaf image "
                "using Disease Detection. For uncertain or "
                "spreading problems, consult a local agricultural "
                "expert."
            )

    # Translate the answer into the farmer's selected language.
    if language_code == "en":
        return answer

    translated_answer = translate_text(
        answer,
        target_language=language_code,
        source_language="en",
    )

    if translated_answer:
        return translated_answer

    # Never falsely label English text as a successful translation.
    return (
        answer
        + "\n\n"
        + "Translation is temporarily unavailable. "
        + "This response is shown in English."
    )


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":
    print("AgroSense-X Multilingual Chatbot")
    print("Languages: English, Kannada, Hindi, Telugu, Tamil, Marathi")

    selected_language = input(
        "\nChoose a language (default English): "
    ).strip()

    if not selected_language:
        selected_language = "English"

    question = input("Ask a crop-health question: ").strip()

    print("\nAgroSense-X:")
    print(
        get_response(
            question,
            language=selected_language,
        )
    )