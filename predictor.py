import os
import torch
import torch.nn as nn

from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b0


# ============================================================
# AGROSENSE-X
# PREDICTOR MODULE
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

MODELS_ROOT = os.path.join(
    PROJECT_ROOT,
    "Models"
)


# ============================================================
# DEVICE
# ============================================================

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


# ============================================================
# IMAGE SETTINGS
# ============================================================

IMAGE_SIZE = 224

transform = transforms.Compose([
    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_CONFIGS = {

    "paddy": {
        "display_name": "Paddy",
        "model_file": "paddy_efficientnet_b0_best.pth",
        "confidence_threshold": 0.60
    },

    "potato": {
        "display_name": "Potato",
        "model_file": "potato_efficientnet_b0_best.pth",
        "confidence_threshold": 0.60
    },

    "tomato": {
        "display_name": "Tomato",
        "model_file": "tomato_efficientnet_b0_best.pth",
        "confidence_threshold": 0.60
    },

    "grape": {
        "display_name": "Grape",
        "model_file": "grape_niphad_efficientnet_b0_best.pth",
        "confidence_threshold": 0.75
    }
}


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(crop_key):

    if crop_key not in MODEL_CONFIGS:
        raise ValueError(
            f"Unknown crop: {crop_key}"
        )

    config = MODEL_CONFIGS[crop_key]

    model_path = os.path.join(
        MODELS_ROOT,
        config["model_file"]
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found:\n{model_path}"
        )

    print(
        f"Loading {config['display_name']} model..."
    )

    checkpoint = torch.load(
        model_path,
        map_location=DEVICE,
        weights_only=True
    )

    class_names = checkpoint[
        "class_names"
    ]

    num_classes = checkpoint[
        "num_classes"
    ]

    # --------------------------------------------------------
    # Create EfficientNet-B0
    # --------------------------------------------------------

    model = efficientnet_b0(
        weights=None
    )

    input_features = (
        model.classifier[1].in_features
    )

    model.classifier = nn.Sequential(
        nn.Dropout(
            p=0.40
        ),

        nn.Linear(
            input_features,
            num_classes
        )
    )

    # --------------------------------------------------------
    # Load trained weights
    # --------------------------------------------------------

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    model = model.to(
        DEVICE
    )

    model.eval()

    return model, class_names


# ============================================================
# PREDICT IMAGE
# ============================================================

def predict_image(
    image_path,
    crop_key
):

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found:\n{image_path}"
        )

    model, class_names = load_model(
        crop_key
    )

    # --------------------------------------------------------
    # Open image
    # --------------------------------------------------------

    image = Image.open(
        image_path
    ).convert(
        "RGB"
    )

    # --------------------------------------------------------
    # Preprocess
    # --------------------------------------------------------

    image_tensor = transform(
        image
    )

    image_tensor = image_tensor.unsqueeze(
        0
    )

    image_tensor = image_tensor.to(
        DEVICE
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )[0]

    # --------------------------------------------------------
    # Top 3 predictions
    # --------------------------------------------------------

    top_k = min(
        3,
        len(class_names)
    )

    top_probabilities, top_indices = torch.topk(
        probabilities,
        top_k
    )

    top_predictions = []

    for probability, index in zip(
        top_probabilities,
        top_indices
    ):

        top_predictions.append({

            "disease": class_names[
                index.item()
            ],

            "confidence": float(
                probability.item()
            )
        })

    # --------------------------------------------------------
    # Best prediction
    # --------------------------------------------------------

    best_prediction = top_predictions[0]

    best_confidence = (
        best_prediction["confidence"]
    )

    threshold = MODEL_CONFIGS[
        crop_key
    ]["confidence_threshold"]

    # --------------------------------------------------------
    # Confidence status
    # --------------------------------------------------------

    if best_confidence >= threshold:
        confidence_status = "HIGH"
    else:
        confidence_status = "LOW"

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    result = {

        "crop": MODEL_CONFIGS[
            crop_key
        ]["display_name"],

        "crop_key": crop_key,

        "disease": best_prediction[
            "disease"
        ],

        "confidence": best_confidence,

        "confidence_percentage":
            best_confidence * 100,

        "confidence_threshold":
            threshold,

        "confidence_status":
            confidence_status,

        "top_predictions":
            top_predictions,

        "device":
            str(DEVICE)
    }

    # --------------------------------------------------------
    # Grape warning
    # --------------------------------------------------------

    if crop_key == "grape":

        result["warning"] = (
            "The Grape model was trained on a "
            "small dataset. Predictions should "
            "be treated as experimental and "
            "verified when possible."
        )

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "AGROSENSE-X PREDICTOR TEST"
    )

    print("=" * 60)

    print(
        "Device:",
        DEVICE
    )

    print(
        "\nAvailable crops:"
    )

    for crop in MODEL_CONFIGS:

        print(
            "-",
            crop
        )
