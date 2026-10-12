
import json
import re
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_PATH = BASE_DIR / "knowledge" / "diseases.json"


# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def normalize(value):
    """
    Normalize crop and disease names so that labels such as
    Tomato___Early_blight and Tomato Early blight can match.
    """
    value = str(value or "").lower().strip()
    value = value.replace("___", " ")
    value = value.replace("_", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


# --------------------------------------------------
# LOAD KNOWLEDGE BASE
# --------------------------------------------------

def load_knowledge():
    """Load disease information from the local JSON file."""
    if not KNOWLEDGE_PATH.exists():
        return {"diseases": []}

    try:
        with KNOWLEDGE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {"diseases": []}

        diseases = data.get("diseases", [])

        if not isinstance(diseases, list):
            return {"diseases": []}

        return {"diseases": diseases}

    except (OSError, json.JSONDecodeError) as error:
        print(f"Warning: Could not load disease knowledge: {error}")
        return {"diseases": []}


# --------------------------------------------------
# KNOWLEDGE-BASE FIELD HELPERS
# --------------------------------------------------

def get_value(entry, *keys):
    """Return the first non-empty value for the requested keys."""
    for key in keys:
        value = entry.get(key)
        if value:
            return value
    return None


def format_items(value):
    """Convert a text field or list into a clean list of strings."""
    if isinstance(value, str):
        value = [value]

    if not isinstance(value, list):
        return []

    result = []

    for item in value:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())

        elif isinstance(item, dict):
            # Support simple structured entries where practical.
            text = (
                item.get("description")
                or item.get("advice")
                or item.get("name")
                or item.get("text")
            )

            if text:
                result.append(str(text).strip())

    return result


# --------------------------------------------------
# DISEASE MATCHING
# --------------------------------------------------

def find_disease_info(crop, disease):
    """
    Match a model prediction with an entry in diseases.json.

    Supports:
    - Underscores versus spaces
    - Case differences
    - Labels with crop prefixes, such as Tomato___Early_blight
    """
    data = load_knowledge()

    crop_key = normalize(crop)
    disease_key = normalize(disease)

    if not disease_key:
        return None

    candidates = []

    for entry in data["diseases"]:
        if not isinstance(entry, dict):
            continue

        entry_disease = normalize(
            get_value(entry, "disease", "disease_name", "name", "class_name")
        )

        entry_crop = normalize(
            get_value(entry, "crop", "crop_name")
        )

        if not entry_disease:
            continue

        # Crop names can appear either in a separate field or
        # as part of a model label.
        crop_matches = (
            not entry_crop
            or not crop_key
            or entry_crop == crop_key
            or entry_crop in crop_key
            or crop_key in entry_crop
        )

        if not crop_matches:
            continue

        # Exact normalized disease-name match.
        if entry_disease == disease_key:
            return entry

        # Handle a crop prefix in either name.
        disease_without_crop = disease_key
        entry_without_crop = entry_disease

        if crop_key:
            if disease_without_crop.startswith(crop_key + " "):
                disease_without_crop = disease_without_crop[
                    len(crop_key) + 1:
                ]

            if entry_without_crop.startswith(crop_key + " "):
                entry_without_crop = entry_without_crop[
                    len(crop_key) + 1:
                ]

        if entry_without_crop == disease_without_crop:
            return entry

        # Keep partial matches conservative to avoid matching
        # unrelated disease names.
        if (
            len(disease_without_crop) >= 6
            and (
                disease_without_crop in entry_without_crop
                or entry_without_crop in disease_without_crop
            )
        ):
            candidates.append(entry)

    # Only return a partial match when it is unambiguous.
    if len(candidates) == 1:
        return candidates[0]

    return None


# --------------------------------------------------
# HEALTHY CLASS DETECTION
# --------------------------------------------------

def is_healthy_prediction(disease):
    """Identify common healthy class labels."""
    label = normalize(disease)

    return (
        label in {"healthy", "normal"}
        or label.endswith(" healthy")
        or label.endswith(" normal")
    )


# --------------------------------------------------
# PREDICTION EXPLANATION
# --------------------------------------------------

