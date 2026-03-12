"""Social Manager Service
Backend wrapper for posts, comments and likes.
Uses the project's DB connection via backend_routes.get_db_connection().
"""
from __future__ import annotations

import json
import datetime
from typing import List, Optional, Dict, Any

from backend_routes import get_db_connection
from shared.skill_base import SkillBase
from shared.response_formatter import ResponseFormatter


class SocialService(SkillBase):
    """Lightweight service wrapper following project conventions."""

    def __init__(self):
        super().__init__(name="social-manager", version="0.1.0")

    # Convenience helper
    def _fmt(self, payload: Any) -> Dict[str, Any]:
        return ResponseFormatter.success(payload) if isinstance(payload, dict) else ResponseFormatter.success(payload)

    @staticmethod
    def _db_commit(conn) -> None:
        if conn:
            try:
                conn.commit()
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

def _get_conn():
    return get_db_connection()


def create_post(user_id: int, content: str, images: Optional[List[str]] = None, spot_id: Optional[int] = None) -> Dict[str, Any]:
    images_json = json.dumps(images or [])
    conn = _get_conn()
    try:
        cur = conn.cursor()
        # Assumes a posts table with appropriate columns
        cur.execute(
            "INSERT INTO posts (user_id, content, images, spot_id, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (user_id, content, images_json, spot_id, datetime.datetime.utcnow()),
        )
        row = cur.fetchone()
        post_id = row[0] if row else None
        conn.commit()
        cur.close()
        return {"success": True, "post_id": post_id}
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def get_posts(user_id: int, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, user_id, content, images, spot_id, created_at FROM posts WHERE user_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (user_id, limit, offset),
        )
        rows = cur.fetchall()
        posts = []
        for r in rows:
            posts.append({
                "id": r[0],
                "user_id": r[1],
                "content": r[2],
                "images": json.loads(r[3]) if r[3] else [],
                "spot_id": r[4],
                "created_at": r[5].isoformat() if hasattr(r[5], "isoformat") else str(r[5]),
            })
        cur.close()
        return {"success": True, "posts": posts}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def delete_post(post_id: int, user_id: int) -> Dict[str, Any]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM posts WHERE id=%s", (post_id,))
        row = cur.fetchone()
        if not row:
            return {"success": False, "error": "Post not found"}
        owner = row[0]
        if owner != user_id:
            return {"success": False, "error": "Unauthorized"}
        cur.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        cur.execute("DELETE FROM comments WHERE post_id=%s", (post_id,))
        cur.execute("DELETE FROM likes WHERE post_id=%s", (post_id,))
        conn.commit()
        cur.close()
        return {"success": True}
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def add_comment(post_id: int, user_id: int, content: str) -> Dict[str, Any]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM posts WHERE id=%s", (post_id,))
        if not cur.fetchone():
            return {"success": False, "error": "Post not found"}
        cur.execute(
            "INSERT INTO comments (post_id, user_id, content, created_at) VALUES (%s, %s, %s, %s) RETURNING id",
            (post_id, user_id, content, datetime.datetime.utcnow()),
        )
        row = cur.fetchone()
        comment_id = row[0] if row else None
        conn.commit()
        cur.close()
        return {"success": True, "comment_id": comment_id}
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def get_comments(post_id: int, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, user_id, content, created_at FROM comments WHERE post_id=%s ORDER BY created_at ASC LIMIT %s OFFSET %s",
            (post_id, limit, offset),
        )
        rows = cur.fetchall()
        comments = [
            {
                "id": r[0],
                "user_id": r[1],
                "content": r[2],
                "created_at": r[3].isoformat() if hasattr(r[3], "isoformat") else str(r[3]),
            }
            for r in rows
        ]
        cur.close()
        return {"success": True, "comments": comments}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def like_post(post_id: int, user_id: int) -> Dict[str, Any]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM posts WHERE id=%s", (post_id,))
        if not cur.fetchone():
            return {"success": False, "error": "Post not found"}
        cur.execute("SELECT 1 FROM likes WHERE post_id=%s AND user_id=%s", (post_id, user_id))
        if cur.fetchone():
            return {"success": False, "error": "Already liked"}
        cur.execute("INSERT INTO likes (post_id, user_id, created_at) VALUES (%s, %s, %s)", (post_id, user_id, datetime.datetime.utcnow()))
        conn.commit()
        cur.close()
        return {"success": True}
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def unlike_post(post_id: int, user_id: int) -> Dict[str, Any]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM likes WHERE post_id=%s AND user_id=%s", (post_id, user_id))
        conn.commit()
        cur.close()
        return {"success": True}
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return {"success": False, "error": str(e)}
    finally:
        try:
            conn.close()
        except Exception:
            pass


__all__ = [
    "SocialService",
    "create_post",
    "get_posts",
    "delete_post",
    "add_comment",
    "get_comments",
    "like_post",
    "unlike_post",
]
