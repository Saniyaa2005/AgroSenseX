# AgroSense-X
# Python Basics - Decision Making with if statements

# --------------------------------
# 1. Basic decision
# --------------------------------

severity = "Moderate"

print("Crop severity:", severity)

if severity == "Severe":
    print("Warning: Immediate attention is required.")
else:
    print("The crop does not have severe symptoms.")


# --------------------------------
# 2. Multiple decisions
# --------------------------------

print("\nSeverity assessment:")

if severity == "Healthy":
    print("The crop appears healthy.")

elif severity == "Mild":
    print("The disease appears mild.")
    print("Monitor the crop regularly.")

elif severity == "Moderate":
    print("The disease appears moderate.")
    print("Treatment and regular monitoring are recommended.")

elif severity == "Severe":
    print("The disease appears severe.")
    print("Immediate agricultural intervention is recommended.")

else:
    print("Unknown severity level.")


# --------------------------------
# 3. Disease-based decision
# --------------------------------

disease = "Leaf Blast"

print("\nDisease:", disease)

if disease == "Leaf Blast":
    print("Possible action: inspect affected leaves and follow suitable disease-management practices.")

elif disease == "Brown Spot":
    print("Possible action: inspect the crop for brown lesions and follow suitable management practices.")

elif disease == "Bacterial Leaf Blight":
    print("Possible action: inspect the crop for water-soaked or yellowing lesions and follow suitable management practices.")

elif disease == "Healthy":
    print("No disease has been identified.")

else:
    print("Disease information is not available.")


# --------------------------------
# 4. Combining disease and severity
# --------------------------------

print("\nFinal AgroSense-X assessment:")

if disease != "Healthy" and severity == "Severe":
    print("Disease detected with severe symptoms.")
    print("Priority: Immediate attention.")

elif disease != "Healthy" and severity == "Moderate":
    print("Disease detected with moderate symptoms.")
    print("Priority: Treatment and close monitoring.")

elif disease != "Healthy" and severity == "Mild":
    print("Disease detected with mild symptoms.")
    print("Priority: Monitor and take appropriate preventive action.")

elif disease == "Healthy":
    print("The crop appears healthy.")

else:
    print("Assessment requires further analysis.")