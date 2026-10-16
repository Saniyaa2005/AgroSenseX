"""Standalone five-class crop validator. Run with the project's .venv_gpu Python."""
import json
from functools import lru_cache
import sys
from pathlib import Path

import torch
from PIL import Image, ImageOps
from torch import nn
from torchvision import transforms
from torchvision.models import efficientnet_b0

ROOT = Path(__file__).resolve().parent
CHECKPOINT = ROOT / "Results" / "Crop_Validator" / "checkpoints" / "crop_validator_best.pth"
CLASSES = ["Paddy", "Potato", "Tomato", "Grape", "Other"]


@lru_cache(maxsize=1)
def load_crop_model():
    checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=True)
    if checkpoint.get("classes") != CLASSES:
        raise RuntimeError("Unexpected crop validator classes")
    model = efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(CLASSES))
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    model.eval()
    return model


def predict(image_path):
    model = load_crop_model()
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    with Image.open(image_path) as image:
        tensor = transform(ImageOps.exif_transpose(image).convert("RGB")).unsqueeze(0)
    with torch.inference_mode():
        probabilities = torch.softmax(model(tensor).float(), dim=1)[0].tolist()
    winner = max(range(len(probabilities)), key=probabilities.__getitem__)
    return {
        "predicted_crop": CLASSES[winner],
        "confidence": probabilities[winner],
        "probabilities": dict(zip(CLASSES, probabilities)),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: crop_validator_inference.py IMAGE_PATH")
    print(json.dumps(predict(Path(sys.argv[1]))))
