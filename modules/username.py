"""
ShadowRecon Username Reconnaissance Module
Asynchronously check username existence across multiple platforms
"""

import asyncio
import aiohttp
import logging
from config import Config
from utils import Utils

logger = logging.getLogger("ShadowRecon")

class UsernameRecon:
    """Check username existence across platforms"""
    
    def __init__(self):
        self.platforms = Config.USERNAME_PLATFORMS
        self.timeout = aiohttp.ClientTimeout(total=Config.ASYNC_TIMEOUT)
        self.results = {}
    
    async def check_username(self, username):
        """
        Asynchronously check username on all platforms
        Returns dict with platform, URL, status, and HTTP response code
        """
        logger.info(f"Starting username reconnaissance for: {username}")
        
        if not username or len(username) < 3:
            logger.warning("Username too short or invalid")
            return {"error": "Username must be at least 3 characters"}
        
        self.results = {}
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [
                self._check_platform(session, platform, username)
                for platform in self.platforms.keys()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return self.results
    
    async def _check_platform(self, session, platform, username):
        """Check if username exists on a specific platform"""
        try:
            url = self.platforms[platform].format(Utils.sanitize_username(username))
            
            async with session.head(url, allow_redirects=True, ssl=False) as response:
                # Status code logic for different platforms
                exists = self._interpret_status(response.status, platform)
                
                self.results[platform] = {
                    "url": url,
                    "status": "FOUND" if exists else "NOT FOUND",
                    "http_code": response.status,
                    "accessible": response.status not in [403, 404, 410]
                }
                
                logger.debug(f"{platform}: {response.status} - {self.results[platform]['status']}")
        
        except asyncio.TimeoutError:
            self.results[platform] = {
                "url": self.platforms[platform].format(username),
                "status": "TIMEOUT",
                "http_code": None,
                "accessible": False
            }
            logger.warning(f"{platform}: Request timeout")
        
        except Exception as e:
            self.results[platform] = {
                "url": self.platforms[platform].format(username),
                "status": "ERROR",
                "http_code": None,
                "accessible": False,
                "error": str(e)
            }
            logger.debug(f"{platform}: {str(e)}")
    
    @staticmethod
    def _interpret_status(status_code, platform):
        """
        Interpret HTTP status codes
        Different platforms return different codes for existing/non-existing users
        """
        # 200-299: Generally means found
        if 200 <= status_code < 300:
            return True
        
        # 301-302: Redirect (might indicate found for some platforms)
        if status_code in [301, 302]:
            return True
        
        # 404: Usually not found
        if status_code == 404:
            return False
        
        # 403: Forbidden (sometimes means found but private)
        if status_code == 403:
            return True
        
        # 429: Rate limited (be cautious)
        if status_code == 429:
            return False
        
        return False
    
    def get_summary(self):
        """Get summary of found usernames"""
        found = [p for p, r in self.results.items() if r.get("status") == "FOUND"]
        not_found = [p for p, r in self.results.items() if r.get("status") == "NOT FOUND"]
        
        return {
            "found_count": len(found),
            "not_found_count": len(not_found),
            "found_platforms": found,
            "not_found_platforms": not_found,
            "total_checked": len(self.results)
        }
