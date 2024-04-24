from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from metaflow import Flow, get_metadata
import json
import pandas as pd
from joblib import load
import os 
from decimal import Decimal
import numpy as np 
from prophet import Prophet


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
     

def getGraph(request):
    data = json.loads(request.body)
    timestamp = data['timestamp']
    last_5_minute_footprint = data['footprint']
    print(timestamp,last_5_minute_footprint)
    df = pd.read_csv('static/mess_system_app/Galav_Mess_5_Minute_Slot_foot_print.csv',index_col=0)
    # Define the new row data
    # new_row = {'record_date': '2024-04-25 16:00:00', 'footprint': 42}
    # new_row = {'record_date': timestamp, 'footprint': last_5_minute_footprint}

    # # Append the new row to the DataFrame
    # df = df.append(new_row, ignore_index=True)

    # # Save the updated DataFrame back to a CSV file
    # df.to_csv('static/mess_system_app/Galav_Mess_5_Minute_Slot_foot_print.csv', index=False)


    df['ds'] = pd.to_datetime(df['ds'])
    m = Prophet()
    m.fit(df)
    from datetime import datetime, timedelta

    # Get the current timestamp
    current_timestamp = datetime.now()

    # Create a DataFrame with the current timestamp and next 30-minute intervals
    future_dates = pd.DataFrame({
        'ds': pd.date_range(start=current_timestamp, periods=24, freq='5min')
    })

    # Make predictions for the next 30 minutes
    forecast = m.predict(future_dates)

    # Convert Timestamp objects to string format
    forecast['ds'] = forecast['ds'].astype(str)
    # Convert NumPy arrays to lists for JSON serialization
    future_time_stamp = forecast['ds'].tolist()
    future_predictions = forecast['yhat'].tolist()

    # Prepare JSON response
    data = {
        "message": "Forecasting of next two hours at interval of 30 minutes",
        "future_time_stamp": future_time_stamp,
        "footprint_count": future_predictions
    }

    # Convert data to JSON string
    json_data = json.dumps(data)

    
    return JsonResponse(json_data, status=200, safe=False)