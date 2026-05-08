import argparse
import socket
import threading


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 28765
BUFFER_SIZE = 1024


def receive_loop(sock, peer_name):
    """Continuously read incoming messages and print them."""
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print(f"\n[{peer_name}] disconnected.")
                break
            print(f"\n{peer_name}: {data.decode('utf-8', errors='replace')}")
        except OSError:
            break


def send_loop(sock):
    """Read terminal input and send it to the peer until /quit."""
    while True:
        try:
            message = input("You: ")
        except (EOFError, KeyboardInterrupt):
            message = "/quit"

        if message.strip().lower() == "/quit":
            break

        try:
            sock.sendall(message.encode("utf-8"))
        except OSError:
            print("Connection closed.")
            break


def run_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print(f"Server listening on {host}:{port}")
        print("Open a second terminal and start the client.")

        conn, addr = server.accept()
        with conn:
            print(f"Connected by {addr}")
            recv_thread = threading.Thread(target=receive_loop, args=(conn, "Client"), daemon=True)
            recv_thread.start()
            send_loop(conn)


def run_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        recv_thread = threading.Thread(target=receive_loop, args=(client, "Server"), daemon=True)
        recv_thread.start()
        send_loop(client)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simple localhost socket chat. Run in two terminals: one server, one client."
    )
    parser.add_argument("mode", choices=["server", "client"], help="Run as server or client")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host/IP to bind/connect (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port (default: {DEFAULT_PORT})")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.mode == "server":
        run_server(args.host, args.port)
    else:
        run_client(args.host, args.port)