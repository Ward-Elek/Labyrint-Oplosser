import os
import sys

# Ensure project modules in practice/task are importable when running tests from repository root.
test_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(test_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
