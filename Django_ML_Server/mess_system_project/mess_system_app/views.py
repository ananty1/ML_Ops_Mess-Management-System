from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from metaflow import Flow, get_metadata
import json
import pandas as pd
from joblib import load
import os 
from decimal import Decimal
import numpy as np 


def home(request):
	return JsonResponse({'message':"Hello World"})

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        data_dict = {
            'mess_mess-galav': 0.0,
            'mess_mess-kumard': 0.0,
            'mess_mess-ssai': 0.0,
            'day_name_Friday': 0.0,
            'day_name_Monday': 0.0,
            'day_name_Saturday': 0.0,
            'day_name_Sunday': 0.0,
            'day_name_Thursday': 0.0,
            'day_name_Tuesday': 0.0,
            'day_name_Wednesday': 0.0,
            'Food_Aloo Paratha-Bhurji': 0.0,
            'Food_Aloo Paratha-CornFlakes Milk': 0.0,
            'Food_Aloo Sem': 0.0,
            'Food_Aloo gobhi mattr': 0.0,
            'Food_Aloo puri-Boiled egg': 0.0,
            'Food_Aloo puri-CornFlakes Milk': 0.0,
            'Food_Bread Pakoda': 0.0,
            'Food_Brinjal Bartha': 0.0,
            'Food_Butter Paneer Masala': 0.0,
            'Food_Carrot Peas': 0.0,
            'Food_Chicken Biryani': 0.0,
            'Food_Chicken Curry': 0.0,
            'Food_Chicken Fried Rice': 0.0,
            'Food_Chilli Chicken': 0.0,
            'Food_Chole Masala': 0.0,
            'Food_Choley(kabuli chana)': 0.0,
            'Food_Dahi Kachori': 0.0,
            'Food_Egg Curry': 0.0,
            'Food_Fish Curry': 0.0,
            'Food_Fried Chicken': 0.0,
            'Food_Gatte Sabji': 0.0,
            'Food_Gobi Paratha-Bhurji': 0.0,
            'Food_Gobi Paratha-CornFlakes Milk': 0.0,
            'Food_Idly--CornFlakes Milk': 0.0,
            'Food_Idly-Boiled egg': 0.0,
            'Food_Kadhai Paneer': 0.0,
            'Food_Loki Chana': 0.0,
            'Food_Masala Dosa--CornFlakes Milk': 0.0,
            'Food_Masala Dosa-Omlette': 0.0,
            'Food_Mix Veg': 0.0,
            'Food_Mix Veg dry': 0.0,
            'Food_Mutter Paneer': 0.0,
            'Food_Palak Paneer': 0.0,
            'Food_Palak Tomato': 0.0,
            'Food_Paneer Chilli': 0.0,
            'Food_Panni Puri': 0.0,
            'Food_Pasta': 0.0,
            'Food_Pav Bhaji': 0.0,
            'Food_Rajma': 0.0,
            'Food_Rawa Dosa-Bhurji': 0.0,
            'Food_Rawa Dosa-CornFlakes Milk': 0.0,
            'Food_Samosa': 0.0,
            'Food_Sandwich': 0.0,
            'Food_Shahi Paneer': 0.0,
            'Food_Uttapam-CornFlakes Milk': 0.0,
            'Food_Uttapam-Omlette': 0.0,
            'Food_Veg Biryani': 0.0,
            'Food_Veg Cutlet': 0.0,
            'Food_Veg Manchurian': 0.0,
            'Food_Veg Roll': 0.0,
            'Food_Veg kofta': 0.0,
            'time_minute': 0.0
        }
        for key in data.keys():
            data_dict[key] = Decimal(data[key])
        
        # print("Fine till here")
        try:
            model = load("static/mess_system_app/linear_regression_model.pkl")
            # print("Model coeffis",model.coef_)
            prediction = model.predict(np.array(list(data_dict.values())).reshape(1, -1))
            return JsonResponse({'Expected Footprint is:': int(prediction[0])})  # Convert to float for JSON response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Hand
    else:
        return JsonResponse({'error': 'Only POST requests allowed.'}, status=405)


@csrf_exempt
def popular_dishes(request):
    data = json.loads(request.body)
    day_name = data['day_name']
    time_slot = data['time_slot']
    # print(data)
    # print("Current directory ",os.listdir())
    df = pd.read_csv('static/mess_system_app/Day_Wise_MaxDemand.csv',index_col=0)
    # print(day_name,time_slot)
    # print(df.head(2))
    dish = df.loc[(df['day_name'] == day_name) & (df['time_slot'] == time_slot), 'Food'].iloc[0]
    return JsonResponse({"Popular dish":dish})
     
