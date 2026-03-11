import pandas as pd
import tensorflow as tf
import flwr as fl

data = pd.read_csv('/Users/apple/Downloads/client2_data.csv')

data['length'] = pd.to_numeric(data['length'], errors='coerce')
data = data.dropna(subset=['length'])

numeric_data = data.select_dtypes(include=['number'])
x_train = numeric_data.drop(columns=['length']).values.astype('float32')
y_train = numeric_data['length'].values.astype('float32')
from sklearn.preprocessing import StandardScaler

# Standardize the data
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)

class Client(fl.client.NumPyClient):
    def __init__(self, model, x_train, y_train):
        self.model = model
        self.x_train = x_train
        self.y_train = y_train

    def get_parameters(self, config):
        # Log the parameters before sending them to the server
        parameters = self.model.get_weights()
        print("Sending parameters to the server:")
        print(parameters)
        return parameters

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=5, batch_size=32, verbose=0)
        # Log the parameters after training
        trained_parameters = self.model.get_weights()
        print("Trained parameters after fitting:")
        print(trained_parameters)
        return trained_parameters, len(self.x_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, mae = self.model.evaluate(self.x_train, self.y_train, verbose=0)
        # Log the evaluation parameters and results
        print(f"Evaluation results: Loss = {loss}, MAE = {mae}")
        return loss, len(self.x_train), {"mae": mae}
    
def create_model(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(input_shape,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

if __name__ == "__main__":
    model = create_model(x_train.shape[1])
    client = Client(model, x_train, y_train)
    fl.client.start_client(server_address="localhost:8080", client=client)
