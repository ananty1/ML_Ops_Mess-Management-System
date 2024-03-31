from metaflow import FlowSpec, step, Parameter
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
import numpy as np
import joblib

class LinearRegressionFlow(FlowSpec):

    dataset_file = "Prepared_dataset.csv"

    @step
    def start(self):
        self.dataset = pd.read_csv(self.dataset_file, index_col=0)
        self.next(self.preprocessing)

    @step
    def preprocessing(self):
        self.dataset['transaction_date'] = pd.to_datetime(self.dataset['transaction_date'])
        self.dataset['time_minute'] = self.dataset['transaction_date'].apply(lambda x: x.hour*60+x.minute)
        filter_df = self.dataset[['mess', 'day_name', 'Food', 'time_minute']]
        filter_df = pd.DataFrame(filter_df.groupby(['mess', 'day_name', 'Food', 'time_minute']).size().reset_index(name='footprint'))
        transformed_data, columns = self.transform_data(filter_df)
        self.transformed_df = pd.DataFrame(transformed_data.toarray(), columns=columns)
        print("The df size is ",self.transformed_df.shape)
        self.next(self.train_model)

    def transform_data(self, data):
        ohe = OneHotEncoder(sparse_output=True)
        transform = ColumnTransformer(transformers=[('tnf', ohe, ['mess', 'day_name', 'Food'])], remainder='passthrough')
        transformed_data = transform.fit_transform(data)
        columns = transform.named_transformers_['tnf'].get_feature_names_out(input_features=['mess', 'day_name', 'Food'])
        columns = list(columns)
        columns.append('time_minute')
        columns.append('footprint')
        columns = np.array(columns)
        return transformed_data, columns

    @step
    def train_model(self):
        X =self.transformed_df.drop(columns=['footprint'])
        y = self.transformed_df[['footprint']]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.model = model
        self.y_pred = model.predict(X_test)
        self.rmse = np.sqrt(mean_squared_error(y_test, self.y_pred))
        self.cv_rmse_scores = self.cross_validation_scores(X, y)
        self.next(self.save_model)

    def cross_validation_scores(self, X, y):
        model = LinearRegression()
        cv_scores = cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=5)
        cv_rmse_scores = np.sqrt(-cv_scores)
        return cv_rmse_scores

    @step
    def save_model(self):
        joblib.dump(self.model, 'linear_regression_model.pkl')
        self.next(self.end)

    @step
    def end(self):
        print("Now the model has been saved")

if __name__ == '__main__':
    LinearRegressionFlow()
