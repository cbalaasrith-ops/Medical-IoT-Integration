import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import flwr as fl

# Load dataset
try:
    data = pd.read_csv('/Users/apple/Downloads/final_dataset_2.csv', encoding='ISO-8859-1')
except FileNotFoundError:
    print("Client 1 dataset not found. Ensure the correct path is provided.")
    exit()
except UnicodeDecodeError:
    print("Encoding error in the dataset. Ensure it uses a compatible encoding.")
    exit()

# Check if 'Length' column exists and preprocess
if 'Length' in data.columns:
    data['Length'] = pd.to_numeric(data['Length'], errors='coerce')
else:
    print("Warning: 'Length' column not found. Skipping this column.")

# Preprocess data
try:
    x_train = data.drop(columns=['target']).values  # Replace 'target' with the correct target column name
    y_train = data['target'].values  # Replace 'target' with the correct target column name
except KeyError as e:
    print(f"Column {e} not found in the dataset. Verify the column names.")
    exit()

# Define the model
model = Sequential([
    Dense(32, input_shape=(x_train.shape[1],), activation="relu"),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Define Flower client
class Client1(fl.client.NumPyClient):
    def get_parameters(self):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=2)
        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_train, y_train, verbose=0)
        return loss, len(x_train), {"accuracy": accuracy}

# Start the client
fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=Client1())
