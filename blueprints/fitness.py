from flask import render_template, request, jsonify
from . import fitness_bp
from math import pow
from flask import jsonify, request
import pandas as pd
from sk.fitness_model import generate_recommendations as model_generate_recommendations
import concurrent.futures
import time
from functools import reduce

@fitness_bp.route('/', methods=['GET'])
def index():
    return render_template('fitness/index.html')

def calculate_metrics_map_reduce(data):
<<<<<<< HEAD
    """使用MapReduce模式并行计算各项指标"""
    # Mapper函数
=======
    """Use MapReduce pattern calculate the metrics paralelly"""
    # Mapper function
>>>>>>> f4a32df (v10)
    def mapper(item):
        key, func = item
        return (key, func())
    
<<<<<<< HEAD
    # 准备计算任务
=======
    # Prepare for calculation tasks
>>>>>>> f4a32df (v10)
    tasks = [
        ('bmi', lambda: calculate_bmi(data['weight'], data['height'])),
        ('bfp', lambda: calculate_bfp_parallel(data['weight'], data['height'], data['age_range'], data['gender'])),
    ]
    
    if data.get('waist') and data.get('hips'):
        tasks.append(('whr', lambda: calculate_whr_parallel(data['waist'], data['hips'], data['gender'])))
    
    tasks.append(('calories', lambda: calculate_daily_calories_parallel(
        data['weight'], data['height']*100, data['age_range'], data['gender'], data['level']
    )))
    
<<<<<<< HEAD
    # 使用线程池并行执行Map阶段
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(mapper, tasks))
    
    # Reduce阶段：将结果合并为字典
    return dict(results)

def generate_recommendations_map_reduce(age_range, level, goal, bmi_category, bfp_category):
    """使用MapReduce模式生成推荐"""
=======
    # use threadpool and execute Map stage
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(mapper, tasks))
    
    # Reduce stage：combine the results into dictionary.
    return dict(results)

def generate_recommendations_map_reduce(age_range, level, goal, bmi_category, bfp_category):
    """use MapReduce pattern to generate recommendations"""
>>>>>>> f4a32df (v10)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rec_future = executor.submit(generate_recommendations, age_range, level, goal, bmi_category, bfp_category)
        workout_future = executor.submit(generate_workout_plan, rec_future, level)
        return rec_future.result(), workout_future.result()

@fitness_bp.route('/calculate', methods=['POST'])
def calculate():
    start_time = time.time()
    
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400, {'Content-Type': 'application/json'}
    
    try:
        data = request.get_json()

        if not all(key in data for key in ['weight', 'height', 'age', 'gender', 'goal', 'level']):
            return jsonify({'error': 'Missing required parameters'}), 400
            
        weight = float(data.get('weight'))
        height = float(data.get('height')) / 100  # Convert to meters
        age_range = data.get('age')
        gender = data.get('gender')
        goal = data.get('goal')
        level = data.get('level')
        
<<<<<<< HEAD
        # 使用MapReduce模式并行计算各项指标
=======
        # use MapReduce pattern to calculate metrics paralelly
