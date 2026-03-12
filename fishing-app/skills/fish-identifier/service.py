"""Fish Identifier Service - Wraps fusion_fish_recognition"""
from typing import Dict, Any, Optional
import sys
import os
import base64

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared import SkillBase, ResponseFormatter
from fusion_fish_recognition import recognize_fish_fusion, get_fish_tips


class FishIdentifierService(SkillBase):
    """Fish identification service using AI vision models
    
    Wraps fusion_fish_recognition to provide:
    - Fish species recognition from images
    - Fishing tips for identified species
    - Knowledge graph integration
    """
    
    def __init__(self):
        super().__init__("fish-identifier", "1.0.0")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute fish identification
        
        Args:
            image_path: Path to image file
            image_base64: Base64-encoded image data
            
        Returns:
            Recognition results with species and confidence
        """
        image_path = kwargs.get('image_path')
        image_base64 = kwargs.get('image_base64')
        
        if not image_path and not image_base64:
            return ResponseFormatter.error("Missing required parameter: image_path or image_base64")
        
        try:
            # Read image data
            if image_path:
                with open(image_path, 'rb') as f:
                    image_data = f.read()
            else:
                image_data = base64.b64decode(image_base64)
            
            # Recognize fish
            result = recognize_fish_fusion(image_data)
            
            return ResponseFormatter.success(
                data=result,
                message="Fish identification complete"
            )
        
        except FileNotFoundError:
            return ResponseFormatter.error(
                error=f"Image file not found: {image_path}",
                code="FILE_NOT_FOUND"
            )
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="RECOGNITION_ERROR"
            )
    
    def recognize(self, image_path: str = None, image_base64: str = None) -> Dict[str, Any]:
        """Recognize fish from image (convenience method)
        
        Args:
            image_path: Path to image file
            image_base64: Base64-encoded image
            
        Returns:
            Recognition results
        """
        return self.execute(image_path=image_path, image_base64=image_base64)
    
    def get_tips(self, fish_name: str) -> Dict[str, Any]:
        """Get fishing tips for a species
        
        Args:
            fish_name: Fish species name (Chinese)
            
        Returns:
            Fishing tips and techniques
        """
        try:
            tips = get_fish_tips(fish_name)
            
            if tips and tips.get("success"):
                return ResponseFormatter.success(
                    data=tips,
                    message=f"Fishing tips for {fish_name}"
                )
            else:
                return ResponseFormatter.error(
                    error=f"No tips found for {fish_name}",
                    code="NOT_FOUND"
                )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="TIPS_ERROR"
            )
