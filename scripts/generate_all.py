#!/usr/bin/env python3
"""
Master script to run all generation scripts in order.

This script orchestrates the execution of all code generation scripts
in the correct sequence to build the complete qnty unit system.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_script(script_path: Path, description: str) -> bool:
    """
    Run a single script and report status.
    
    Args:
        script_path: Path to the script to run
        description: Description of what the script does
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"Running: {script_path.name}")
    print(f"Purpose: {description}")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        elapsed = time.time() - start_time
        
        # Print script output
        if result.stdout:
            print(result.stdout)
        
        print(f"✅ {script_path.name} completed successfully in {elapsed:.2f}s")
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"❌ {script_path.name} failed after {elapsed:.2f}s")
        print("Error output:")
        if e.stderr:
            print(e.stderr)
        if e.stdout:
            print(e.stdout)
        return False
    except Exception as e:
        print(f"❌ Unexpected error running {script_path.name}: {e}")
        return False


def main():
    """Main function to run all scripts in sequence."""
    
    # Setup paths
    scripts_dir = Path(__file__).parent
    
    # Define scripts to run in order with descriptions
    scripts = [
        ("_1_generate_dimensions.py", "Generate dimension constants from unit definitions"),
        ("_2_generate_units.py", "Generate consolidated units module with all unit definitions"),
        ("_3_generate_variables.py", "Generate variables module with type-safe variable classes"),
        ("_4_generate_variable_pyi.py", "Generate type stub file for IDE support"),
        ("_5_generate_package_init.py", "Generate package __init__.py with public API exports"),
    ]
    
    print("\n" + "="*70)
    print("QNTY Code Generation Pipeline")
    print("="*70)
    print(f"\nThis will run {len(scripts)} generation scripts in sequence:")
    for i, (script_name, description) in enumerate(scripts, 1):
        print(f"  {i}. {script_name:35} - {description}")
    
    print("\nStarting generation pipeline...")
    
    total_start = time.time()
    successful = 0
    failed = 0
    
    # Run each script in order
    for script_name, description in scripts:
        script_path = scripts_dir / script_name
        
        if not script_path.exists():
            print(f"\n⚠️  Warning: {script_name} not found, skipping...")
            continue
            
        if run_script(script_path, description):
            successful += 1
        else:
            failed += 1
            print(f"\n❌ Pipeline stopped due to failure in {script_name}")
            break
    
    # Print summary
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*70)
    print("Generation Pipeline Summary")
    print("="*70)
    print(f"Total time: {total_elapsed:.2f}s")
    print(f"Scripts run: {successful + failed}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✅ All generation scripts completed successfully!")
        print("\nGenerated files:")
        src_path = scripts_dir.parent / "src" / "qnty"
        generated_files = [
            "dimension.py",
            "units.py",
            "variables.py",
            "variables.pyi",
            "__init__.py"
        ]
        for file_name in generated_files:
            file_path = src_path / file_name
            if file_path.exists():
                size = file_path.stat().st_size
                lines = len(file_path.read_text().splitlines())
                print(f"  • {file_name:20} ({lines:,} lines, {size:,} bytes)")
    else:
        print("\n❌ Pipeline failed. Please check the errors above.")
        sys.exit(1)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
