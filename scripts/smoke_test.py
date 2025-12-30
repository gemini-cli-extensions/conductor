import subprocess
import os
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(
        cmd, 
        shell=True, 
        cwd=cwd, 
        capture_output=True, 
        text=True,
        env={**os.environ, "PYTHONPATH": f"{os.getcwd()}/conductor-gemini/src:{os.getcwd()}/conductor-core/src"}
    )
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout

def run_smoke_test():
    test_workspace = Path("/tmp/conductor_smoke_test")
    if test_workspace.exists():
        shutil.rmtree(test_workspace)
    test_workspace.mkdir(parents=True)
    
    # 1. Init git
    run_command("git init", cwd=test_workspace)
    run_command("git config user.email 'smoke@test.com'", cwd=test_workspace)
    run_command("git config user.name 'smoke'", cwd=test_workspace)
    
    # 2. Run Setup
    print("\n--- Testing Setup ---")
    run_command("python -m conductor_gemini.cli setup --goal 'Smoke test project'", cwd=test_workspace)
    assert (test_workspace / "conductor" / "product.md").exists()
    assert "Smoke test project" in (test_workspace / "conductor" / "product.md").read_text()
    
    # 3. Run New Track
    print("\n--- Testing New Track ---")
    run_command("python -m conductor_gemini.cli new-track 'Test feature'", cwd=test_workspace)
    tracks_dir = test_workspace / "conductor" / "tracks"
    assert any(tracks_dir.iterdir()) # Ensure at least one track was created
    
    # 4. Run Status
    print("\n--- Testing Status ---")
    output = run_command("python -m conductor_gemini.cli status", cwd=test_workspace)
    assert "Project Tracks" in output
    
    print("\nSmoke test passed successfully!")

if __name__ == "__main__":
    try:
        run_smoke_test()
    except Exception as e:
        print(f"Smoke test failed: {e}")
        exit(1)
