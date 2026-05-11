import sys
sys.path.insert(0, "generated")

import grpc
import time
from concurrent import futures
from generated import services_pb2
from generated import services_pb2_grpc

# Fake log data
FAKE_LOGS = [
    ("INFO",  "Service started successfully"),
    ("INFO",  "Listening on port 8080"),
    ("WARN",  "High memory usage detected"),
    ("INFO",  "Request received from 192.168.1.1"),
    ("ERROR", "Database connection timed out"),
    ("INFO",  "Retrying database connection..."),
    ("INFO",  "Database reconnected"),
]


class LogServiceServicer(services_pb2_grpc.LogServiceServicer):

    def GetLogs(self, request, context):
        print(f"[Server] Client requested logs for: {request.service_name}")

        for level, message in FAKE_LOGS:
            # Simulate logs arriving over time
            time.sleep(0.5)

            print(f"[Server] Sending log: [{level}] {message}")

            # yield sends one response at a time (streaming)
            yield services_pb2.LogEntry(level=level, message=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_LogServiceServicer_to_server(LogServiceServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("[Server] Server-Streaming server running on port 50052...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()