def explain_prediction(prediction):
    """
    Build a farmer-friendly explanation from the prediction
    and the available local knowledge base.
    """
    if not isinstance(prediction, dict):
        return {
            "title": "No prediction available",
            "summary": (
                "Analyze a leaf image first to receive an explanation."
            ),
            "matched": False,
            "symptoms": [],
            "prevention": [],
            "treatment": [],
            "actions": [
                "Upload a clear image of the crop leaf."
            ],
            "confidence": None,
            "status": "No prediction",
        }

    crop = str(prediction.get("crop", "Unknown"))
    disease = str(prediction.get("disease", "Unknown"))
    confidence = prediction.get("confidence")
    status = str(prediction.get("status", "Review recommended"))

    # --------------------------------------------------
    # HEALTHY PREDICTION
    # --------------------------------------------------

    if is_healthy_prediction(disease):
        return {
            "title": "No disease detected by the model",
            "summary": (
                f"The model classified the {crop} leaf as healthy. "
                "This is encouraging, but it does not guarantee "
                "that the entire plant or crop is disease-free."
            ),
            "matched": True,
            "symptoms": [],
            "prevention": [
                "Inspect plants regularly for unusual spots, "
                "yellowing, wilting, or leaf damage.",
                "Maintain suitable watering and crop hygiene.",
                "Monitor the crop as it grows."
            ],
            "treatment": [],
            "actions": [
                "Continue monitoring your plants.",
                "If you can see disease symptoms despite this result, "
                "ask an agricultural expert to examine the plant."
            ],
            "confidence": confidence,
            "status": status,
        }

    # --------------------------------------------------
    # LOOK UP DISEASE
    # --------------------------------------------------

    entry = find_disease_info(crop, disease)

    if entry is None:
        return {
            "title": "Possible issue detected",
            "summary": (
                f"The model predicted '{disease}' for {crop}. "
                "However, a matching entry was not found in the "
                "local knowledge base. The prediction should be "
                "checked before deciding on treatment."
            ),
            "matched": False,
            "symptoms": [],
            "prevention": [],
            "treatment": [],
            "actions": [
                "Inspect several leaves and compare their symptoms.",
                "Take clear photographs of affected and healthy leaves.",
                "Ask a local agricultural officer or plant-health "
                "expert to confirm the diagnosis before treatment."
            ],
            "confidence": confidence,
            "status": status,
        }

    # --------------------------------------------------
    # EXTRACT KNOWLEDGE-BASE INFORMATION
    # --------------------------------------------------

    symptoms = format_items(
        get_value(entry, "symptoms", "common_symptoms")
    )

    prevention = format_items(
        get_value(
            entry,
            "prevention",
            "prevention_methods",
            "preventive_measures",
        )
    )

    treatment = format_items(
        get_value(
            entry,
            "treatment",
            "treatment_guidance",
            "management",
            "management_methods",
        )
    )

    display_name = get_value(
        entry,
        "disease",
        "disease_name",
        "name",
    ) or disease

    # --------------------------------------------------
    # BUILD FARMER-FRIENDLY EXPLANATION
    # --------------------------------------------------

    summary = (
        f"The model predicts that your {crop} leaf may be affected "
        f"by {display_name}. Compare the symptoms below with what "
        "you can see on your plant. An image prediction alone "
        "cannot confirm the disease."
    )

    actions = [
        "Inspect more than one plant to understand how widespread "
        "the symptoms may be.",
        "Confirm that the symptoms match before choosing a treatment.",
        "Consult a local agricultural expert if the problem is "
        "spreading or the diagnosis is uncertain."
    ]

    if not symptoms:
        actions.append(
            "Disease-specific symptoms are not yet recorded in "
            "the local knowledge base."
        )

    if not treatment:
        actions.append(
            "Specific treatment guidance is not available in the "
            "local knowledge base for this entry. Do not guess at "
            "a pesticide or dosage."
        )

    return {
        "title": f"Understanding {display_name}",
        "summary": summary,
        "matched": True,
        "symptoms": symptoms,
        "prevention": prevention,
        "treatment": treatment,
        "actions": actions,
        "confidence": confidence,
        "status": status,
    }


# --------------------------------------------------
# OPTIONAL COMMAND-LINE TEST
# --------------------------------------------------

if __name__ == "__main__":
    example_prediction = {
        "crop": "Tomato",
        "disease": "Tomato___Early_blight",
        "confidence": 0.87,
        "status": "Review recommended",
    }

    explanation = explain_prediction(example_prediction)

    print("\n--- AgroSense-X Result Explanation ---")
    print("Title:", explanation["title"])
    print("Summary:", explanation["summary"])
    print("Knowledge matched:", explanation["matched"])

    for section in ("symptoms", "prevention", "treatment", "actions"):
        print(f"\n{section.title()}:")

        items = explanation.get(section, [])

        if items:
            for item in items:
                print("-", item)
        else:
            print("- No information available.")