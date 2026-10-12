# ============================================================
# AGROSENSE-X
# PROJECT CONFIGURATION
# ============================================================
#
# This file contains the main settings for our project.
#
# IMPORTANT:
# Do not put training code in this file.
# Do not modify the original datasets from here.
# ============================================================


import os


# ============================================================
# 1. PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 2. ORIGINAL DATASET DIRECTORY
# ============================================================

DATASET_ROOT = os.path.join(
    PROJECT_ROOT,
    "Datasets"
)


# ============================================================
# 3. INDIVIDUAL DATASET LOCATIONS
# ============================================================

PADDY_DATASET = os.path.join(
    DATASET_ROOT,
    "Paddy_dataset"
)


TOMATO_DATASET = os.path.join(
    DATASET_ROOT,
    "Tomato_dataset"
)


POTATO_DATASET = os.path.join(
    DATASET_ROOT,
    "Potato_dataset"
)


GRAPE_DATASET = os.path.join(
    DATASET_ROOT,
    "Grape_Leaf_dataset"
)


# ============================================================
# 4. TOMATO ACTUAL IMAGE LOCATION
# ============================================================
#
# Tomato is nested inside two folders before reaching
# train / val / test.
#
# We discovered this during our audit.
# ============================================================

TOMATO_SPLIT_ROOT = os.path.join(
    TOMATO_DATASET,
    "Summarized_PlantVillage_Split",
    "Summarized_PlantVillage_Split"
)


TOMATO_TRAIN = os.path.join(
    TOMATO_SPLIT_ROOT,
    "train"
)


TOMATO_VAL = os.path.join(
    TOMATO_SPLIT_ROOT,
    "val"
)


TOMATO_TEST = os.path.join(
    TOMATO_SPLIT_ROOT,
    "test"
)


# ============================================================
# 5. GRAPE ACTUAL IMAGE LOCATION
# ============================================================

GRAPE_IMAGE_ROOT = os.path.join(
    GRAPE_DATASET,
    "Dataset_images_CLEAN"
)


# ============================================================
# 6. OUTPUT DIRECTORIES
# ============================================================

MODELS_ROOT = os.path.join(
    PROJECT_ROOT,
    "models"
)


RESULTS_ROOT = os.path.join(
    PROJECT_ROOT,
    "results"
)


PROCESSED_ROOT = os.path.join(
    PROJECT_ROOT,
    "processed_data"
)


# ============================================================
# 7. CREATE OUTPUT DIRECTORIES
# ============================================================

os.makedirs(
    MODELS_ROOT,
    exist_ok=True
)


os.makedirs(
    RESULTS_ROOT,
    exist_ok=True
)


os.makedirs(
    PROCESSED_ROOT,
    exist_ok=True
)


# ============================================================
# 8. CROP NAMES
# ============================================================

CROPS = [
    "Paddy",
    "Tomato",
    "Potato",
    "Grape"
]


# ============================================================
# 9. IMAGE SETTINGS
# ============================================================
#
# CNN models normally require all images to have the same
# input size.
#
# We will use 224 x 224 pixels.
# ============================================================

IMAGE_SIZE = (
    224,
    224
)


IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224


# ============================================================
# 10. IMAGE CHANNELS
# ============================================================

IMAGE_CHANNELS = 3


# ============================================================
# 11. TRAINING SETTINGS
# ============================================================

BATCH_SIZE = 32


EPOCHS = 20


RANDOM_SEED = 42


# ============================================================
# 12. VALIDATION / TEST SETTINGS
# ============================================================
#
# These values are mainly for datasets where we need to
# create our own split.
#
# Tomato already has train / val / test.
# ============================================================

VALIDATION_SPLIT = 0.20

TEST_SPLIT = 0.10


# ============================================================
# 13. SUPPORTED IMAGE FORMATS
# ============================================================

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# ============================================================
# 14. DATASET SUMMARY
# ============================================================
#
# These are the verified values from our audit.
#
# We keep them here as reference.
# ============================================================

DATASET_SUMMARY = {

    "Paddy": {
        "classes": 13,
        "images": 16225
    },

    "Tomato": {
        "classes": 10,
        "images": 18160
    },

    "Potato": {
        "classes": 6,
        "images": 5748
    },

    "Grape": {
        "classes": 8,
        "images": 247
    }
}


# ============================================================
# 15. PROJECT TOTALS
# ============================================================

TOTAL_CLASSES = 37

TOTAL_IMAGES = 40380


# ============================================================
# 16. DISPLAY CONFIGURATION
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("                 AGROSENSE-X")
    print("              PROJECT CONFIGURATION")
    print("=" * 70)


    print("\nProject root:")
    print(PROJECT_ROOT)


    print("\nDataset root:")
    print(DATASET_ROOT)


    print("\nDatasets:")


    print(
        "Paddy  :",
        PADDY_DATASET
    )


    print(
        "Tomato :",
        TOMATO_DATASET
    )


    print(
        "Potato :",
        POTATO_DATASET
    )


    print(
        "Grape  :",
        GRAPE_DATASET
    )


    print("\nOutput directories:")


    print(
        "Models    :",
        MODELS_ROOT
    )


    print(
        "Results   :",
        RESULTS_ROOT
    )


    print(
        "Processed :",
        PROCESSED_ROOT
    )


    print("\nImage size:")

    print(
        IMAGE_WIDTH,
        "x",
        IMAGE_HEIGHT
    )


    print(
        "\nTotal verified images:",
        TOTAL_IMAGES
    )


    print(
        "Total verified classes:",
        TOTAL_CLASSES
    )


    print("\nConfiguration loaded successfully.")

    print("=" * 70)