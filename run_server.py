"""
Start ASYLUM server on the first available port (8001, 8002, 8003).
Avoids "address already in use" when a previous instance is still running.
"""
import socket
import sys


def port_free(host: str, port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
        return True
    except OSError:
        return False


def main():
    host = "127.0.0.1"
    for port in (8001, 8002, 8003):
        if port_free(host, port):
            print(f"Starting ASYLUM server at http://{host}:{port}", flush=True)
            print(f"Open this URL in your browser. Close this window to stop the server.", flush=True)
            import uvicorn
            uvicorn.run("api.main:app", host=host, port=port)
            return
        print(f"Port {port} in use, trying next...", flush=True)
    print("Ports 8001, 8002, 8003 are all in use. Close another ASYLUM server or free a port.", flush=True)
    sys.exit(1)


if __name__ == "__main__":
    main()