>>>>>>> f4a32df (v10)
        metrics_data = {
            'weight': weight,
            'height': height,
            'age_range': age_range,
            'gender': gender,
            'level': level,
            'waist': data.get('waist'),
            'hips': data.get('hips')
        }
        
        metrics = calculate_metrics_map_reduce(metrics_data)
        
        bmi = metrics['bmi']
        bfp = metrics['bfp']
        whr_info = metrics.get('whr')
        daily_calories = metrics['calories']
        
        bmi_category = get_bmi_category(bmi)
        bfp_category = get_bfp_category(bfp, gender)
        
        # BMI result information
        bmi_info = {
            'category': 'BMI (Body Mass Index)',
            'description': 'BMI is a common indicator used to assess the relationship between weight and height, providing an initial assessment of whether weight is healthy.',
            'formula': 'BMI = Weight(kg) ÷ Height(m)²',
            'ranges': [
                {'range': '< 18.5', 'category': 'Underweight'},
                {'range': '18.5 - 24.9', 'category': 'Normal'},
                {'range': '25.0 - 29.9', 'category': 'Overweight'},
                {'range': '30.0 - 34.9', 'category': 'Obesity (Grade I)'},
                {'range': '35.0 - 39.9', 'category': 'Obesity (Grade II)'},
                {'range': '≥ 40.0', 'category': 'Obesity (Grade III)'},
            ],
            'result': f'{round(bmi, 1)} - {bmi_category}',
            'note': 'BMI is applicable to most adults but not suitable for children, pregnant women, and certain special populations.',
            'gender': gender
        }
        
        # Body fat percentage result information
        bfp_info = {
            'category': 'Body Fat Percentage (BFP)',
            'description': 'Body fat percentage reflects the proportion of body fat to total weight and is an important indicator for assessing body composition.',
            'formula': 'Male: (1.20 × BMI) + (0.23 × Age) - 16.2\nFemale: (1.20 × BMI) + (0.23 × Age) - 5.4',
            'ranges': [
                {'gender': 'Male', 'healthy': '10-20%', 'overweight': '20-25%', 'obese': '> 25%'},
                {'gender': 'Female', 'healthy': '20-30%', 'overweight': '30-35%', 'obese': '> 35%'}
            ],
            'result': f'{round(bfp, 1)}% - {bfp_category}',
            'note': 'Body fat percentage can also be measured using body fat scales or professional equipment, which may be more accurate than calculated results.',
            'gender': gender
        }
        
        height_in_meters = height
        weight_range = {
            'min': round(18.5 * (height_in_meters ** 2), 1),
            'max': round(24.9 * (height_in_meters ** 2), 1)
        }
        
<<<<<<< HEAD
        # 使用MapReduce模式生成推荐
=======
        # use MapReduce pattern to generate recommendations
