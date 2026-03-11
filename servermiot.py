import flwr as fl

# Define a custom strategy to log parameters
class CustomFedAvg(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd, results, failures):
        # Log the aggregated parameters from the clients
        aggregated_parameters = super().aggregate_fit(rnd, results, failures)
        print(f"Aggregated parameters after round {rnd}: {aggregated_parameters}")
        return aggregated_parameters

    def aggregate_evaluate(self, rnd, results, failures):
        # Log the evaluation results
        print(f"Evaluation results after round {rnd}: {results}")
        return super().aggregate_evaluate(rnd, results, failures)

def start_server():
    # Use CustomFedAvg strategy to include logging
    strategy = CustomFedAvg()
    fl.server.start_server(server_address="localhost:8080", strategy=strategy)

if __name__ == "__main__":
    start_server()
