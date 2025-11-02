"""
Test if the orchestrator can properly call database functions.
This diagnoses why database calls aren't showing up in pipeline runs.
"""

import sys
import os

# Point sys.path at backend/
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BACKEND_DIR)

# Load .env
from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

print("="*80)
print("ORCHESTRATOR DATABASE INTEGRATION TEST")
print("="*80)

# Test 1: Can we import orchestrator?
print("\n[1] Testing orchestrator import...")
try:
    from api.services import orchestrator
    print("✅ Orchestrator module imported")
except Exception as e:
    print(f"❌ Failed to import orchestrator: {e}")
    sys.exit(1)

# Test 2: Are database functions available in orchestrator?
print("\n[2] Checking if database functions are imported in orchestrator...")
import inspect
source = inspect.getsource(orchestrator)

checks = [
    ("save_pipeline_start import", "from .database import" in source and "save_pipeline_start" in source),
    ("update_pipeline_progress import", "update_pipeline_progress" in source),
    ("save_pipeline_completion import", "save_pipeline_completion" in source),
    ("save_pipeline_error import", "save_pipeline_error" in source),
    ("save_pipeline_start call", "save_pipeline_start(run_id" in source),
    ("update_pipeline_progress call", "update_pipeline_progress(run_id" in source),
    ("save_pipeline_completion call", "save_pipeline_completion(" in source),
]

all_good = True
for name, result in checks:
    status = "✅" if result else "❌"
    print(f"  {status} {name}")
    if not result:
        all_good = False

if not all_good:
    print("\n❌ Some database functions are missing from orchestrator!")
    sys.exit(1)

# Test 3: Can we import database functions directly?
print("\n[3] Testing direct import of database functions...")
try:
    from api.services.database import (
        save_pipeline_start,
        update_pipeline_progress,
        save_pipeline_completion,
        save_pipeline_error
    )
    print("✅ All database functions imported successfully")
except Exception as e:
    print(f"❌ Failed to import database functions: {e}")
    sys.exit(1)

# Test 4: Can we call database functions directly?
print("\n[4] Testing direct database function calls...")
print("\nCalling save_pipeline_start('test_direct_123', 'https://test.com', 'Pop')...")
result = save_pipeline_start('test_direct_123', 'https://test.com', 'Pop')
print(f"Result: {result}")

if result:
    print("✅ Direct call successful - data should be in Google Sheets")
else:
    print("⚠️  Direct call returned False - check warnings above")

# Test 5: Test the orchestrator's generate_hiresong_video function signature
print("\n[5] Checking orchestrator function signature...")
try:
    sig = inspect.signature(orchestrator.generate_hiresong_video)
    print(f"✅ Function signature: {sig}")
    print(f"   Parameters: {list(sig.parameters.keys())}")
except Exception as e:
    print(f"❌ Failed to get signature: {e}")

# Test 6: Check if there are any import-time errors
print("\n[6] Testing if orchestrator module has any import-time issues...")
try:
    # Force reload to see if there are any issues
    import importlib
    importlib.reload(orchestrator)
    print("✅ Orchestrator reloaded successfully - no import-time errors")
except Exception as e:
    print(f"❌ Orchestrator has import-time errors: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Verify the database functions are actually callable
print("\n[7] Verifying database functions are callable...")
try:
    print(f"  save_pipeline_start is callable: {callable(orchestrator.save_pipeline_start)}")
    print(f"  update_pipeline_progress is callable: {callable(orchestrator.update_pipeline_progress)}")
    print(f"  save_pipeline_completion is callable: {callable(orchestrator.save_pipeline_completion)}")
    print(f"  save_pipeline_error is callable: {callable(orchestrator.save_pipeline_error)}")
    print("✅ All functions are callable")
except AttributeError as e:
    print(f"❌ Functions not found in orchestrator: {e}")
    print("\nAvailable in orchestrator module:")
    print([x for x in dir(orchestrator) if not x.startswith('_')])

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\nCheck your Google Sheet to see if 'test_direct_123' row was added:")
print("https://docs.google.com/spreadsheets/d/1ZBwSfDbNE9DA5YQ2LVGovLdhtkYzEwwmGiaLvE9E5QA/")

