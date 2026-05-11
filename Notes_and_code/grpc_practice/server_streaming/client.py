import sys
sys.path.insert(0, "generated")

import grpc
from generated import services_pb2
from generated import services_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = services_pb2_grpc.LogServiceStub(channel)

        request = services_pb2.LogRequest(service_name="payment-service")

        print("[Client] Requesting logs...\n")

        # Iterating over a stream — server keeps sending, client keeps receiving
        for log in stub.GetLogs(request):
            print(f"[Client] [{log.level}] {log.message}")

        print("\n[Client] Stream ended.")


if __name__ == "__main__":
    run()