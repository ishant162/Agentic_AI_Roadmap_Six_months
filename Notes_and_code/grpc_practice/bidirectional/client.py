import sys
sys.path.insert(0, "generated")

import grpc
import time
from generated import services_pb2
from generated import services_pb2_grpc


def generate_messages():
    messages = ["Hello", "How are you", "What is gRPC", "Bye"]

    for text in messages:
        print(f"[Client] Sending: {text}")
        time.sleep(0.8)
        yield services_pb2.ChatMessage(user="Ishant", text=text)


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = services_pb2_grpc.ChatServiceStub(channel)

        print("[Client] Starting chat...\n")

        # Both generator (outgoing) and iterator (incoming) run simultaneously
        responses = stub.Chat(generate_messages())

        for response in responses:
            print(f"[Client] Bot replied: {response.text}\n")

        print("[Client] Chat ended.")


if __name__ == "__main__":
    run()