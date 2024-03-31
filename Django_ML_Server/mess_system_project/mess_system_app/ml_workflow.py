from metaflow import FlowSpec, step
import pandas as pd
from sklearn.linear_model import LinearRegression

class MLWorkflow(FlowSpec):
    @step
    def start(self):
        self.data = pd.read_csv('Final_data.csv',index_col=0)
        self.next(self.preprocess_data)

    @step
    def preprocess_data(self):
        # Add preprocessing steps here if needed
        self.X = self.data[['mess_mess-galav', 'mess_mess-kumard', 'mess_mess-ssai',
                            'remarks_Add-On', 'remarks_Basic', 'remarks_Basic-AddOn',
                            'day_of_week', 'time']]
        self.y = self.data['count']
        self.next(self.train_model)

    @step
    def train_model(self):
        self.model = LinearRegression()
        self.model.fit(self.X, self.y)
        self.next(self.end)

    @step
    def end(self):
        self.log("Model trained successfully!")

if __name__ == '__main__':
    MLWorkflow()

