"""Catch Tracker Service - Wraps backend catch record functionality"""
from typing import Dict, Any, Optional, List
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared import SkillBase, ResponseFormatter


class CatchTrackerService(SkillBase):
    """Catch record management service
    
    Wraps backend_routes catch endpoints to provide:
    - Catch logging
    - Catch history
    - Statistics and analytics
    - CRUD operations
    """
    
    def __init__(self):
        super().__init__("catch-tracker", "1.0.0")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute catch tracker operation
        
        Args:
            action: Operation type (log/list/stats/delete)
            user_id: User ID
            fish_species: Fish species name
            weight: Fish weight in kg
            spot_id: Fishing spot ID
            image_path: Path to catch photo
            
        Returns:
            Operation results
        """
        action = kwargs.get('action', 'log')
        
        if action == 'log':
            return self.log_catch(**kwargs)
        elif action == 'list':
            return self.get_catches(**kwargs)
        elif action == 'stats':
            return self.get_statistics(**kwargs)
        elif action == 'delete':
            return self.delete_catch(**kwargs)
        else:
            return ResponseFormatter.error(f"Unknown action: {action}")
    
    def log_catch(self, user_id: str, fish_species: str, weight: float,
                  spot_id: int = None, length: float = None,
                  image_path: str = None, notes: str = None,
                  latitude: float = None, longitude: float = None) -> Dict[str, Any]:
        """Log a new catch
        
        Args:
            user_id: User ID
            fish_species: Fish species name
            weight: Fish weight in kg
            spot_id: Optional fishing spot ID
            length: Optional fish length in cm
            image_path: Optional path to catch photo
            notes: Optional notes
            latitude: Optional GPS latitude
            longitude: Optional GPS longitude
            
        Returns:
            Catch record with ID
        """
        self.validate_params(['user_id', 'fish_species', 'weight'], {
            'user_id': user_id,
            'fish_species': fish_species,
            'weight': weight
        })
        
        try:
            from backend_routes import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert catch record
            cursor.execute("""
                INSERT INTO fishing_reports 
                (user_id, fish_species, weight, length, spot_id, image_url, notes, 
                 latitude, longitude, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (user_id, fish_species, weight, length, spot_id, image_path, 
                  notes, latitude, longitude))
            
            catch_id = cursor.lastrowid
            conn.commit()
            
            # Get the created record
            cursor.execute("""
                SELECT r.*, s.name as spot_name
                FROM fishing_reports r
                LEFT JOIN fishing_spot s ON r.spot_id = s.id
                WHERE r.id = ?
            """, (catch_id,))
            
            catch_record = dict(cursor.fetchone())
            conn.close()
            
            return ResponseFormatter.success(
                data=catch_record,
                message=f"Catch logged: {fish_species} ({weight}kg)"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="LOG_ERROR"
            )
    
    def get_catches(self, user_id: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Get user's catch history
        
        Args:
            user_id: User ID
            limit: Number of records to return
            offset: Offset for pagination
            
        Returns:
            List of catch records
        """
        try:
            from backend_routes import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM fishing_reports
                WHERE user_id = ?
            """, (user_id,))
            
            total = cursor.fetchone()[0]
            
            # Get catch records
            cursor.execute("""
                SELECT r.*, s.name as spot_name
                FROM fishing_reports r
                LEFT JOIN fishing_spot s ON r.spot_id = s.id
                WHERE r.user_id = ?
                ORDER BY r.created_at DESC
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset))
            
            catches = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return ResponseFormatter.success(
                data={
                    "total": total,
                    "count": len(catches),
                    "catches": catches,
                    "pagination": {
                        "limit": limit,
                        "offset": offset,
                        "has_more": offset + limit < total
                    }
                },
                message=f"Retrieved {len(catches)} of {total} catches"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="LIST_ERROR"
            )
    
    def get_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get catch statistics for user
        
        Args:
            user_id: User ID
            
        Returns:
            Statistics summary
        """
        try:
            from backend_routes import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Total catches and weight
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_catches,
                    SUM(weight) as total_weight,
                    AVG(weight) as avg_weight,
                    MAX(weight) as max_weight,
                    COUNT(DISTINCT fish_species) as species_count
                FROM fishing_reports
                WHERE user_id = ?
            """, (user_id,))
            
            summary = dict(cursor.fetchone())
            
            # Species distribution
            cursor.execute("""
                SELECT 
                    fish_species,
                    COUNT(*) as count,
                    SUM(weight) as total_weight,
                    AVG(weight) as avg_weight
                FROM fishing_reports
                WHERE user_id = ?
                GROUP BY fish_species
                ORDER BY count DESC
                LIMIT 10
            """, (user_id,))
            
            species_dist = [dict(row) for row in cursor.fetchall()]
            
            # Favorite spot
            cursor.execute("""
                SELECT 
                    s.name as spot_name,
                    COUNT(*) as catch_count
                FROM fishing_reports r
                JOIN fishing_spot s ON r.spot_id = s.id
                WHERE r.user_id = ?
                GROUP BY r.spot_id
                ORDER BY catch_count DESC
                LIMIT 1
            """, (user_id,))
            
            favorite_spot = cursor.fetchone()
            favorite_spot = dict(favorite_spot) if favorite_spot else None
            
            conn.close()
            
            return ResponseFormatter.success(
                data={
                    "summary": summary,
                    "species_distribution": species_dist,
                    "favorite_spot": favorite_spot
                },
                message="Statistics calculated"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="STATS_ERROR"
            )
    
    def delete_catch(self, catch_id: int, user_id: str = None) -> Dict[str, Any]:
        """Delete a catch record
        
        Args:
            catch_id: Catch record ID
            user_id: Optional user ID for ownership verification
            
        Returns:
            Deletion confirmation
        """
        try:
            from backend_routes import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verify ownership if user_id provided
            if user_id:
                cursor.execute("""
                    SELECT user_id FROM fishing_reports WHERE id = ?
                """, (catch_id,))
                
                record = cursor.fetchone()
                if not record:
                    conn.close()
                    return ResponseFormatter.error(
                        error=f"Catch record not found: {catch_id}",
                        code="NOT_FOUND"
                    )
                
                if record[0] != user_id:
                    conn.close()
                    return ResponseFormatter.error(
                        error="Not authorized to delete this catch",
                        code="UNAUTHORIZED"
                    )
            
            # Delete the record
            cursor.execute("DELETE FROM fishing_reports WHERE id = ?", (catch_id,))
            conn.commit()
            conn.close()
            
            return ResponseFormatter.success(
                data={"catch_id": catch_id},
                message="Catch record deleted"
            )
        
        except Exception as e:
            return ResponseFormatter.error(
                error=str(e),
                code="DELETE_ERROR"
            )
