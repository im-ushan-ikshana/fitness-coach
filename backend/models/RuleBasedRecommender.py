class RuleBasedRecommender:
    """
    Rule-based recommendation system to classify users (0-6)
    based on dynamically calculated BMI, medical conditions, and age.
    """

    @staticmethod
    def calculate_bmi(weight, height):
        """
        Calculates BMI using the formula: weight (kg) / height (m)^2.
        """
        if height <= 0:
            raise ValueError("Height must be greater than zero.")
        
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)
        return round(bmi, 1)

    @staticmethod
    def get_recommendation_level(weight, height, age, hypertension, diabetes):
        """
        Determines the recommendation level based on calculated BMI, medical conditions, and age.

        **Recommendation Levels:**
        - 0: **No exercise recommended** (Severe medical concerns, extremely high or low BMI)
        - 1: **Minimal activity** (Medical supervision required)
        - 2: **Light exercise only** (With doctor's approval)
        - 3-4: **Standard workout plan**
        - 5-6: **Weight management & professional oversight required**
        """

        # Calculate BMI dynamically
        bmi = RuleBasedRecommender.calculate_bmi(weight, height)

        # **1️⃣ No Exercise Recommended (Severe Health Risk)**
        if bmi >= 40:  # BMI >= 40 (Severely Obese)
            return 0
        if bmi < 16:  # Extremely underweight
            return 0
        if hypertension == "Yes" and diabetes == "Yes":  # Both medical conditions present
            return 0
        if age > 65 and (hypertension == "Yes" or diabetes == "Yes"):  # Elderly with conditions
            return 0

        # **2️⃣ Light Activity with Medical Advice**
        if bmi >= 35 or (age >= 60 and bmi >= 30):
            return 1
        if hypertension == "Yes" or diabetes == "Yes":
            return 2

        # **3️⃣ Standard Exercise Recommendations**
        if 25 <= bmi < 35:
            return 3
        if 18.5 <= bmi < 25:  # Healthy BMI range
            return 4

        # **4️⃣ Underweight or Special Cases**
        if bmi < 18.5:
            return 5
        if age < 18:
            return 5

        return 6  # Default case (Good fitness condition)
