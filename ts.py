import flwr as fl
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Define the model architecture
def create_model(input_shape):
    model = Sequential([
        tf.keras.layers.Input(shape=(input_shape,)),
        tf.keras.layers.Dense(128, activation='relu', kernel_initializer='he_normal'),
        tf.keras.layers.Dense(64, activation='relu', kernel_initializer='he_normal'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer=Adam(learning_rate=1e-4), loss='mean_squared_error', metrics=['mae'])
    return model

# Create and compile the model
input_shape = 7  # Adjust according to your input shape
model = create_model(input_shape)

# Server-side training function
def server_train(model, dataset):
    # Assuming dataset is preprocessed and ready for training
    # Split into features (X) and target (y)
    X = dataset.drop(columns='length')  # Replace 'target_column' with actual column name
    y = dataset['length']
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the model on the merged dataset
    model.fit(X_scaled, y, epochs=10, batch_size=32)
    return model

# Flower strategy: Federated Averaging
# class MyFedAvg(fl.server.strategy.FedAvg):
#     def aggregate_fit(self, server_round, results, failures):
#         # Perform federated averaging
#         aggregated_weights = super().aggregate_fit(server_round, results, failures)
        
#         # Optionally, load merged dataset model weights and use them for aggregation
#         # For example, you can load pre-trained weights here if necessary
#         # model.set_weights(aggregated_weights)
        
#         return aggregated_weights
class MyFedAvg(fl.server.strategy.FedAvg):
    def aggregate_fit(self, server_round, results, failures):
        # Perform federated averaging
        aggregated_weights = super().aggregate_fit(server_round, results, failures)

        # Load aggregated weights into the server model
        if aggregated_weights is not None:
            model.set_weights(aggregated_weights)

            # Evaluate the aggregated model on the merged dataset
            merged_data = pd.read_csv('/Users/apple/adjusted_data2.csv')
            X = merged_data.drop(columns='length')
            y = merged_data['length']
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            loss, mae = model.evaluate(X_scaled, y, verbose=0)

            print(f"Round {server_round}: Loss = {loss:.4f}, MAE = {mae:.4f}")
        
        return aggregated_weights

# Start the server
def start_server():
    # Load your merged dataset (update the path to your actual merged dataset)
    merged_data = pd.read_csv('/Users/apple/adjusted_data2.csv')
    
    # Create a model (or load an existing model)
    model = create_model(input_shape=merged_data.shape[1] - 1)  # Input shape depends on your dataset
    
    # Train the model on the full merged dataset
    model = server_train(model, merged_data)
    
    # Define the strategy without 'min_eval_clients'
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=0.1,  # Percentage of clients used in each round
        min_fit_clients=1,  # Minimum number of clients for fitting
        min_available_clients=1,  # Minimum number of clients available to start the rounds
    )

    # Create a server config in1tance with 'num_rounds'
    server_config = fl.server.ServerConfig(num_rounds=5)
    
    # Start the server
    fl.server.start_server(
        server_address="localhost:8080",
        config=server_config,  # Use the ServerConfig object here
        strategy=strategy,
    )

if __name__ == "__main__":
    start_server()
