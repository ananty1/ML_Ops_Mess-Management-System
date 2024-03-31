import pandas as pd

def morning(row):
    return (row.time() > pd.Timestamp('07:00:00').time())& (row.time() < pd.Timestamp('11:00:00').time())
def afternoon(row):
    return (row.time() > pd.Timestamp('12:00:00').time()) & (row.time() < pd.Timestamp('15:30:00').time())
def snacksTime(row):
    return (row.time() > pd.Timestamp('16:00:00').time()) & (row.time() < pd.Timestamp('18:40:00').time())

def evening(row):
    return (row.time() > pd.Timestamp('19:30:00').time()) & (row.time() < pd.Timestamp('23:00:00').time())
def addFoodDetails(df):

    if df['remarks']=='Basic':
        if afternoon(df['transaction_date']):
            if df['day_name']=='Monday':
                df['Food']='Mix Veg dry'
            elif df['day_name']=='Tuesday':
                df['Food']='Chole Masala'
            elif df['day_name']=='Wednesday':
                df['Food']='Loki Chana'
            elif df['day_name']=='Thursday':
                df['Food']='Palak Tomato'
            elif df['day_name']=='Friday':
                df['Food']='Rajma'
            elif df['day_name']=='Saturday':
                df['Food']='Choley(kabuli chana)'
            elif df['day_name']=='Sunday':
                df['Food']='Gatte Sabji'
        
        if evening(df['transaction_date']):
            if df['day_name']=='Monday':
                df['Food']='Brinjal Bartha'
            elif df['day_name']=='Tuesday':
                df['Food']='Aloo gobhi mattr'
            elif df['day_name']=='Wednesday':
                df['Food']='Veg kofta'
            elif df['day_name']=='Thursday':
                df['Food']='Aloo Sem'
            elif df['day_name']=='Friday':
                df['Food']='Carrot Peas'
            elif df['day_name']=='Saturday':
                df['Food']='Mix Veg'
            elif df['day_name']=='Sunday':
                df['Food']='Veg Manchurian'
            
    elif df['remarks']=='Add-On':
        if df['mess']=='mess-galav':
            # add on in galav mess
            if morning(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Aloo puri-Boiled egg'
                elif df['day_name']=='Tuesday':
                    df['Food']='Masala Dosa-Omlette'
                elif df['day_name']=='Wednesday':
                    df['Food']='Aloo Paratha-Bhurji'
                elif df['day_name']=='Thursday':
                    df['Food']='Uttapam-Omlette'
                elif df['day_name']=='Friday':
                    df['Food']='Gobi Paratha-Bhurji'
                elif df['day_name']=='Saturday':
                    df['Food']='Idly-Boiled egg'
                elif df['day_name']=='Sunday':
                    df['Food']='Rawa Dosa-Bhurji'


            if afternoon(df['transaction_date']):
                
                if df['day_name']=='Monday':
                    
                    df['Food']='Chicken Curry'
                    
                elif df['day_name']=='Tuesday':
                    df['Food']='Chicken Fried Rice'
                elif df['day_name']=='Wednesday':
                    df['Food']='Chilli Chicken'
                elif df['day_name']=='Thursday':
                    df['Food']='Egg Curry'
                elif df['day_name']=='Friday':
                    df['Food']='Chicken Biryani'
                elif df['day_name']=='Saturday':
                    df['Food']='Egg Curry'
                elif df['day_name']=='Sunday':
                    df['Food']='Chicken Curry'

            if snacksTime(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Dahi Kachori'
                elif df['day_name']=='Tuesday':
                    df['Food']='Pav Bhaji'
                elif df['day_name']=='Wednesday':
                    df['Food']='Veg Roll'
                elif df['day_name']=='Thursday':
                    df['Food']='Veg Cutlet'
                elif df['day_name']=='Friday':
                    df['Food']='Panni Puri'
                elif df['day_name']=='Saturday':
                    df['Food']='Bread Pakoda'
                elif df['day_name']=='Sunday':
                    df['Food']='Samosa'
            
            if evening(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Egg Curry'
                elif df['day_name']=='Tuesday':
                    df['Food']='Chicken Curry'
                elif df['day_name']=='Wednesday':
                    df['Food']='Veg Biryani'
                elif df['day_name']=='Thursday':
                    df['Food']='Fish Curry'
                elif df['day_name']=='Friday':
                    df['Food']='Fried Chicken'
                elif df['day_name']=='Saturday':
                    df['Food']='Fish Curry'
                elif df['day_name']=='Sunday':
                    df['Food']='Chilli Chicken'
        
        if df['mess']=='mess-kumard':
            # add on in galav mess
            if morning(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Aloo puri-CornFlakes Milk'
                elif df['day_name']=='Tuesday':
                    df['Food']='Masala Dosa--CornFlakes Milk'
                elif df['day_name']=='Wednesday':
                    df['Food']='Aloo Paratha-CornFlakes Milk'
                elif df['day_name']=='Thursday':
                    df['Food']='Uttapam-CornFlakes Milk'
                elif df['day_name']=='Friday':
                    df['Food']='Gobi Paratha-CornFlakes Milk'
                elif df['day_name']=='Saturday':
                    df['Food']='Idly--CornFlakes Milk'
                elif df['day_name']=='Sunday':
                    df['Food']='Rawa Dosa-CornFlakes Milk'


            if afternoon(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Butter Paneer Masala'
                elif df['day_name']=='Tuesday':
                    df['Food']='Mutter Paneer'
                elif df['day_name']=='Wednesday':
                    df['Food']='Shahi Paneer'
                elif df['day_name']=='Thursday':
                    df['Food']='Palak Paneer'
                elif df['day_name']=='Friday':
                    df['Food']='Veg Biryani'
                elif df['day_name']=='Saturday':
                    df['Food']='Paneer Chilli'
                elif df['day_name']=='Sunday':
                    df['Food']='Palak Paneer'

            if snacksTime(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Dahi Kachori'
                elif df['day_name']=='Tuesday':
                    df['Food']='Pav Bhaji'
                elif df['day_name']=='Wednesday':
                    df['Food']='Veg Roll'
                elif df['day_name']=='Thursday':
                    df['Food']='Veg Cutlet'
                elif df['day_name']=='Friday':
                    df['Food']='Panni Puri'
                elif df['day_name']=='Saturday':
                    df['Food']='Bread Pakoda'
                elif df['day_name']=='Sunday':
                    df['Food']='Samosa'
            
            if evening(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Kadhai Paneer'
                elif df['day_name']=='Tuesday':
                    df['Food']='Veg Biryani'
                elif df['day_name']=='Wednesday':
                    df['Food']='Kadhai Paneer'
                elif df['day_name']=='Thursday':
                    df['Food']='Paneer Chilli'
                elif df['day_name']=='Friday':
                    df['Food']='Shahi Paneer'
                elif df['day_name']=='Saturday':
                    df['Food']='Butter Paneer Masala'
                elif df['day_name']=='Sunday':
                    df['Food']='Paneer Chilli'


        if df['mess']=='mess-ssai':

            # add on in galav mess
            if morning(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Aloo puri-Boiled egg'
                elif df['day_name']=='Tuesday':
                    df['Food']='Masala Dosa-Omlette'
                elif df['day_name']=='Wednesday':
                    df['Food']='Aloo Paratha-Bhurji'
                elif df['day_name']=='Thursday':
                    df['Food']='Uttapam-Omlette'
                elif df['day_name']=='Friday':
                    df['Food']='Gobi Paratha-Bhurji'
                elif df['day_name']=='Saturday':
                    df['Food']='Idly-Boiled egg'
                elif df['day_name']=='Sunday':
                    df['Food']='Rawa Dosa-Bhurji'

            if afternoon(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Chicken Curry'
                elif df['day_name']=='Tuesday':
                    df['Food']='Chicken Fried Rice'
                elif df['day_name']=='Wednesday':
                    df['Food']='Chilli Chicken'
                elif df['day_name']=='Thursday':
                    df['Food']='Egg Curry'
                elif df['day_name']=='Friday':
                    df['Food']='Chicken Biryani'
                elif df['day_name']=='Saturday':
                    df['Food']='Egg Curry'
                elif df['day_name']=='Sunday':
                    df['Food']='Chicken Curry'

            if snacksTime(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Dahi Kachori'
                elif df['day_name']=='Tuesday':
                    df['Food']='Pav Bhaji'
                elif df['day_name']=='Wednesday':
                    df['Food']='Veg Roll'
                elif df['day_name']=='Thursday':
                    df['Food']='Veg Cutlet'
                elif df['day_name']=='Friday':
                    df['Food']='Panni Puri'
                elif df['day_name']=='Saturday':
                    df['Food']='Pasta'
                elif df['day_name']=='Sunday':
                    df['Food']='Sandwich'
            
            if evening(df['transaction_date']):
                if df['day_name']=='Monday':
                    df['Food']='Egg Curry'
                elif df['day_name']=='Tuesday':
                    df['Food']='Chicken Curry'
                elif df['day_name']=='Wednesday':
                    df['Food']='Chicken Biryani'
                elif df['day_name']=='Thursday':
                    df['Food']='Fish Curry'
                elif df['day_name']=='Friday':
                    df['Food']='Fried Chicken'
                elif df['day_name']=='Saturday':
                    df['Food']='Fish Curry'
                elif df['day_name']=='Sunday':
                    df['Food']='Chilli Chicken'
    return df
