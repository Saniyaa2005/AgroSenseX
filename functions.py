# AgroSense-X
# Python Basics - Functions


# --------------------------------
# 1. A simple function
# --------------------------------

def welcome_message():
    print("Welcome to AgroSense-X!")
    print("Your intelligent crop health assistant.")


# Calling the function
welcome_message()


# --------------------------------
# 2. Function with an input
# --------------------------------

def greet_farmer(name):
    print("Hello", name)
    print("Welcome to AgroSense-X.")


greet_farmer("Farmer")


# --------------------------------
# 3. Function that returns a value
# --------------------------------

def calculate_average(a, b):
    average = (a + b) / 2
    return average


result = calculate_average(80, 90)

print("\nAverage:", result)


# --------------------------------
# 4. Crop information function
# --------------------------------

def show_crop_information(crop):
    print("\nCrop:", crop)

    if crop == "Paddy":
        print("This is a paddy crop.")

    elif crop == "Tomato":
        print("This is a tomato crop.")

    elif crop == "Potato":
        print("This is a potato crop.")

    elif crop == "Grape":
        print("This is a grape crop.")

    else:
        print("Crop information is not available.")


show_crop_information("Paddy")
show_crop_information("Tomato")


# --------------------------------
# 5. Disease assessment function
# --------------------------------

def assess_disease(disease, severity):

    print("\nDisease:", disease)
    print("Severity:", severity)

    if disease == "Healthy":
        message = "The crop appears healthy."

    elif severity == "Mild":
        message = "The disease appears mild. Regular monitoring is recommended."

    elif severity == "Moderate":
        message = "The disease appears moderate. Treatment and close monitoring are recommended."

    elif severity == "Severe":
        message = "The disease appears severe. Immediate attention is recommended."

    else:
        message = "Further analysis is required."

    return message


# Test the function

message = assess_disease("Leaf Blast", "Moderate")

print("Recommendation:", message)


# --------------------------------
# 6. Complete AgroSense-X example
# --------------------------------

def agro_sense_prediction(crop, disease, severity, confidence):

    print("\n------------------------------")
    print("      AGROSENSE-X RESULT")
    print("------------------------------")

    print("Crop:", crop)
    print("Disease:", disease)
    print("Severity:", severity)
    print("Confidence:", confidence)

    if disease == "Healthy":
        print("Status: The crop appears healthy.")

    elif severity == "Severe":
        print("Status: Severe disease detected.")
        print("Action: Immediate attention is recommended.")

    elif severity == "Moderate":
        print("Status: Moderate disease detected.")
        print("Action: Treatment and monitoring are recommended.")

    elif severity == "Mild":
        print("Status: Mild disease detected.")
        print("Action: Monitor the crop regularly.")

    else:
        print("Status: Further analysis is required.")


agro_sense_prediction(
    "Paddy",
    "Leaf Blast",
    "Moderate",
    0.87
)