import sys
sys.path.insert(0, "generated")

import grpc
from generated import services_pb2
from generated import services_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = services_pb2_grpc.CalculatorStub(channel)

        request = services_pb2.AddRequest(a=10, b=25)
        response = stub.Add(request)  # Single call, single response

        print(f"[Client] 10 + 25 = {response.result}")


if __name__ == "__main__":
    run()