import subprocess
import time
import urllib.request
import os
import sys

def test_frontend_routing():
    print("🚀 Starting Lumia FastAPI Backend to verify static serving...")
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/replytim/Desktop/portaldot"
    
    server_process = subprocess.Popen(
        ["venv/bin/python", "-m", "backend.app"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to boot up
    time.sleep(6)
    
    success = True
    try:
        # Test 1: Fetch root index.html
        print("\n🔍 Test 1: GET http://127.0.0.1:8000/")
        req = urllib.request.Request("http://127.0.0.1:8000/")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            print(f"✅ Loaded index.html successfully! (Length: {len(html)} characters)")
            assert "<title>Lumia // AI Trust Layer for Portaldot</title>" in html
            assert "style.css" in html
            assert "app.js" in html

        # Test 2: Fetch style.css
        print("\n🔍 Test 2: GET http://127.0.0.1:8000/static/style.css")
        req = urllib.request.Request("http://127.0.0.1:8000/static/style.css")
        with urllib.request.urlopen(req) as response:
            css = response.read().decode()
            print(f"✅ Loaded style.css successfully! (Length: {len(css)} characters)")
            assert "LUMIA Protocol" in css
            assert "glass-panel" in css

        # Test 3: Fetch app.js
        print("\n🔍 Test 3: GET http://127.0.0.1:8000/static/app.js")
        req = urllib.request.Request("http://127.0.0.1:8000/static/app.js")
        with urllib.request.urlopen(req) as response:
            js = response.read().decode()
            print(f"✅ Loaded app.js successfully! (Length: {len(js)} characters)")
            assert "LUMIA Protocol - Dashboard" in js
            assert "scan-form" in js

    except Exception as e:
        print(f"❌ Frontend Routing Verification Failed: {e}")
        success = False
    finally:
        print("\n🛑 Stopping background server process...")
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("Server stopped.")
        
    if success:
        print("\n🟢 ALL FRONTEND STATIC ROUTING FULLY VERIFIED!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    test_frontend_routing()
