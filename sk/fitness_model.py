import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Create a simulated dataset
def generate_synthetic_data():
    # Set random seeds to ensure reproducibility
    np.random.seed(42)
    
    # Define the dataset size
    n_samples = 1000
    
    # Generate age ranges
    age_ranges = ['13-18', '19-35', '36-55', '56 and above']
    age_weights = [0.15, 0.4, 0.3, 0.15]  # Weights for each age group
    ages = np.random.choice(age_ranges, size=n_samples, p=age_weights)
    
    # Generate gender
    genders = np.random.choice(['Male', 'Female'], size=n_samples)
    
    # Generate BMI values
    bmi_values = np.random.normal(24.5, 5, n_samples)  # The mean is 24.5 and the standard deviation is 5
    bmi_values = np.clip(bmi_values, 16, 40)  # Limit the BMI range
    
    # Produces body fat percentage
    def generate_bfp(gender, bmi, age_range):
        # Generate a reasonable body fat percentage based on gender and BMI
        age_factor = {'13-18': 0.8, '19-35': 1.0, '36-55': 1.2, '56 and above': 1.3}
        base = 10 if gender == 'Male' else 20
        variation = np.random.normal(0, 2)  # Add some random variations
        return base + (bmi - 18.5) * 0.6 * age_factor[age_range] + variation
    
    bfp_values = [generate_bfp(gender, bmi, age) for gender, bmi, age in zip(genders, bmi_values, ages)]
    bfp_values = np.clip(bfp_values, 5, 50)  # Limit the range of body fat percentage
    
    # Generate movement levels
    activity_levels = np.random.choice(['Low', 'Medium', 'High'], size=n_samples, p=[0.4, 0.4, 0.2])
    
    # Generate fitness goals
    goals = np.random.choice(['Muscle Gain', 'Fat Loss', 'Body Shaping', 'Improve Flexibility', 'Improve Endurance'], 
                            size=n_samples)
    
    # Generate recommended exercises
    exercise_categories = {
        'Muscle Gain': [
            'Push-ups', 'Pull-ups', 'Bench Press', 'Squats', 'Deadlifts', 'Shoulder Press',
            'Barbell Rows', 'Dumbbell Curls', 'Tricep Extensions', 'Leg Press'
        ],
        'Fat Loss': [
            'Running', 'HIIT', 'Cycling', 'Swimming', 'Jump Rope', 'Burpees',
            'Mountain Climbers', 'Rowing', 'Elliptical Training', 'Stair Climbing'
        ],
        'Body Shaping': [
            'Pilates', 'Yoga', 'Barre', 'Resistance Band Training', 'Circuit Training',
            'Bodyweight Training', 'TRX Training', 'Core Exercises', 'Functional Training', 'Kettlebell Workouts'
        ],
        'Improve Flexibility': [
            'Yoga', 'Stretching', 'Tai Chi', 'Dynamic Stretching', 'PNF Stretching',
            'Ballet', 'Gymnastics', 'Mobility Drills', 'Foam Rolling', 'Active Isolated Stretching'
        ],
        'Improve Endurance': [
            'Long Distance Running', 'Cycling', 'Swimming', 'Rowing', 'Cross-Country Skiing',
            'Hiking', 'Stair Climbing', 'Circuit Training', 'Interval Training', 'Triathlon Training'
        ]
    }
    
    # Generate recommended exercise items based on goals and other characteristics
    def generate_recommended_exercise(goal, age, gender, bmi, activity_level):
        # Select from the list of motions for the target
        potential_exercises = exercise_categories[goal]
        
        # Adjust the recommended probability based on age, sex, BMI, and activity level
        if age == '13-18':
            # Teenagers are more suitable for basic training
            weights = [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05]
        elif age == '56 and above':
            # Older people are better suited for low-intensity training
            weights = [0.05, 0.05, 0.05, 0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1]
        else:
            # Adult weights are relatively balanced
            weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        
        # Adjust the weights according to BMI
        if bmi > 30:  # Obese
            # Reduce the weight of high-intensity training
            for i, exercise in enumerate(potential_exercises):
                if any(term in exercise.lower() for term in ['running', 'jump', 'hiit', 'burpees']):
                    weights[i] *= 0.5
        
        # Adjust the weights according to the activity level
        if activity_level == 'Low':
            # Reduce the weight of high-intensity training
            for i, exercise in enumerate(potential_exercises):
                if any(term in exercise.lower() for term in ['hiit', 'deadlifts', 'intense']):
                    weights[i] *= 0.3
        elif activity_level == 'High':
            # Increase the weight of high-intensity training
            for i, exercise in enumerate(potential_exercises):
                if any(term in exercise.lower() for term in ['hiit', 'intense', 'training']):
                    weights[i] *= 1.5
        
        # Normalized weights
        weights = np.array(weights)
        weights = weights / weights.sum()
        
        # Select a sport
        return np.random.choice(potential_exercises, p=weights)
    
    recommended_exercises = [generate_recommended_exercise(goal, age, gender, bmi, level) 
                            for goal, age, gender, bmi, level in 
                            zip(goals, ages, genders, bmi_values, activity_levels)]
    
    # Create DataFrame
    data = pd.DataFrame({
        'age': ages,
        'gender': genders,
        'bmi': bmi_values,
        'body_fat_percentage': bfp_values,
        'activity_level': activity_levels,
        'goal': goals,
        'recommended_exercise': recommended_exercises
    })
    
    return data

