import json
import os
from datetime import datetime, timedelta
from typing import Any, Optional
from pathlib import Path


class CacheService:
    def __init__(self, cache_dir: str = "cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        safe_key = "".join(c for c in key if c.isalnum() or c in ('_', '-')).rstrip()
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            expires_at = cached_time + timedelta(hours=self.ttl_hours)
            
            if datetime.now() > expires_at:
                cache_path.unlink()
                return None
            
            return cache_data['data']
            
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def set(self, key: str, data: Any) -> bool:
        cache_path = self._get_cache_path(key)
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'key': key,
            'data': data
        }
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False

    def clear_expired(self) -> int:
        deleted = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                expires_at = cached_time + timedelta(hours=self.ttl_hours)
                
                if datetime.now() > expires_at:
                    cache_file.unlink()
                    deleted += 1
            except Exception:
                continue
        return deleted

    def clear_all(self) -> int:
        deleted = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            deleted += 1
        return deleted
