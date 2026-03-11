import flwr as fl

def start_server():
    fl.server.start_server(server_address="localhost:8080", strategy=fl.server.strategy.FedAvg())

if __name__ == "__main__":
    start_server()
