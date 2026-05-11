import sys
sys.path.insert(0, "generated")

import grpc
from concurrent import futures
from generated import services_pb2
from generated import services_pb2_grpc


class CalculatorServicer(services_pb2_grpc.CalculatorServicer):

    def Add(self, request, context):
        print(f"[Server] Received: {request.a} + {request.b}")
        result = request.a + request.b
        return services_pb2.AddResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[Server] Unary server running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()