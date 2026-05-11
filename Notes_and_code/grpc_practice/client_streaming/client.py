import sys
import time
sys.path.insert(0, "generated")

import grpc
from generated import services_pb2
from generated import services_pb2_grpc

def generate_numbers():
    numbers = [10, 20, 5, 40, 25]

    for num in numbers:
        print(f"[Client] Sending number: {num}")
        time.sleep(0.4)  # Simulate sending chunks over time
        yield services_pb2.NumberChunk(value=num)

def run():
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = services_pb2_grpc.AggregatorStub(channel)

        response = stub.UploadNumbers(generate_numbers())
        print("Server replied")
        print(f"[Client]   Total = {response.total}")
        print(f"[Client]   Count = {response.count}")
        print(f"[Client]   Average = {response.total / response.count:.2f}")

if __name__ == "__main__":
    run()