# Train the model
def train_model(data=None):
    if data is None:
        data = generate_synthetic_data()
    
    # Feature encoding
    label_encoders = {}
    for column in ['age', 'gender', 'activity_level', 'goal']:
        le = LabelEncoder()
        data[column + '_encoded'] = le.fit_transform(data[column])
        label_encoders[column] = le
    
    # Prepare features and target variables
    X = data[['age_encoded', 'gender_encoded', 'bmi', 'body_fat_percentage', 'activity_level_encoded', 'goal_encoded']]
    y = data['recommended_exercise']
    
    # Train a random forest classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, label_encoders, data

# Generate recommendations
def generate_recommendations(user_data, top_n=5):
    # Train a model (or load a pretrained model)
    model, label_encoders, training_data = train_model()
    
    # Encoding user data
    user_features = []
    try:
        for column in ['age', 'gender', 'activity_level', 'goal']:
            if column in user_data and user_data[column] in label_encoders[column].classes_:
                user_features.append(label_encoders[column].transform([user_data[column]])[0])
            else:
                # If the feature is invalid, an error message is returned
                raise ValueError(f'Invalid value for {column}: {user_data.get(column)}')
    
        # Add BMI and body fat percentage
        bmi = float(user_data.get('bmi', 22.0))
        bfp = float(user_data.get('body_fat_percentage', 20.0))
        if not (16 <= bmi <= 40):
            raise ValueError(f'BMI value out of range: {bmi}')
        if not (5 <= bfp <= 50):
            raise ValueError(f'Body fat percentage out of range: {bfp}')
        user_features.append(bmi)
        user_features.append(bfp)
    
        # Reorder features to match training data
        user_features_ordered = [
            user_features[0],  # age_encoded
            user_features[1],  # gender_encoded
            user_features[4],  # bmi
            user_features[5],  # body_fat_percentage
            user_features[2],  # activity_level_encoded
            user_features[3],  # goal_encoded
        ]
    except (ValueError, TypeError) as e:
        raise ValueError(f'Invalid input parameters: {str(e)}')
    
    try:
        # Predict probability
        proba = model.predict_proba([user_features_ordered])[0]
    except Exception as e:
        raise ValueError(f'Error during prediction: {str(e)}')
    
    # Get the top N recommendations
    top_indices = proba.argsort()[-top_n:][::-1]
    top_classes = [model.classes_[i] for i in top_indices]
    
    # Get confidence in your recommendations
    confidences = [proba[i] for i in top_indices]
    
    # Create a referral list
    recommendations = []
    for exercise, confidence in zip(top_classes, confidences):
        # Find similar users in your training data
        similar_users = training_data[
            (training_data['recommended_exercise'] == exercise) &
            (training_data['goal'] == user_data['goal'])
        ]
        
        # Count the number of users
        user_count = len(similar_users)
        
        recommendations.append({
            'exercise': exercise,
            'confidence': round(confidence * 100, 1),
            'similar_users': user_count
        })
    
    return recommendations

# Get all possible recommendations
def get_all_exercise_options():
    exercise_categories = {
        'Muscle Gain': [
            'Push-ups', 'Pull-ups', 'Bench Press', 'Squats', 'Deadlifts', 'Shoulder Press',
            'Barbell Rows', 'Dumbbell Curls', 'Tricep Extensions', 'Leg Press'
        ],
        'Fat Loss': [
            'Running', 'HIIT', 'Cycling', 'Swimming', 'Jump Rope', 'Burpees',
            'Mountain Climbers', 'Rowing', 'Elliptical Training', 'Stair Climbing'
        ],
        'Body Shaping': [
            'Pilates', 'Yoga', 'Barre', 'Resistance Band Training', 'Circuit Training',
            'Bodyweight Training', 'TRX Training', 'Core Exercises', 'Functional Training', 'Kettlebell Workouts'
        ],
        'Improve Flexibility': [
            'Yoga', 'Stretching', 'Tai Chi', 'Dynamic Stretching', 'PNF Stretching',
            'Ballet', 'Gymnastics', 'Mobility Drills', 'Foam Rolling', 'Active Isolated Stretching'
        ],
        'Improve Endurance': [
            'Long Distance Running', 'Cycling', 'Swimming', 'Rowing', 'Cross-Country Skiing',
            'Hiking', 'Stair Climbing', 'Circuit Training', 'Interval Training', 'Triathlon Training'
        ]
    }
    
    all_exercises = []
    for category, exercises in exercise_categories.items():
        for exercise in exercises:
            all_exercises.append({
                'name': exercise,
                'category': category
            })
    
    return all_exercises

# If you run this file directly, sample data is generated
if __name__ == "__main__":
    data = generate_synthetic_data()
    print(f"Generated {len(data)} synthetic fitness records")
    print(data.head())
    
    # Train the model
    model, encoders, _ = train_model(data)
    print("Model trained successfully")
    
    # Test recommended
    test_user = {
        'age': '19-35',
        'gender': 'Male',
        'bmi': 24.5,
        'body_fat_percentage': 18.0,
        'activity_level': 'Medium',
        'goal': 'Muscle Gain'
    }
    
    recommendations = generate_recommendations(test_user)
    print("\nRecommendations for test user:")
    for rec in recommendations:
        print(f"{rec['exercise']} (Confidence: {rec['confidence']}%, Similar users: {rec['similar_users']})")