import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    print("=" * 65)
    print("  Starting PG Finder - StaySathi Voice AI Production Suite")
    print("=" * 65)
    print("  Web Console: http://localhost:8000")
    print("  API Docs:    http://localhost:8000/docs")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
