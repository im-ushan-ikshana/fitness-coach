import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

class ModelTrainer:
    def __init__(self, model_type='random_forest', **kwargs):
        """
        Initialize the ModelTrainer with a specified model type.
        Supported models: 'random_forest'.
        """
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(**kwargs)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def train_model(self, X_train, y_train):
        """Train the model on the given training data."""
        self.model.fit(X_train, y_train)
        print("Model trained successfully.")
        return self.model

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate the model on the test data."""
        y_pred = model.predict(X_test)
        print("Evaluation Results:")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

    def save_model(self, model, file_path):
        """Save the trained model to a file."""
        #if the path is not available, create the path
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        joblib.dump(model, file_path)
        print(f"Model saved to {file_path}.")

    def load_model(self, file_path):
        """Load a model from a file."""
        model = joblib.load(file_path)
        print(f"Model loaded from {file_path}.")
        return model

