class InferencePipeline:
    def __init__(self, pipeline=None, model=None):
        """
        Initialize the inference pipeline with a preprocessing pipeline and a model.
        """
        self.pipeline = pipeline
        self.model = model

    def predict(self, user_data,numeric_columns):
        '''
        Predict the fitness type for a given user's data.
        - user_data: A dictionary of user attributes (e.g., {'age': 25, 'sex': 1, ...}).
        '''
        if not self.pipeline or not self.model:
            raise ValueError("Both pipeline and model must be set before prediction.")

        # Convert user data to a DataFrame for compatibility
        import pandas as pd
        user_df = pd.DataFrame([user_data])


        expected_features = self.pipeline.feature_names
        for col in expected_features:
            if col not in user_df.columns:
                user_df[col] = 0  # Add missing columns with default values (e.g., 0)
                
        # Reorder columns to match the expected feature order
        user_df = user_df[expected_features]

        # Apply preprocessing
        user_df = self.pipeline.transform(user_df, numeric_columns)

        # Make prediction
        prediction = self.model.predict(user_df)
        return prediction[0]


    def explain_prediction(self, user_data):
        """
        (Optional) Provide an explanation for the model's prediction using SHAP or similar tools.
        - user_data: A dictionary of user attributes.
        """
        # Example: Use SHAP (optional, requires installation and setup)
        import shap
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values([list(user_data.values())])
        return shap_values
