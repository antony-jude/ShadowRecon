"""
ShadowRecon IP Reconnaissance Module
Geolocation, open ports/services (Shodan), ASN, organization, risk indicators
"""

import requests
import logging
from config import Config
from utils import Utils

logger = logging.getLogger("ShadowRecon")

class IPRecon:
    """Comprehensive IP address reconnaissance"""
    
    def __init__(self, ip_address):
        if not Utils.validate_ip(ip_address):
            raise ValueError(f"Invalid IP format: {ip_address}")
        
        self.ip = ip_address
        self.results = {}
    
    def recon(self):
        """Execute full IP reconnaissance"""
        logger.info(f"Starting IP reconnaissance for: {self.ip}")
        
        self.results = {
            "ip": self.ip,
            "timestamp": Utils.format_timestamp(),
            "geolocation": self._get_geolocation(),
            "shodan": self._get_shodan_data() if Config.ENABLE_SHODAN else None,
            "asn": self._get_asn_info(),
            "organization": self._get_organization(),
        }
        
        return self.results
    
    def _get_geolocation(self):
        """Get geolocation from IP address"""
        geo_data = {
            "country": None,
            "country_code": None,
            "city": None,
            "latitude": None,
            "longitude": None,
            "isp": None,
            "timezone": None,
            "error": None
        }
        
        try:
            logger.debug(f"Fetching geolocation for {self.ip}")
            
            # Using ip-api.com (free tier available)
            response = requests.get(
                f"http://ip-api.com/json/{self.ip}",
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    geo_data = {
                        "country": data.get('country'),
                        "country_code": data.get('countryCode'),
                        "city": data.get('city'),
                        "latitude": data.get('lat'),
                        "longitude": data.get('lon'),
                        "isp": data.get('isp'),
                        "timezone": data.get('timezone'),
                        "error": None
                    }
                else:
                    geo_data["error"] = "IP geolocation failed"
            else:
                geo_data["error"] = f"HTTP {response.status_code}"
        
        except requests.Timeout:
            geo_data["error"] = "Request timeout"
            logger.warning(f"Geolocation timeout for {self.ip}")
        
        except Exception as e:
            geo_data["error"] = str(e)
            logger.warning(f"Geolocation error: {str(e)}")
        
        return geo_data
    
    def _get_shodan_data(self):
        """Fetch Shodan data for open ports and services"""
        shodan_data = {
            "open_ports": [],
            "services": [],
            "vulnerabilities": [],
            "hostnames": [],
            "error": None
        }
        
        if not Config.SHODAN_API_KEY:
            shodan_data["error"] = "Shodan API key not configured"
            logger.debug("Shodan API key not configured")
            return shodan_data
        
        try:
            logger.debug(f"Fetching Shodan data for {self.ip}")
            
            response = requests.get(
                f"https://api.shodan.io/shodan/host/{self.ip}",
                params={"key": Config.SHODAN_API_KEY},
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract ports
                ports = data.get('ports', [])
                shodan_data["open_ports"] = ports
                
                # Extract services
                for item in data.get('data', []):
                    service = {
                        "port": item.get('port'),
                        "protocol": item.get('_shodan', {}).get('module'),
                        "product": item.get('product'),
                        "version": item.get('version'),
                        "banner": item.get('data')[:100] if item.get('data') else None
                    }
                    shodan_data["services"].append(service)
                
                # Extract hostnames
                shodan_data["hostnames"] = data.get('hostnames', [])
            
            elif response.status_code == 401:
                shodan_data["error"] = "Invalid Shodan API key"
            
            else:
                shodan_data["error"] = f"HTTP {response.status_code}"
        
        except requests.Timeout:
            shodan_data["error"] = "Shodan request timeout"
            logger.warning(f"Shodan timeout for {self.ip}")
        
        except Exception as e:
            shodan_data["error"] = str(e)
            logger.debug(f"Shodan error: {str(e)}")
        
        return shodan_data
    
    def _get_asn_info(self):
        """Get ASN (Autonomous System Number) information"""
        asn_data = {
            "asn": None,
            "asn_name": None,
            "prefix": None,
            "error": None
        }
        
        try:
            logger.debug(f"Fetching ASN info for {self.ip}")
            
            # Using ASNdb API
            response = requests.get(
                f"https://api.asndb.net/v2/ip/{self.ip}",
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    asn_data = {
                        "asn": data['data'].get('asn'),
                        "asn_name": data['data'].get('name'),
                        "prefix": data['data'].get('prefix'),
                        "error": None
                    }
        
        except Exception as e:
            logger.debug(f"ASN lookup error: {str(e)}")
        
        return asn_data
    
    def _get_organization(self):
        """Get organization/ISP details"""
        org_data = {
            "organization": None,
            "isp": None,
            "type": None,
            "error": None
        }
        
        try:
            # Using TeamCymru whois
            logger.debug(f"Fetching organization for {self.ip}")
            
            response = requests.get(
                f"https://ip.teredo.pro/whois.php?ip={self.ip}",
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    if 'Organization' in line:
                        org_data["organization"] = line.split(':', 1)[1].strip()
                    elif 'ISP' in line:
                        org_data["isp"] = line.split(':', 1)[1].strip()
                    elif 'Type' in line:
                        org_data["type"] = line.split(':', 1)[1].strip()
        
        except Exception as e:
            logger.debug(f"Organization lookup error: {str(e)}")
        
        return org_data
