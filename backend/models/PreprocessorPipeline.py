from sklearn.preprocessing import MinMaxScaler
import joblib

class PreprocessorPipeline:
    def __init__(self):
        """
        Initialize the scaler attribute.
            - scaler: MinMaxScaler object
            - MinMaxScaler: Transforms features by scaling each feature to a given range.
            - feature_names: List of feature names fitted during preprocessing.
        """
        self.scaler = None
        self.feature_names = None  # To store feature names

    def fit(self, data, numeric_columns):
        """Fit the scaler on the numeric columns."""
        self.scaler = MinMaxScaler()
        self.scaler.fit(data[numeric_columns])
        self.feature_names = data.columns.tolist()  # Store feature names
        print("Scaler fitted on numeric columns.")

    def transform(self, data, numeric_columns):
        '''Transform the data to match the feature order and apply scaling.'''
        if self.scaler is None:
            raise ValueError("Scaler has not been fitted. Call 'fit' first.")
        if self.feature_names is None:
            raise ValueError("Feature names are not set. Ensure 'fit' is called first.")

        # Reorder data to match the saved feature names
        data = data.reindex(columns=self.feature_names, fill_value=0)

        # Apply scaling only to numeric columns
        if not set(numeric_columns).issubset(data.columns):
            raise ValueError(f"Numeric columns {numeric_columns} are missing from the input data.")

        data[numeric_columns] = self.scaler.transform(data[numeric_columns])
        print("Data transformed successfully.")
        return data


    def fit_transform(self, data, numeric_columns):
        """Fit and transform the data in one step."""
        self.fit(data, numeric_columns)
        return self.transform(data, numeric_columns)

    def save_pipeline(self, file_path):
        """Save the preprocessing pipeline to a file."""
        pipeline_data = {"scaler": self.scaler, "feature_names": self.feature_names}
        joblib.dump(pipeline_data, file_path)
        print(f"Preprocessing pipeline saved to {file_path}.")

    def load_pipeline(self, file_path):
        """Load a saved preprocessing pipeline."""
        pipeline_data = joblib.load(file_path)
        self.scaler = pipeline_data["scaler"]
        self.feature_names = pipeline_data["feature_names"]
        print(f"Preprocessing pipeline loaded from {file_path}.")
