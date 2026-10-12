# AgroSense-X
# Python Basics - Variables and Lists

# -----------------------------
# 1. Variables
# -----------------------------

name = "AgroSense-X"
crop = "Paddy"
number_of_crops = 4

print("Project:", name)
print("Crop:", crop)
print("Number of crops:", number_of_crops)


# -----------------------------
# 2. List of all crops
# -----------------------------

crops = ["Paddy", "Tomato", "Potato", "Grape"]

print("\nOur crops:")
print(crops)


# -----------------------------
# 3. Accessing individual crops
# -----------------------------

print("\nIndividual crops:")

print("Crop 1:", crops[0])
print("Crop 2:", crops[1])
print("Crop 3:", crops[2])
print("Crop 4:", crops[3])


# -----------------------------
# 4. Paddy disease list
# -----------------------------

paddy_diseases = [
    "Healthy",
    "Leaf Blast",
    "Brown Spot",
    "Bacterial Leaf Blight"
]

print("\nPaddy diseases:")
print(paddy_diseases)


# -----------------------------
# 5. Number of crops and diseases
# -----------------------------

print("\nNumber of crops:", len(crops))
print("Number of Paddy disease classes:", len(paddy_diseases))