"""
Assistive Communication Device - Main Application
Real-time lip movement recognition system for speech impairments

This application integrates:
- Visual lip movement detection using computer vision
- Llama 2 for text processing and generation
- OpenAI Whisper technologies for speech synthesis
- AMD Ryzen AI hardware acceleration
"""

import cv2
import sys
import time
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.lip_detection import LipDetector
from src.text_processing import TextProcessor
from src.speech_synthesis import SpeechSynthesizer
from src.utils import CameraCapture, ConfigLoader


class AssistiveCommunicationDevice:
    """
    Main application class for the assistive communication device
    """
    
    def __init__(self, config_path=None):
        """
        Initialize the assistive communication device
        
        Args:
            config_path: Path to configuration file
        """
        print("=" * 60)
        print("Assistive Communication Device for Speech Impairments")
        print("Visual Lip Movement Recognition System")
        print("=" * 60)
        
        # Load configuration
        self.config = ConfigLoader(config_path)
        
        # Initialize components
        print("\nInitializing components...")
        
        # Camera
        camera_config = self.config.get('camera')
        self.camera = CameraCapture(
            camera_id=camera_config['device_id'],
            width=camera_config['width'],
            height=camera_config['height'],
            fps=camera_config['fps']
        )
        
        # Lip detector
        lip_config = self.config.get('lip_detection')
        self.lip_detector = LipDetector(
            min_detection_confidence=lip_config['min_detection_confidence'],
            min_tracking_confidence=lip_config['min_tracking_confidence']
        )
        
        # Text processor (Llama 2)
        text_config = self.config.get('text_processing')
        self.text_processor = TextProcessor(
            model_name=text_config['model_name'],
            use_local=text_config['use_local']
        )
        
        # Speech synthesizer
        speech_config = self.config.get('speech_synthesis')
        self.speech_synthesizer = SpeechSynthesizer(
            engine=speech_config['engine'],
            rate=speech_config['rate'],
            volume=speech_config['volume']
        )
        
        # Runtime state
        self.running = False
        self.last_speech_time = 0
        self.speech_interval = 3.0  # seconds between speech outputs
        self.frame_count = 0
        self.start_time = None
        
        print("\nComponents initialized successfully!")
        print("\nAMD Ryzen AI Optimization: Enabled" if self.config.get('amd_ryzen_ai.enable_hardware_acceleration') else "AMD Ryzen AI Optimization: Disabled")
    
    def start(self):
        """Start the application"""
        print("\nStarting application...")
        
        # Start camera
        self.camera.start()
        
        # Optionally load Llama 2 model (can be slow)
        load_llama = input("\nLoad Llama 2 model? (requires HuggingFace auth) [y/N]: ").lower() == 'y'
        if load_llama:
            print("\nLoading Llama 2 model (this may take several minutes)...")
            self.text_processor.load_model()
        else:
            print("\nSkipping Llama 2 model loading (using basic processing)")
        
        self.running = True
        self.start_time = time.time()
        
        print("\n" + "=" * 60)
        print("Application started!")
        print("Press 'q' to quit, 's' to speak current text, 'r' to reset")
        print("=" * 60 + "\n")
        
        self.run_loop()
    
    def run_loop(self):
        """Main processing loop"""
        try:
            while self.running and self.camera.is_running():
                # Capture frame
                frame = self.camera.read()
                
                if frame is None:
                    continue
                
                self.frame_count += 1
                
                # Detect lip movement
                movement_detected, movement_magnitude, annotated_frame = \
                    self.lip_detector.detect_movement(frame)
                
                # Process movement pattern
                if movement_detected:
                    movement_history = self.lip_detector.get_movement_pattern()
                    recognized_text = self.text_processor.process_movement(movement_history)
                    
                    # Display recognized text on frame
                    cv2.putText(annotated_frame, f"Text: {recognized_text}", 
                               (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    
                    # Periodic speech output
                    current_time = time.time()
                    if current_time - self.last_speech_time > self.speech_interval:
                        if recognized_text:
                            self.speech_synthesizer.speak_async(recognized_text)
                            self.last_speech_time = current_time
                
                # Calculate and display FPS
                elapsed = time.time() - self.start_time
                fps = self.frame_count / elapsed if elapsed > 0 else 0
                cv2.putText(annotated_frame, f"FPS: {fps:.1f}", 
                           (10, annotated_frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display frame
                cv2.imshow('Assistive Communication Device', annotated_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\nQuitting...")
                    break
                elif key == ord('s'):
                    # Speak current text
                    text = self.text_processor.get_current_text()
                    if text:
                        print(f"\nSpeaking: {text}")
                        self.speech_synthesizer.speak(text)
                elif key == ord('r'):
                    # Reset
                    print("\nResetting...")
                    self.text_processor.reset_buffer()
                    self.lip_detector.reset()
                
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the application and cleanup"""
        print("\nStopping application...")
        
        self.running = False
        
        # Cleanup components
        self.camera.stop()
        self.lip_detector.close()
        self.speech_synthesizer.cleanup()
        
        # Close windows
        cv2.destroyAllWindows()
        
        # Print statistics
        if self.start_time:
            elapsed = time.time() - self.start_time
            avg_fps = self.frame_count / elapsed if elapsed > 0 else 0
            print(f"\nSession statistics:")
            print(f"  Duration: {elapsed:.1f} seconds")
            print(f"  Frames processed: {self.frame_count}")
            print(f"  Average FPS: {avg_fps:.1f}")
        
        print("\nApplication stopped successfully")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Assistive Communication Device with Lip Movement Recognition'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--camera',
        type=int,
        default=0,
        help='Camera device ID (default: 0)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create and start application
        app = AssistiveCommunicationDevice(config_path=args.config)
        
        # Override camera ID if specified
        if args.camera != 0:
            app.config.set('camera.device_id', args.camera)
        
        app.start()
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
