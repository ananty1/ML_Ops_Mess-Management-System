from metaflow import FlowSpec, step
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import plotly.io as pio
from addTime import addFoodDetails

class HelloFlow(FlowSpec):
    filepath = 'card_transaction.csv'

    @step
    def start(self):
        """
        This is the 'start' step. All flows must have a step named 'start' that
        is the first step in the flow.

        """
        print("HelloFlow is starting.")
        self.next(self.load_dataset)

    @step
    def load_dataset(self):
        """
        A step for metaflow to introduce itself.

        """
        self.dataset = pd.read_csv(self.filepath)
        self.next(self.data_summary)

    @step
    def data_summary(self):
        print("Shape of the dataset:", self.dataset.shape)
        print("Sample records from the dataset:")
        print(self.dataset.sample(3))
        self.num_iitbh_transactions = (self.dataset['account_to'] == 'IITBH').sum()
        self.next(self.filter_recharge_transactions)

    @step
    def filter_recharge_transactions(self):
        self.df = self.dataset[self.dataset['remarks'] != 'Recharge']
        self.next(self.handle_dates)

    @step
    def handle_dates(self):
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'], format='%d-%m-%Y %H:%M')
        self.df['record_date'] = pd.to_datetime(self.df['record_date'], format='%d-%m-%Y %H:%M')
        self.next(self.rename_columns)

    @step
    def rename_columns(self):
        self.df.rename(columns={"account_from": "mess", "account_to": "id_number"}, inplace=True)
        self.next(self.plot_graphs)

    @step
    def plot_graphs(self):
        self.df['remarks'].value_counts().plot(kind='bar')
        plt.savefig('remarks_bar_chart.png')
        self.df['mess'].value_counts().plot(kind='bar')
        plt.savefig('mess_bar_chart.png')
        self.next(self.preprocess_data)


    @step
    def preprocess_data(self):
        self.df['month'] = self.df['transaction_date'].dt.month
        self.df['year'] = self.df['transaction_date'].dt.year
        self.df['date'] = self.df['transaction_date'].dt.date
        self.df['time'] = self.df['transaction_date'].dt.time
        self.next(self.plot_daily_trends)


    @step
    def plot_daily_trends(self):
        daily_data = self.df.groupby(self.df['transaction_date'].dt.date).size().reset_index(name='transactions')
        sns.lineplot(x='transaction_date', y='transactions', data=daily_data, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Number of Transactions')
        plt.title('Daily Transaction Trends')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('daily_transaction_trends.png')
        self.next(self.plot_hourly_trends)  

    @step
    def plot_hourly_trends(self):
        self.df['hour'] = self.df['transaction_date'].dt.hour
        hourly_data = self.df.groupby(['hour', 'mess']).size().reset_index(name='transactions')
        sns.lineplot(x='hour', y='transactions', hue='mess', data=hourly_data, marker='o')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Transactions')
        plt.title('Hourly Transaction Trends with Mess Hue')
        plt.xticks(range(6, 24))
        plt.legend(title='Mess')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('hourly_transaction_trends.png')
        self.next(self.analyze_time_series)
   
    @step
    def analyze_time_series(self):
        self.df['time_24hr'] = self.df['transaction_date'].dt.strftime('%H:%M')
        df_count = self.df.groupby('time_24hr').size().reset_index(name='count')
        fig = px.line(df_count, x='time_24hr', y='count', labels={'time_24hr': 'Time (24-hour format)', 'count': 'Transaction Count'})
        fig.update_layout(title='Transaction Count per Minute Interval (24-hour format)', xaxis_title='Time (24-hour format)', yaxis_title='Transaction Count')
        fig.update_traces(marker=dict(color='blue', line=dict(color='black', width=1)))
        pio.write_html(fig, 'transaction_count.html')
        self.next(self.add_week_days)

    @step 
    def add_week_days(self):
        # Extract day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        self.df['day_of_week'] = self.df['transaction_date'].dt.dayofweek

        # Define a mapping for day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Map day of the week integers to day names
        self.df['day_name'] = self.df['day_of_week'].map(lambda x: day_names[x])
        self.next(self.weekly_plot)
        
    @step 
    def weekly_plot(self):
        daily_hourly_data = self.df.groupby(['day_name', 'mess', self.df['transaction_date'].dt.hour]).size().reset_index(name='transactions')
        # Plot the data using Seaborn with hue='day_name' and x='hour'
        plt.figure(figsize=(12, 8))
        sns.lineplot(x='transaction_date', y='transactions', hue='day_name', data=daily_hourly_data, marker='o')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Transactions')
        plt.title('Hourly Transaction Trends by Day of the Week with Mess Hue')
        plt.xticks(range(5,24))  # Set x-axis ticks to represent hours of the day (0-23)
        plt.legend(title='Day of the Week')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('Weekly_hourly_transaction_trends.png')

        self.next(self.mess_hue_weekly_plot)

    @step
    def mess_hue_weekly_plot(self):
        hourly_data = self.df.groupby(['hour', 'mess']).size().reset_index(name='transactions')

        # Plot the data using Seaborn with hue='mess' and x='hour'
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='hour', y='transactions', hue='mess', data=hourly_data, marker='o')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Transactions')
        plt.title('Hourly Transaction Trends with Mess Hue')
        plt.xticks(range(24))  # Set x-axis ticks to represent hours of the day (0-23)
        plt.legend(title='Mess')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('Hourly_Transaction_Trends_with_Mess_wise.png')

        self.next(self.plot_minute_histogram)
    
    @step
    def plot_minute_histogram(self):
        # Extract hour and minute components
        hour_minute = self.df['transaction_date'].dt.hour * 60 + self.df['transaction_date'].dt.minute

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.hist(hour_minute, bins=24 * 60, edgecolor='black')  # Create minute-level bins
        plt.xlabel('Hour-Minute Intervals')
        plt.ylabel('Frequency')
        plt.title('Minute Interval Histogram')
        plt.xticks(range(0, 24 * 60, 60), [f'{h:02d}:00' for h in range(24)])  # Label x-axis with hour intervals
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('Minute Interval Histogram.png')

        self.next(self.split_basic_add_on)
    
    @step 
    def split_basic_add_on(self):
        addOn = self.df[self.df['remarks']=='Basic-AddOn'].copy()
        addOn['remarks']='Add-On'
        self.df['remarks'] = self.df['remarks'].apply(lambda x: 'Basic' if x == 'Basic-AddOn' else x)
        self.df = pd.concat([addOn,self.df])
        
        self.next(self.add_food_details)

            
    @step 
    def add_food_details(self):
        self.df['Food'] = self.df['mess']
        for index, row in self.df.iterrows():
            updated_row = addFoodDetails(row)
            self.df.at[index, 'Food'] = updated_row['Food']

        self.next(self.bar_plot_food_pattern)
    
    @step
    def bar_plot_food_pattern(self):
        self.df['Food'].value_counts().plot(kind='bar',figsize=(10,8))
        plt.xlabel('Food Items')
        plt.ylabel('Count')
        plt.title('Count of Food Items')
        plt.savefig('Food_Consumption_Count.jpg')

        self.next(self.save_heatmap_plot)
    
    @step 
    def save_heatmap_plot(self):
        day_Wise_Food = self.df[['mess','day_name','Food']]
        # Create a pivot table
        pivot_df = pd.pivot_table(day_Wise_Food, index='Food', columns='day_name', aggfunc='size', fill_value=0)
        # print(pivot_df)
        # Create the heatmap
        plt.figure(figsize=(20, 10))
        sns.heatmap(pivot_df, cmap='viridis', annot=True, fmt='d')
        plt.xlabel('Food Items')
        plt.ylabel('Days of the Week')
        plt.title('Count of Food Items by Day of the Week')
        plt.savefig("Weekly_food_consumption_patter.png")

    

        self.next(self.show_df)
    
    @step
    def show_df(self):
        print("The dataset shape is",self.df.shape)
        print("How it looks like:")
        print(self.df.head(4))
        self.df.to_csv("Prepared_dataset.csv")
        self.next(self.end)
    
    
        

    


    









    @step
    def end(self):
        ''' This is where we end'''
        print("Metaflow script execution completed.")


if __name__ == "__main__":
    HelloFlow()
