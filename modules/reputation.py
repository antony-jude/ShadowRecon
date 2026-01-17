"""
ShadowRecon Reputation & Threat Intelligence Module
VirusTotal scores, malicious indicators, risk assessment
"""

import requests
import logging
from config import Config
from utils import Utils

logger = logging.getLogger("ShadowRecon")

class ReputationRecon:
    """Check reputation scores and threat intelligence"""
    
    def __init__(self, target, target_type='domain'):
        """
        Initialize reputation check
        target_type: 'domain', 'ip', or 'url'
        """
        self.target = target
        self.target_type = target_type
        self.results = {}
        
        # Validate target
        if target_type == 'domain' and not Utils.validate_domain(target):
            raise ValueError(f"Invalid domain: {target}")
        elif target_type == 'ip' and not Utils.validate_ip(target):
            raise ValueError(f"Invalid IP: {target}")
    
    def recon(self):
        """Execute full reputation check"""
        logger.info(f"Starting reputation check for {self.target_type}: {self.target}")
        
        self.results = {
            "target": self.target,
            "target_type": self.target_type,
            "timestamp": Utils.format_timestamp(),
            "virustotal": self._check_virustotal(),
            "risk_score": None,
            "risk_level": None
        }
        
        # Calculate risk score based on findings
        self.results["risk_score"] = Utils.calculate_risk_score(self.results)
        self.results["risk_level"] = Utils.get_risk_level(self.results["risk_score"])
        
        return self.results
    
    def _check_virustotal(self):
        """Check VirusTotal for malicious indicators"""
        vt_data = {
            "found": False,
            "malicious_count": 0,
            "undetected_count": 0,
            "suspicious_count": 0,
            "harmless_count": 0,
            "last_analysis_date": None,
            "last_analysis_stats": {},
            "categories": {},
            "tags": [],
            "error": None
        }
        
        if not Config.VIRUSTOTAL_API_KEY:
            vt_data["error"] = "VirusTotal API key not configured"
            logger.debug("VirusTotal API key not configured")
            return vt_data
        
        try:
            logger.debug(f"Checking VirusTotal for {self.target}")
            
            headers = {
                "x-apikey": Config.VIRUSTOTAL_API_KEY
            }
            
            # Determine which endpoint to use
            if self.target_type == 'domain':
                endpoint = f"https://www.virustotal.com/api/v3/domains/{self.target}"
            elif self.target_type == 'ip':
                endpoint = f"https://www.virustotal.com/api/v3/ip_addresses/{self.target}"
            elif self.target_type == 'url':
                # URL requires special encoding
                import urllib.parse
                encoded_url = urllib.parse.quote(self.target, safe='')
                endpoint = f"https://www.virustotal.com/api/v3/urls/{encoded_url}"
            else:
                vt_data["error"] = "Unknown target type"
                return vt_data
            
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data:
                    attributes = data['data'].get('attributes', {})
                    
                    # Extract stats
                    last_analysis = attributes.get('last_analysis_stats', {})
                    vt_data["malicious_count"] = last_analysis.get('malicious', 0)
                    vt_data["undetected_count"] = last_analysis.get('undetected', 0)
                    vt_data["suspicious_count"] = last_analysis.get('suspicious', 0)
                    vt_data["harmless_count"] = last_analysis.get('harmless', 0)
                    vt_data["last_analysis_stats"] = last_analysis
                    
                    # Extract date
                    vt_data["last_analysis_date"] = attributes.get('last_analysis_date')
                    
                    # Extract categories
                    vt_data["categories"] = attributes.get('categories', {})
                    
                    # Extract tags
                    vt_data["tags"] = attributes.get('tags', [])
                    
                    vt_data["found"] = True
                    
                    # Determine if malicious
                    if vt_data["malicious_count"] > 0:
                        logger.warning(
                            f"{self.target} flagged by {vt_data['malicious_count']} "
                            "VirusTotal vendors"
                        )
            
            elif response.status_code == 404:
                vt_data["found"] = False
                logger.debug(f"{self.target} not found in VirusTotal")
            
            elif response.status_code == 401:
                vt_data["error"] = "Invalid VirusTotal API key"
            
            elif response.status_code == 429:
                vt_data["error"] = "Rate limited by VirusTotal API"
            
            else:
                vt_data["error"] = f"HTTP {response.status_code}"
        
        except requests.Timeout:
            vt_data["error"] = "VirusTotal request timeout"
            logger.warning(f"VirusTotal timeout for {self.target}")
        
        except Exception as e:
            vt_data["error"] = str(e)
            logger.warning(f"VirusTotal error: {str(e)}")
        
        return vt_data
    
    def get_threat_summary(self):
        """Get human-readable threat summary"""
        if not self.results:
            return "No scan results available"
        
        vt = self.results.get("virustotal", {})
        
        summary = {
            "target": self.target,
            "risk_level": self.results.get("risk_level", "UNKNOWN"),
            "risk_score": self.results.get("risk_score", 0),
            "virustotal_status": "MALICIOUS" if vt.get("malicious_count", 0) > 0 else "CLEAN",
            "detections": f"{vt.get('malicious_count', 0)} malicious vendors",
            "recommendation": self._get_recommendation()
        }
        
        return summary
    
    def _get_recommendation(self):
        """Get security recommendation based on findings"""
        risk_level = self.results.get("risk_level", "MINIMAL")
        
        recommendations = {
            "CRITICAL": "⚠️  CRITICAL: Do not interact. Block immediately.",
            "HIGH": "🔴 HIGH RISK: Exercise extreme caution. Consider blocking.",
            "MEDIUM": "🟡 MEDIUM RISK: Monitor suspicious activity. Verify legitimacy.",
            "LOW": "🟢 LOW RISK: Minor concerns. Standard precautions recommended.",
            "MINIMAL": "✓ MINIMAL RISK: Appears safe. No immediate action needed."
        }
        
        return recommendations.get(risk_level, "Unknown risk profile")
