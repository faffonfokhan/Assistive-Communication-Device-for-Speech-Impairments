"""
Quick syntax and structure validation test
Tests that all Python files are syntactically correct
"""

import sys
import os
from pathlib import Path

def test_file_syntax(filepath):
    """Test if a Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        return True, None
    except SyntaxError as e:
        return False, str(e)

def main():
    """Test all Python files in the project"""
    print("=" * 60)
    print("Project Structure and Syntax Validation")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    
    # Find all Python files
    python_files = list(project_root.glob('**/*.py'))
    python_files = [f for f in python_files if '.git' not in str(f) and '__pycache__' not in str(f)]
    
    print(f"\nFound {len(python_files)} Python files\n")
    
    passed = 0
    failed = 0
    
    for filepath in sorted(python_files):
        rel_path = filepath.relative_to(project_root)
        success, error = test_file_syntax(filepath)
        
        if success:
            print(f"✓ {rel_path}")
            passed += 1
        else:
            print(f"✗ {rel_path}: {error}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("Syntax Test Summary")
    print("=" * 60)
    print(f"Passed: {passed}/{len(python_files)}")
    print(f"Failed: {failed}/{len(python_files)}")
    
    # Test project structure
    print("\n" + "=" * 60)
    print("Project Structure Validation")
    print("=" * 60)
    
    required_files = [
        'README.md',
        'requirements.txt',
        'main.py',
        'demo.py',
        '.gitignore',
        'config/default_config.json',
        'src/__init__.py',
        'src/lip_detection/__init__.py',
        'src/lip_detection/detector.py',
        'src/text_processing/__init__.py',
        'src/text_processing/processor.py',
        'src/speech_synthesis/__init__.py',
        'src/speech_synthesis/synthesizer.py',
        'src/utils/__init__.py',
        'src/utils/camera.py',
        'src/utils/config_loader.py',
    ]
    
    structure_passed = 0
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
            structure_passed += 1
        else:
            print(f"✗ {file_path} (missing)")
    
    print(f"\n{structure_passed}/{len(required_files)} required files present")
    
    # Test documentation files
    print("\n" + "=" * 60)
    print("Documentation Files")
    print("=" * 60)
    
    doc_files = [
        'README.md',
        'INSTALLATION.md',
        'USAGE.md',
        'ARCHITECTURE.md',
    ]
    
    for doc_file in doc_files:
        full_path = project_root / doc_file
        if full_path.exists():
            size = os.path.getsize(full_path)
            print(f"✓ {doc_file} ({size} bytes)")
        else:
            print(f"✗ {doc_file} (missing)")
    
    # Overall result
    print("\n" + "=" * 60)
    if failed == 0 and structure_passed == len(required_files):
        print("✓ All tests passed!")
        print("The project structure is complete and all files are valid.")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
