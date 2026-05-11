import sys
sys.path.insert(0, "generated")

import grpc
from concurrent import futures
from generated import services_pb2
from generated import services_pb2_grpc


# Simple bot replies
BOT_REPLIES = {
    "hello":   "Hey there! How can I help?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "bye":     "Goodbye! Have a great day!",
}


class ChatServiceServicer(services_pb2_grpc.ChatServiceServicer):

    def Chat(self, request_iterator, context):
        # Both sides stream simultaneously
        for message in request_iterator:
            print(f"[Server] Received from '{message.user}': {message.text}")

            reply_text = BOT_REPLIES.get(
                message.text.lower(),
                f"You said: '{message.text}' — I don't understand that yet!"
            )

            print(f"[Server] Replying: {reply_text}")

            # yield = send one response back to client
            yield services_pb2.ChatMessage(user="Bot", text=reply_text)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[Server] Unary server running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()