"""
AR Colorize - Real-Time Wall Repainting System
Main Python implementation for wall detection and color overlay
"""

import cv2
import numpy as np
from typing import Tuple, List
import argparse


class ARColorize:
    """Main class for AR wall colorization system"""
    
    def __init__(self):
        self.selected_color = (255, 255, 255)  # Default white in BGR
        self.cap = None
        self.running = False
        
    def hex_to_bgr(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to BGR format for OpenCV"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (rgb[2], rgb[1], rgb[0])  # Convert RGB to BGR
    
    def detect_wall(self, frame: np.ndarray) -> np.ndarray:
        """
        Detect wall surfaces in the frame using edge detection and color analysis
        Returns a mask where walls are detected
        """
        # Convert to different color spaces
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        
        # Create mask for lighter areas (typically walls)
        # Walls are usually in the mid to high value range
        _, brightness_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # Reduce noise
        kernel = np.ones((5, 5), np.uint8)
        brightness_mask = cv2.morphologyEx(brightness_mask, cv2.MORPH_CLOSE, kernel)
        brightness_mask = cv2.morphologyEx(brightness_mask, cv2.MORPH_OPEN, kernel)
        
        # Remove edges from wall mask (walls should be uniform)
        edges_dilated = cv2.dilate(edges, kernel, iterations=1)
        wall_mask = cv2.bitwise_and(brightness_mask, cv2.bitwise_not(edges_dilated))
        
        return wall_mask
    
    def apply_color_overlay(self, frame: np.ndarray, mask: np.ndarray, 
                           color: Tuple[int, int, int], alpha: float = 0.7) -> np.ndarray:
        """
        Apply color overlay to the masked regions of the frame
        alpha: transparency level (0.0 to 1.0)
        """
        # Create colored overlay
        overlay = np.zeros_like(frame)
        overlay[mask > 0] = color
        
        # Blend the overlay with original frame
        result = frame.copy()
        result[mask > 0] = cv2.addWeighted(
            frame[mask > 0], 
            1 - alpha, 
            overlay[mask > 0], 
            alpha, 
            0
        )
        
        return result
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame and apply AR color overlay"""
        # Detect walls
        wall_mask = self.detect_wall(frame)
        
        # Apply color overlay
        result = self.apply_color_overlay(frame, wall_mask, self.selected_color)
        
        # Add visualization of detected walls (optional)
        contours, _ = cv2.findContours(wall_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(result, contours, -1, (0, 255, 0), 2)
        
        return result
    
    def start_camera(self, camera_id: int = 0):
        """Start the camera and begin processing"""
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
        self.running = True
        print("Camera started. Press 'q' to quit, 'c' to change color")
        print("Press '1-9' to select preset colors")
        
        # Preset colors (BGR format)
        preset_colors = {
            '1': (255, 255, 255),  # White
            '2': (220, 248, 255),  # Cream
            '3': (211, 211, 211),  # Light Gray
            '4': (235, 206, 135),  # Sky Blue (BGR)
            '5': (152, 255, 152),  # Mint Green (BGR)
            '6': (185, 218, 255),  # Peach (BGR)
            '7': (250, 230, 230),  # Lavender (BGR)
            '8': (80, 127, 255),   # Coral (BGR)
            '9': (131, 193, 157),  # Sage Green (BGR)
        }
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process frame
            processed = self.process_frame(frame)
            
            # Display original and processed frames side by side
            combined = np.hstack((frame, processed))
            cv2.imshow('AR Colorize - Original | Processed', combined)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key in [ord(k) for k in preset_colors.keys()]:
                color_key = chr(key)
                self.selected_color = preset_colors[color_key]
                print(f"Color changed to preset {color_key}")
        
        self.stop_camera()
    
    def stop_camera(self):
        """Stop the camera and cleanup"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Camera stopped")
    
    def set_color(self, hex_color: str):
        """Set the color to apply (hex format)"""
        self.selected_color = self.hex_to_bgr(hex_color)
        print(f"Color set to {hex_color}")


def main():
    """Main function to run the AR Colorize application"""
    parser = argparse.ArgumentParser(description='AR Colorize - Real-Time Wall Repainting System')
    parser.add_argument('--camera', type=int, default=0, help='Camera ID (default: 0)')
    parser.add_argument('--color', type=str, default='#FFFFFF', help='Initial color in hex format (default: #FFFFFF)')
    
    args = parser.parse_args()
    
    # Create and run AR Colorize
    ar_colorize = ARColorize()
    ar_colorize.set_color(args.color)
    
    try:
        ar_colorize.start_camera(args.camera)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ar_colorize.stop_camera()


if __name__ == "__main__":
    main()
