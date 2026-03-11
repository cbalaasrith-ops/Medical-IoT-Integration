# Medical IoT Federated Learning Framework

This project implements a federated learning-based intrusion and anomaly detection system for Medical IoT (MIoT) networks.

Each hospital node trains a model locally on its own network traffic data and sends only model weights to a central server — raw data never leaves the node. The server aggregates these updates into a global intrusion detection model using FedAvg. The project also includes utilities to simulate attack traffic and capture MQTT protocol traces.

---

## Repository Overview

**Core federated learning pipeline (final version)**
- `ts.py` — Flower FL server. Runs 5 federated rounds (`ServerConfig(num_rounds=5)`) and evaluates the aggregated model on a merged dataset
- `tc1.py` — Client 1 (hospital node 1). Loads `final_dataset_2.csv`, trains a binary classifier on the `target` column (intrusion vs. normal), reports accuracy
- `tc2.py` — Client 2 (hospital node 2). Loads `adjusted_data2.csv`, trains a regression model using `length` as the target, reports MAE

**Earlier FL experiments**
- `servermiot.py`, `ser.py` — simpler FedAvg servers used in early tests
- `client1miot.py`, `client2miot.py`, `cli1.py`, `cli2.py` — earlier clients using other CSV datasets (regression on `length`)

**Attack and traffic utilities**
- `bahubali.py` — UDP flood traffic generator (DoS-style traffic against a target IP/port)
- `rocky4.py` — MQTT traffic capture using Scapy, saves packets to a PCAP file

**Documentation**
- `MEDICAL_IOT_ANSWERS.md` — answers to common questions about nodes, records, rounds, and setup

> Some scripts use absolute paths under `/Users/apple/...`. Update these if you move the project to a different machine.

---

## How It Works

1. Each client (hospital node) holds its own dataset of network/packet-level features
2. Clients train local models and send **model weights** — not raw data — to the server
3. The Flower server aggregates the updates using FedAvg into a global model
4. Optionally, `ts.py` evaluates the aggregated model on a merged dataset to track global performance

**Configuration (main Medical IoT setup):**
- Nodes: 2 hospital nodes (`tc1.py`, `tc2.py`)
- Records: ~369,000 total across both nodes
- Rounds: 5 FL rounds

---

## Requirements

```bash
pip install flwr tensorflow pandas scikit-learn scapy
```

> Skip `scapy` if you don't need packet capture.

---

## Running the Main Setup

Uses `tc1.py` and `tc2.py` as clients and `ts.py` as the server.

**1. Make sure datasets are in place:**
- `/Users/apple/Downloads/final_dataset_2.csv` (for `tc1.py`)
- `/Users/apple/adjusted_data2.csv` (for `tc2.py`)

**2. Start the server** in one terminal:
```bash
cd /Users/apple/Documents/miot
python ts.py
```
Runs 5 federated rounds.

**3. Start client 1** in a second terminal:
```bash
python tc1.py
```
Trains a binary classifier on `target`, reports accuracy.

**4. Start client 2** in a third terminal:
```bash
python tc2.py
```
Trains a regression model predicting `length`, reports MAE.

**5. Watch the output** — the server logs each round and aggregated results; clients log local training and evaluation metrics.

---

## Running the Earlier Setup (Optional)

```bash
python servermiot.py
python client1miot.py
python client2miot.py
```

Uses `client1_data.csv` and `client2_data.csv` (~155k records each), regression on `length`.

---

## Attack Simulation — UDP Flood

> **Only run on localhost or test environments you fully control.**

```bash
python bahubali.py
```

Targets `127.0.0.1:12345` by default. Sending flood traffic to external systems may violate policies or laws.

---

## Traffic Capture — MQTT

```bash
python rocky4.py
```

Captures MQTT traffic on port 1883 using Scapy and saves to `mqtt_traffic.pcap`. May need sudo on some interfaces.

---

## Notes

- **Hardcoded paths:** Update `/Users/apple/...` paths if running on a different machine
- **Metrics:** `tc1.py` reports accuracy (classification); `tc2.py` and earlier clients report MAE (regression)
- **Extending:** Add more clients to simulate additional hospital nodes, unify clients to classify on a common label, or add logging (TensorBoard, CSV) to track metrics per round

---

## Future Work — Blockchain Layer

A possible extension is adding a blockchain-based security layer on top of the federated learning setup:

- **Data integrity:** Store encrypted medical data off-chain, keep hashes on-chain. Tampering becomes detectable even if storage is compromised
- **Model audit trail:** Record model updates, metrics, and round summaries as signed transactions — creates a tamper-evident log of what each client sent and what the server aggregated
- **Defense in depth:** FL already avoids centralizing raw data. A blockchain layer would further protect both medical records and model updates

---
