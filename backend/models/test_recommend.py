import os
from backend.models.PreprocessorPipeline import PreprocessorPipeline
from backend.models.ModelTrainer import ModelTrainer
from backend.models.InferencePipeline import InferencePipeline
 
# Paths
MODEL_PATH = os.path.join('backend','models','recommend_model.pkl')
PIPELINE_PATH = os.path.join('backend','models','recommend_preprocessor_pipeline.pkl')

# Load Model and Pipeline
trainer = ModelTrainer()
model = trainer.load_model(MODEL_PATH)

pipeline = PreprocessorPipeline()
pipeline.load_pipeline(PIPELINE_PATH)

# Inference Pipeline
inference = InferencePipeline(pipeline=pipeline, model=model)


# Test Data (New User)
new_user_data = {
    # weight,height,bmi,gender,age
    'weight': 22.58,
    'height': 154,
    'bmi': 29.8,
    'gender': 1,
    'age': 32,
}
numeric_columns = ['weight','height','bmi','age']

# Predict Fitness Type
prediction = inference.predict(new_user_data,numeric_columns=numeric_columns)
print(f"Recommendation to Exerecise : {prediction}")
