"""
Demo script to test individual components
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def test_lip_detector():
    """Test lip detector initialization"""
    print("Testing Lip Detector...")
    try:
        from src.lip_detection import LipDetector
        detector = LipDetector()
        print("✓ Lip Detector initialized successfully")
        detector.close()
        return True
    except Exception as e:
        print(f"✗ Lip Detector failed: {e}")
        return False


def test_text_processor():
    """Test text processor initialization"""
    print("\nTesting Text Processor...")
    try:
        from src.text_processing import TextProcessor
        processor = TextProcessor()
        
        # Test basic movement processing
        test_movements = [2.5, 3.0, 2.8, 3.2]
        text = processor.process_movement(test_movements)
        print(f"✓ Text Processor initialized successfully")
        print(f"  Sample output: '{text}'")
        return True
    except Exception as e:
        print(f"✗ Text Processor failed: {e}")
        return False


def test_speech_synthesizer():
    """Test speech synthesizer initialization"""
    print("\nTesting Speech Synthesizer...")
    try:
        from src.speech_synthesis import SpeechSynthesizer
        synthesizer = SpeechSynthesizer()
        print("✓ Speech Synthesizer initialized successfully")
        
        # Test speech (print mode)
        synthesizer.speak("Hello")
        synthesizer.cleanup()
        return True
    except Exception as e:
        print(f"✗ Speech Synthesizer failed: {e}")
        return False


def test_camera():
    """Test camera capture (without actually opening camera)"""
    print("\nTesting Camera Capture...")
    try:
        from src.utils import CameraCapture
        # Just test initialization, don't actually start
        camera = CameraCapture(camera_id=0)
        print("✓ Camera Capture initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Camera Capture failed: {e}")
        return False


def test_config_loader():
    """Test configuration loader"""
    print("\nTesting Config Loader...")
    try:
        from src.utils import ConfigLoader
        config = ConfigLoader()
        
        # Test basic config operations
        value = config.get('camera.width')
        print(f"✓ Config Loader initialized successfully")
        print(f"  Sample config value (camera.width): {value}")
        return True
    except Exception as e:
        print(f"✗ Config Loader failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Component Testing Demo")
    print("=" * 60)
    
    tests = [
        test_config_loader,
        test_camera,
        test_lip_detector,
        test_text_processor,
        test_speech_synthesizer,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All components are working correctly!")
    else:
        print("\n✗ Some components failed. Check error messages above.")
        print("Note: Some failures may be due to missing optional dependencies.")
    
    print("\nTo run the full application:")
    print("  python main.py")


if __name__ == '__main__':
    main()
