"""
Camera Capture Utility
Handles video capture from webcam or video file
"""

import cv2
import threading
import queue


class CameraCapture:
    """
    Camera capture handler with threading support for better performance
    """
    
    def __init__(self, camera_id=0, width=640, height=480, fps=30):
        """
        Initialize camera capture
        
        Args:
            camera_id: Camera device ID or video file path
            width: Frame width
            height: Frame height
            fps: Target frames per second
        """
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        
        self.cap = None
        self.frame_queue = queue.Queue(maxsize=2)
        self.running = False
        self.capture_thread = None
        
    def start(self):
        """Start camera capture"""
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {self.camera_id}")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        # AMD Ryzen AI optimization: Enable hardware acceleration if available
        self.cap.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY)
        
        self.running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        
        print(f"Camera started: {self.width}x{self.height} @ {self.fps}fps")
        
    def _capture_loop(self):
        """Continuous frame capture loop"""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Clear old frames if queue is full
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                
                try:
                    self.frame_queue.put_nowait(frame)
                except queue.Full:
                    pass
    
    def read(self):
        """
        Read latest frame from camera
        
        Returns:
            frame: Latest captured frame or None
        """
        try:
            return self.frame_queue.get(timeout=1.0)
        except queue.Empty:
            return None
    
    def is_running(self):
        """Check if capture is running"""
        return self.running and self.cap is not None and self.cap.isOpened()
    
    def stop(self):
        """Stop camera capture"""
        self.running = False
        
        if self.capture_thread is not None:
            self.capture_thread.join(timeout=2.0)
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        print("Camera stopped")
    
    def get_fps(self):
        """Get actual camera FPS"""
        if self.cap is not None:
            return self.cap.get(cv2.CAP_PROP_FPS)
        return 0
    
    def get_resolution(self):
        """Get actual camera resolution"""
        if self.cap is not None:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return (width, height)
        return (0, 0)
