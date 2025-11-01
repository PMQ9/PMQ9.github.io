#!/usr/bin/env python3
"""Simple HTTP server with user-friendly output"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
os.chdir(Path(__file__).parent)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"\n{'='*60}")
    print(f"🚀 Server is running!")
    print(f"{'='*60}")
    print(f"📍 Visit: http://localhost:{PORT}")
    print(f"{'='*60}\n")
    httpd.serve_forever()
