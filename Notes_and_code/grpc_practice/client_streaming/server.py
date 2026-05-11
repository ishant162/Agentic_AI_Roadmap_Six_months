import sys
sys.path.insert(0, "generated")

import grpc
from concurrent import futures
from generated import services_pb2
from generated import services_pb2_grpc


class AggregatorServicer(services_pb2_grpc.AggregatorServicer):

    def UploadNumbers(self, request_iterator, context):
        total = 0
        count = 0

        # request_iterator keeps yielding as client sends chunks
        for chunk in request_iterator:
            print(f"[Server] Received number: {chunk.value}")
            total += chunk.value
            count += 1

        print(f"[Server] All chunks received. Total={total}, Count={count}")

        # Send ONE response after all client data is received
        return services_pb2.SumResponse(total=total, count=count)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AggregatorServicer_to_server(AggregatorServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("[Server] Client-Streaming server running on port 50052...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()