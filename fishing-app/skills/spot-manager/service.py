"""Spot Manager Service - Wraps fishing_spots_db"""
from typing import Dict, Any, Optional, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared import SkillBase, ResponseFormatter
from fishing_spots_db import FishingSpotsDatabase


class SpotManagerService(SkillBase):
    """Fishing spot search and management service
    
    Wraps FishingSpotsDatabase to provide:
    - Nearby spot search
    - Fish species filtering
    - Spot details
    - Favorites management
    """
    
    def __init__(self, db_path: str = "./data/fishing_spots.db"):
        super().__init__("spot-manager", "1.0.0")
        self.db = FishingSpotsDatabase(db_path)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute spot search
        
        Args:
            action: Action type (nearby/search/details)
            latitude: GPS latitude
            longitude: GPS longitude
            radius: Search radius in km
            fish_species: Target fish species
            spot_id: Spot ID for details
            
        Returns:
            Spot search results
        """
        action = kwargs.get('action', 'nearby')
        
        if action == 'nearby':
            return self.search_nearby(
                latitude=kwargs.get('latitude'),
                longitude=kwargs.get('longitude'),
                radius=kwargs.get('radius', 10.0),
                fish_species=kwargs.get('fish_species')
            )
        elif action == 'details':
            return self.get_spot_details(kwargs.get('spot_id'))
        else:
            return ResponseFormatter.error(f"Unknown action: {action}")
    
    def search_nearby(self, latitude: float, longitude: float, 
                     radius: float = 10.0, fish_species: str = None) -> Dict[str, Any]:
        """Search for nearby fishing spots
        
        Args:
            latitude: User latitude
            longitude: User longitude
            radius: Search radius in km (default: 10)
            fish_species: Optional fish species filter
            
        Returns:
            List of nearby spots with distances
        """
        self.validate_params(['latitude', 'longitude'], {
            'latitude': latitude,
            'longitude': longitude
        })
        
        try:
            spots = self.db.search_nearby(latitude, longitude, radius_km=radius)
            
            # Filter by fish species if specified
            if fish_species:
                spots = [s for s in spots if fish_species in (s.fish_species or [])]
            
            # Convert to dict format
            spots_data = [self._spot_to_dict(s) for s in spots]
            
            return ResponseFormatter.success(
                data={
                    "count": len(spots_data),
                    "spots": spots_data,
                    "search_params": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "radius": radius,
                        "fish_species": fish_species
                    }
                },
                message=f"Found {len(spots_data)} spots within {radius}km"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="SEARCH_ERROR"
            )
    
    def search_by_fish(self, fish_species: str, city: str = None) -> Dict[str, Any]:
        """Search spots by fish species
        
        Args:
            fish_species: Target fish species
            city: Optional city filter
            
        Returns:
            List of spots with target fish
        """
        try:
            spots = self.db.search_by_fish_species(fish_species)
            
            # Filter by city if specified
            if city:
                spots = [s for s in spots if city in (s.address or "")]
            
            spots_data = [self._spot_to_dict(s) for s in spots]
            
            return ResponseFormatter.success(
                data={
                    "count": len(spots_data),
                    "spots": spots_data,
                    "fish_species": fish_species
                },
                message=f"Found {len(spots_data)} spots for {fish_species}"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="SEARCH_ERROR"
            )
    
    def get_spot_details(self, spot_id: int) -> Dict[str, Any]:
        """Get detailed information for a spot
        
        Args:
            spot_id: Spot ID
            
        Returns:
            Spot details
        """
        try:
            spot = self.db.get_spot_by_id(spot_id)
            
            if not spot:
                return ResponseFormatter.error(
                    error=f"Spot not found: {spot_id}",
                    code="NOT_FOUND"
                )
            
            return ResponseFormatter.success(
                data=self._spot_to_dict(spot),
                message="Spot details retrieved"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="DETAILS_ERROR"
            )
    
    def list_spots(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """List all spots with pagination
        
        Args:
            limit: Number of spots to return
            offset: Offset for pagination
            
        Returns:
            List of spots
        """
        try:
            all_spots = self.db.get_all_spots()
            total = len(all_spots)
            spots = all_spots[offset:offset + limit]
            
            spots_data = [self._spot_to_dict(s) for s in spots]
            
            return ResponseFormatter.success(
                data={
                    "count": len(spots_data),
                    "total": total,
                    "spots": spots_data,
                    "pagination": {
                        "limit": limit,
                        "offset": offset,
                        "has_more": offset + limit < total
                    }
                },
                message=f"Retrieved {len(spots_data)} of {total} spots"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="LIST_ERROR"
            )
    
    def _spot_to_dict(self, spot) -> Dict[str, Any]:
        """Convert spot object to dictionary
        
        Args:
            spot: Spot object
            
        Returns:
            Spot dictionary
        """
        return {
            "id": spot.id,
            "name": spot.name,
            "latitude": spot.latitude,
            "longitude": spot.longitude,
            "address": spot.address,
            "fish_species": spot.fish_species,
            "water_type": spot.water_type,
            "difficulty": spot.difficulty,
            "fee": spot.fee,
            "rating": spot.rating,
            "distance": getattr(spot, 'distance', None)
        }
