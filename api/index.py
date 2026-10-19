import sys
import os

# Add Backend folder to sys.path so modules (analyzer, database) can be resolved
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "..", "Backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