>>>>>>> f4a32df (v10)
        fitness_recommendations, workout_plan = generate_recommendations_map_reduce(
            age_range, level, goal, bmi_category, bfp_category
        )
        
        # Generate nutritional recommendations
        nutrition_tips = [
            f"Daily Calorie Requirement: {round(daily_calories)} calories",
            f"Recommended Weight Range: {weight_range['min']}-{weight_range['max']} kg",
            "Maintain adequate protein intake, 1.6-2.2g per kg of body weight",
            "Ensure sufficient carbohydrate intake for energy",
            "Supplement with essential vitamins and minerals"
        ]
        
        # Prepare user data for model recommendations
        user_data = {
            'age': age_range,
            'gender': gender,
            'bmi': bmi,
            'body_fat_percentage': bfp,
            'activity_level': level,
            'goal': goal
        }
        
        try:
            # Get personalized exercise recommendations
            exercise_recommendations = model_generate_recommendations(user_data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Failed to generate exercise recommendations'}), 500
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return jsonify({
            'bmi_info': bmi_info,
            'bfp_info': bfp_info,
            'whr_info': whr_info,
            'daily_calories': round(daily_calories),
            'weight_range': weight_range,
            'workout_plan': workout_plan,
            'nutrition_tips': nutrition_tips,
            'exercise_recommendations': exercise_recommendations,
            'execution_time_seconds': round(execution_time, 4)
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input parameters'}), 400

# Helper functions
def calculate_bmi(weight, height):
    return weight / pow(height, 2)

def calculate_bfp_parallel(weight, height, age_range, gender):
    bmi = calculate_bmi(weight, height)
    age_map = {
        '13-18': 15,
        '19-35': 27,
        '36-55': 45,
        '56 and above': 65
    }
    age = age_map.get(age_range, 27)
    return calculate_bfp(bmi, age, gender)

def calculate_whr_parallel(waist, hips, gender):
    whr = float(waist) / float(hips)
    whr_category = get_whr_category(whr, gender)
    return {
        'category': 'Waist-Hip Ratio (WHR)',
        'description': 'Waist-hip ratio is an indicator for evaluating abdominal fat distribution and is closely related to health risks.',
        'formula': 'WHR = Waist Circumference(cm) ÷ Hip Circumference(cm)',
        'ranges': [
            {'gender': 'Male', 'healthy': '< 0.90', 'high_risk': '≥ 0.95'},
            {'gender': 'Female', 'healthy': '< 0.85', 'high_risk': '≥ 0.90'}
        ],
        'result': f'{round(whr, 2)} - {whr_category}',
        'note': 'A higher waist-hip ratio indicates a greater risk of cardiovascular disease and metabolic syndrome.',
        'gender': gender
    }

def calculate_daily_calories_parallel(weight, height, age_range, gender, activity_level):
    age_map = {
        '13-18': 15,
        '19-35': 27,
        '36-55': 45,
        '56 and above': 65
    }
    age = age_map.get(age_range, 27)
    return calculate_daily_calories(weight, height, age, gender, activity_level)

def generate_workout_plan(rec_future, level):
    fitness_recommendations = rec_future.result()
    workout_days = ['Monday', 'Wednesday', 'Friday'] if level == 'Low' else \
                  ['Monday', 'Tuesday', 'Thursday', 'Friday'] if level == 'Medium' else \
                  ['Monday', 'Tuesday', 'Thursday', 'Friday', 'Saturday']
    
    workout_plan = []
    for day in workout_days:
        exercises = ', '.join(fitness_recommendations)
        duration = '30-45 minutes' if level == 'Low' else \
                  '45-60 minutes' if level == 'Medium' else \
                  '60-90 minutes'
        workout_plan.append({
            'day': day,
            'exercises': exercises,
            'duration': duration
        })
    return workout_plan

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    elif bmi < 35:
        return 'Obesity (Grade I)'
    elif bmi < 40:
        return 'Obesity (Grade II)'
    else:
        return 'Obesity (Grade III)'

def calculate_bfp(bmi, age, gender):
    if gender == 'Male':
        return (1.20 * bmi) + (0.23 * age) - 16.2
    else:  # Female
        return (1.20 * bmi) + (0.23 * age) - 5.4

def get_bfp_category(bfp, gender):
    if gender == 'Male':
        if bfp <= 20:
            return 'Healthy'
        elif bfp <= 25:
            return 'Overweight'
        else:
            return 'Obese'
    else:  # Female
        if bfp <= 30:
            return 'Healthy'
        elif bfp <= 35:
            return 'Overweight'
        else:
            return 'Obese'

def get_whr_category(whr, gender):
    if gender == 'Male':
        if whr < 0.90:
            return 'Healthy'
        elif whr < 0.95:
            return 'Moderate Risk'
        else:
            return 'High Risk'
    else:  # Female
        if whr < 0.85:
            return 'Healthy'
        elif whr < 0.90:
            return 'Moderate Risk'
        else:
            return 'High Risk'

def generate_recommendations(age_range, level, goal, bmi_category, bfp_category):
    base_recommendations = {
        '13-18': {
            'Low': {
                'Muscle Gain': ['Basic Push-ups', 'Assisted Pull-ups', 'Bodyweight Squats'],
                'Fat Loss': ['Brisk Walking', 'Swimming', 'Low-intensity Cardio'],
                'Body Shaping': ['Basic Yoga', 'Light Stretching', 'Plank Hold'],
                'Improve Flexibility': ['Basic Stretching', 'Simple Yoga', 'Joint Mobility'],
                'Improve Endurance': ['Jogging', 'Swimming', 'Cycling']
            },
            'Medium': {
                'Muscle Gain': ['Standard Push-ups', 'Weighted Squats', 'Assisted Pull-up Training'],
                'Fat Loss': ['Interval Running', 'Basic HIIT', 'Jump Rope'],
                'Body Shaping': ['Dumbbell Training', 'Resistance Band Training', 'Core Training'],
                'Improve Flexibility': ['Intermediate Yoga', 'Dynamic Stretching', 'PNF Stretching'],
                'Improve Endurance': ['5km Run', 'Swimming', 'Cycling']
            },
            'High': {
                'Muscle Gain': ['Pull-ups', 'Barbell Bench Press', 'Deadlifts'],
                'Fat Loss': ['HIIT', 'Circuit Training', 'Combined Cardio'],
                'Body Shaping': ['Strength Training', 'Superset Training', 'Compound Exercise Training'],
                'Improve Flexibility': ['Advanced Yoga', 'Dance', 'Gymnastics Movements'],
                'Improve Endurance': ['10km Run', 'Triathlon Training', 'Trail Running']
            }
        }
    }
    
    base_recommendations['19-35'] = base_recommendations['13-18']
    base_recommendations['36-55'] = {
        level: {
            goal: [exercise.replace('Run', 'Brisk Walk').replace('Running', 'Walking')
                   if any(x in exercise for x in ['Run', 'Running']) else exercise
                   for exercise in exercises]
            for goal, exercises in goals.items()
        }
        for level, goals in base_recommendations['13-18'].items()
    }
    base_recommendations['56 and above'] = {
        level: {
            goal: [exercise.replace('Run', 'Walk').replace('Running', 'Walking').replace('HIIT', 'Low-intensity Interval')
                   if any(x in exercise for x in ['Run', 'Running', 'HIIT']) else exercise
                   for exercise in exercises]
            for goal, exercises in goals.items()
        }
        for level, goals in base_recommendations['36-55'].items()
    }
    
    recommendations = base_recommendations[age_range][level][goal]
    
    if bmi_category.startswith('Obesity') or bfp_category == 'Obese':
        recommendations = [exercise for exercise in recommendations
                          if not any(x in exercise.lower()
                                    for x in ['run', 'jump', 'weight'])]
        recommendations.extend(['Swimming', 'Elliptical', 'Dynamic Stretching'])
    
    return recommendations[:3]

def calculate_daily_calories(weight, height, age, gender, activity_level):
    if gender == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:  # Female
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    activity_multipliers = {
        'Low': 1.2,
        'Medium': 1.55,
        'High': 1.725
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.2)
    return bmr * multiplier














# from flask import render_template, request, jsonify
# from . import fitness_bp
# from math import pow
# from flask import jsonify, request
# import pandas as pd
# from sk.fitness_model import generate_recommendations as model_generate_recommendations
# import concurrent.futures
# import time

# @fitness_bp.route('/', methods=['GET'])
# def index():
#     return render_template('fitness/index.html')

# @fitness_bp.route('/calculate', methods=['POST'])
# def calculate():
#     start_time = time.time()
    
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400, {'Content-Type': 'application/json'}
    
#     try:
#         data = request.get_json()

#         if not all(key in data for key in ['weight', 'height', 'age', 'gender', 'goal', 'level']):
#             return jsonify({'error': 'Missing required parameters'}), 400
            
#         weight = float(data.get('weight'))
#         height = float(data.get('height')) / 100  # Convert to meters
#         age_range = data.get('age')
#         gender = data.get('gender')
#         goal = data.get('goal')
#         level = data.get('level')
        
#         waist = data.get('waist')
#         hips = data.get('hips')
        
#         # Parallel calculation of BMI and BFP
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             bmi_future = executor.submit(calculate_bmi, weight, height)
#             bfp_future = executor.submit(calculate_bfp_parallel, weight, height, age_range, gender)
            
#             bmi = bmi_future.result()
#             bfp = bfp_future.result()
            
#             bmi_category = get_bmi_category(bmi)
#             bfp_category = get_bfp_category(bfp, gender)
        
#         # BMI result information
#         bmi_info = {
#             'category': 'BMI (Body Mass Index)',
#             'description': 'BMI is a common indicator used to assess the relationship between weight and height, providing an initial assessment of whether weight is healthy.',
#             'formula': 'BMI = Weight(kg) ÷ Height(m)²',
#             'ranges': [
#                 {'range': '< 18.5', 'category': 'Underweight'},
#                 {'range': '18.5 - 24.9', 'category': 'Normal'},
#                 {'range': '25.0 - 29.9', 'category': 'Overweight'},
#                 {'range': '30.0 - 34.9', 'category': 'Obesity (Grade I)'},
#                 {'range': '35.0 - 39.9', 'category': 'Obesity (Grade II)'},
#                 {'range': '≥ 40.0', 'category': 'Obesity (Grade III)'},
#             ],
#             'result': f'{round(bmi, 1)} - {bmi_category}',
#             'note': 'BMI is applicable to most adults but not suitable for children, pregnant women, and certain special populations.',
#             'gender': gender
#         }
        
#         # Body fat percentage result information
#         bfp_info = {
#             'category': 'Body Fat Percentage (BFP)',
#             'description': 'Body fat percentage reflects the proportion of body fat to total weight and is an important indicator for assessing body composition.',
#             'formula': 'Male: (1.20 × BMI) + (0.23 × Age) - 16.2\nFemale: (1.20 × BMI) + (0.23 × Age) - 5.4',
#             'ranges': [
#                 {'gender': 'Male', 'healthy': '10-20%', 'overweight': '20-25%', 'obese': '> 25%'},
#                 {'gender': 'Female', 'healthy': '20-30%', 'overweight': '30-35%', 'obese': '> 35%'}
#             ],
#             'result': f'{round(bfp, 1)}% - {bfp_category}',
#             'note': 'Body fat percentage can also be measured using body fat scales or professional equipment, which may be more accurate than calculated results.',
#             'gender': gender
#         }
        
#         # Parallel calculation of WHR and daily calories
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             whr_future = executor.submit(calculate_whr_parallel, waist, hips, gender) if waist and hips else None
#             calories_future = executor.submit(calculate_daily_calories_parallel, weight, height * 100, age_range, gender, level)
            
#             whr_info = whr_future.result() if whr_future else None
#             daily_calories = calories_future.result()
        
#         height_in_meters = height
#         weight_range = {
#             'min': round(18.5 * (height_in_meters ** 2), 1),
#             'max': round(24.9 * (height_in_meters ** 2), 1)
#         }
        
#         # Generate fitness recommendations in parallel with workout plan
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             rec_future = executor.submit(generate_recommendations, age_range, level, goal, bmi_category, bfp_category)
#             workout_future = executor.submit(generate_workout_plan, rec_future, level)
            
#             fitness_recommendations = rec_future.result()
#             workout_plan = workout_future.result()
        
#         # Generate nutritional recommendations
#         nutrition_tips = [
#             f"Daily Calorie Requirement: {round(daily_calories)} calories",
#             f"Recommended Weight Range: {weight_range['min']}-{weight_range['max']} kg",
#             "Maintain adequate protein intake, 1.6-2.2g per kg of body weight",
#             "Ensure sufficient carbohydrate intake for energy",
#             "Supplement with essential vitamins and minerals"
#         ]
        
#         # Prepare user data for model recommendations
#         user_data = {
#             'age': age_range,
#             'gender': gender,
#             'bmi': bmi,
#             'body_fat_percentage': bfp,
#             'activity_level': level,
#             'goal': goal
#         }
        
#         try:
#             # Get personalized exercise recommendations
#             exercise_recommendations = model_generate_recommendations(user_data)
#         except ValueError as e:
#             return jsonify({'error': str(e)}), 400
#         except Exception as e:
#             return jsonify({'error': 'Failed to generate exercise recommendations'}), 500
        
#         end_time = time.time()
#         execution_time = end_time - start_time
        
#         return jsonify({
#             'bmi_info': bmi_info,
#             'bfp_info': bfp_info,
#             'whr_info': whr_info,
#             'daily_calories': round(daily_calories),
#             'weight_range': weight_range,
#             'workout_plan': workout_plan,
#             'nutrition_tips': nutrition_tips,
#             'exercise_recommendations': exercise_recommendations,
#             'execution_time_seconds': round(execution_time, 4)
#         })
        
#     except (ValueError, TypeError) as e:
#         return jsonify({'error': 'Invalid input parameters'}), 400

# # Parallel calculation functions
# def calculate_bmi(weight, height):
#     return weight / pow(height, 2)

# def calculate_bfp_parallel(weight, height, age_range, gender):
#     bmi = calculate_bmi(weight, height)
#     age_map = {
#         '13-18': 15,
#         '19-35': 27,
#         '36-55': 45,
#         '56 and above': 65
#     }
#     age = age_map.get(age_range, 27)
#     return calculate_bfp(bmi, age, gender)

# def calculate_whr_parallel(waist, hips, gender):
#     whr = float(waist) / float(hips)
#     whr_category = get_whr_category(whr, gender)
#     return {
#         'category': 'Waist-Hip Ratio (WHR)',
#         'description': 'Waist-hip ratio is an indicator for evaluating abdominal fat distribution and is closely related to health risks.',
#         'formula': 'WHR = Waist Circumference(cm) ÷ Hip Circumference(cm)',
#         'ranges': [
#             {'gender': 'Male', 'healthy': '< 0.90', 'high_risk': '≥ 0.95'},
#             {'gender': 'Female', 'healthy': '< 0.85', 'high_risk': '≥ 0.90'}
#         ],
#         'result': f'{round(whr, 2)} - {whr_category}',
#         'note': 'A higher waist-hip ratio indicates a greater risk of cardiovascular disease and metabolic syndrome.',
#         'gender': gender
#     }

# def calculate_daily_calories_parallel(weight, height, age_range, gender, activity_level):
#     age_map = {
#         '13-18': 15,
#         '19-35': 27,
#         '36-55': 45,
#         '56 and above': 65
#     }
#     age = age_map.get(age_range, 27)
#     return calculate_daily_calories(weight, height, age, gender, activity_level)

# def generate_workout_plan(rec_future, level):
#     fitness_recommendations = rec_future.result()
#     workout_days = ['Monday', 'Wednesday', 'Friday'] if level == 'Low' else \
#                   ['Monday', 'Tuesday', 'Thursday', 'Friday'] if level == 'Medium' else \
#                   ['Monday', 'Tuesday', 'Thursday', 'Friday', 'Saturday']
    
#     workout_plan = []
#     for day in workout_days:
#         exercises = ', '.join(fitness_recommendations)
#         duration = '30-45 minutes' if level == 'Low' else \
#                   '45-60 minutes' if level == 'Medium' else \
#                   '60-90 minutes'
#         workout_plan.append({
#             'day': day,
#             'exercises': exercises,
#             'duration': duration
#         })
#     return workout_plan

# # Original helper functions remain the same
# def get_bmi_category(bmi):
#     if bmi < 18.5:
#         return 'Underweight'
#     elif bmi < 25:
#         return 'Normal'
#     elif bmi < 30:
#         return 'Overweight'
#     elif bmi < 35:
#         return 'Obesity (Grade I)'
#     elif bmi < 40:
#         return 'Obesity (Grade II)'
#     else:
#         return 'Obesity (Grade III)'

# def calculate_bfp(bmi, age, gender):
#     if gender == 'Male':
#         return (1.20 * bmi) + (0.23 * age) - 16.2
#     else:  # Female
#         return (1.20 * bmi) + (0.23 * age) - 5.4

# def get_bfp_category(bfp, gender):
#     if gender == 'Male':
#         if bfp <= 20:
#             return 'Healthy'
#         elif bfp <= 25:
#             return 'Overweight'
#         else:
#             return 'Obese'
#     else:  # Female
#         if bfp <= 30:
#             return 'Healthy'
#         elif bfp <= 35:
#             return 'Overweight'
#         else:
#             return 'Obese'

# def get_whr_category(whr, gender):
#     if gender == 'Male':
#         if whr < 0.90:
#             return 'Healthy'
#         elif whr < 0.95:
#             return 'Moderate Risk'
#         else:
#             return 'High Risk'
#     else:  # Female
#         if whr < 0.85:
#             return 'Healthy'
#         elif whr < 0.90:
#             return 'Moderate Risk'
#         else:
#             return 'High Risk'

# def generate_recommendations(age_range, level, goal, bmi_category, bfp_category):
#     base_recommendations = {
#         '13-18': {
#             'Low': {
#                 'Muscle Gain': ['Basic Push-ups', 'Assisted Pull-ups', 'Bodyweight Squats'],
#                 'Fat Loss': ['Brisk Walking', 'Swimming', 'Low-intensity Cardio'],
#                 'Body Shaping': ['Basic Yoga', 'Light Stretching', 'Plank Hold'],
#                 'Improve Flexibility': ['Basic Stretching', 'Simple Yoga', 'Joint Mobility'],
#                 'Improve Endurance': ['Jogging', 'Swimming', 'Cycling']
#             },
#             'Medium': {
#                 'Muscle Gain': ['Standard Push-ups', 'Weighted Squats', 'Assisted Pull-up Training'],
#                 'Fat Loss': ['Interval Running', 'Basic HIIT', 'Jump Rope'],
#                 'Body Shaping': ['Dumbbell Training', 'Resistance Band Training', 'Core Training'],
#                 'Improve Flexibility': ['Intermediate Yoga', 'Dynamic Stretching', 'PNF Stretching'],
#                 'Improve Endurance': ['5km Run', 'Swimming', 'Cycling']
#             },
#             'High': {
#                 'Muscle Gain': ['Pull-ups', 'Barbell Bench Press', 'Deadlifts'],
#                 'Fat Loss': ['HIIT', 'Circuit Training', 'Combined Cardio'],
#                 'Body Shaping': ['Strength Training', 'Superset Training', 'Compound Exercise Training'],
#                 'Improve Flexibility': ['Advanced Yoga', 'Dance', 'Gymnastics Movements'],
#                 'Improve Endurance': ['10km Run', 'Triathlon Training', 'Trail Running']
#             }
#         }
#     }
    
#     base_recommendations['19-35'] = base_recommendations['13-18']
#     base_recommendations['36-55'] = {
#         level: {
#             goal: [exercise.replace('Run', 'Brisk Walk').replace('Running', 'Walking')
#                   if any(x in exercise for x in ['Run', 'Running']) else exercise
#                   for exercise in exercises]
#             for goal, exercises in goals.items()
#         }
#         for level, goals in base_recommendations['13-18'].items()
#     }
#     base_recommendations['56 and above'] = {
#         level: {
#             goal: [exercise.replace('Run', 'Walk').replace('Running', 'Walking').replace('HIIT', 'Low-intensity Interval')
#                   if any(x in exercise for x in ['Run', 'Running', 'HIIT']) else exercise
#                   for exercise in exercises]
#             for goal, exercises in goals.items()
#         }
#         for level, goals in base_recommendations['36-55'].items()
#     }
    
#     recommendations = base_recommendations[age_range][level][goal]
    
#     if bmi_category.startswith('Obesity') or bfp_category == 'Obese':
#         recommendations = [exercise for exercise in recommendations
#                           if not any(x in exercise.lower()
#                                     for x in ['run', 'jump', 'weight'])]
#         recommendations.extend(['Swimming', 'Elliptical', 'Dynamic Stretching'])
    
#     return recommendations[:3]

# def calculate_daily_calories(weight, height, age, gender, activity_level):
#     if gender == 'Male':
#         bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
#     else:  # Female
#         bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
#     activity_multipliers = {
#         'Low': 1.2,
#         'Medium': 1.55,
#         'High': 1.725
#     }
    
#     multiplier = activity_multipliers.get(activity_level, 1.2)
#     return bmr * multiplier


