"""
Run the program
"""
import sys
import os
from src.console import console

# Add the project root to path so imports work correctly
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

console()
