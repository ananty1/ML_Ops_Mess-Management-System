from metaflow import FlowSpec, step, Parameter
import pandas as pd

class TimeSlotAnalysisFlow(FlowSpec):
    input_file = Parameter('input_file', default="Prepared_dataset.csv")

    @step
    def start(self):
        self.dataset = pd.read_csv(self.input_file, index_col=0)
        self.next(self.process_data)

    @step
    def process_data(self):
        df = self.dataset[['time_24hr', 'day_name', 'Food']]
        df['time_24hr'] = pd.to_datetime(df['time_24hr'], format='%H:%M')
        morning_slot = pd.to_datetime('07:00', format='%H:%M').time()
        afternoon_slot = pd.to_datetime('12:00', format='%H:%M').time()
        snacks_slot = pd.to_datetime('16:00', format='%H:%M').time()
        evening_dinner_slot = pd.to_datetime('19:30', format='%H:%M').time()

        def categorize_time(time):
            if morning_slot <= time < afternoon_slot:
                return 'Morning'
            elif afternoon_slot <= time < snacks_slot:
                return 'Afternoon'
            elif snacks_slot <= time < evening_dinner_slot:
                return 'Snacks'
            else:
                return 'Evening-Dinner'

        df['time_slot'] = df['time_24hr'].dt.time.apply(categorize_time)
        self.grouped_df = df.groupby(['day_name', 'time_slot', 'Food']).size().reset_index(name='demand')
        self.next(self.find_max_demand)

    @step
    def find_max_demand(self):
        max_demand_df = self.grouped_df.loc[self.grouped_df.groupby(['day_name', 'time_slot'])['demand'].idxmax()]
        max_demand_df.to_csv("Day_Wise_MaxDemand.csv")
        self.next(self.end)

    @step
    def end(self):
        print("Time slot analysis completed.")

if __name__ == '__main__':
    TimeSlotAnalysisFlow()
