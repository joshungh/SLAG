import os
import sys
import uvicorn

if __name__ == "__main__":
    try:
        port = 3500
        print(f"Starting server on port {port}...")
        uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is already in use. Please try a different port or kill the process using this port.")
            sys.exit(1)
        raise 