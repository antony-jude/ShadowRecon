"""
ShadowRecon Domain Reconnaissance Module
WHOIS lookup, DNS resolution, SSL certificate details, hosting IP extraction
"""

import socket
import logging
import ssl
import subprocess
import json
from datetime import datetime

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

from utils import Utils

logger = logging.getLogger("ShadowRecon")

class DomainRecon:
    """Comprehensive domain reconnaissance"""
    
    def __init__(self, domain):
        if not Utils.validate_domain(domain):
            raise ValueError(f"Invalid domain format: {domain}")
        
        self.domain = domain.lower()
        self.results = {}
    
    def recon(self):
        """Execute full domain reconnaissance"""
        logger.info(f"Starting domain reconnaissance for: {self.domain}")
        
        self.results = {
            "domain": self.domain,
            "timestamp": Utils.format_timestamp(),
            "whois": self._get_whois(),
            "dns": self._get_dns_records(),
            "ssl": self._get_ssl_certificate(),
            "hosting_ip": self._get_hosting_ip()
        }
        
        return self.results
    
    def _get_whois(self):
        """Fetch WHOIS information"""
        if not WHOIS_AVAILABLE:
            logger.warning("WHOIS module not available")
            return {"error": "whois package not installed"}
        
        try:
            logger.debug(f"Fetching WHOIS for {self.domain}")
            w = whois.whois(self.domain)
            
            whois_data = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "updated_date": str(w.updated_date),
                "status": w.status,
                "name_servers": w.name_servers if w.name_servers else [],
                "registrant": w.registrant_name if hasattr(w, 'registrant_name') else "Unknown",
                "registrant_email": w.registrant_email if hasattr(w, 'registrant_email') else "Unknown",
            }
            
            return whois_data
        
        except Exception as e:
            logger.warning(f"WHOIS lookup failed: {str(e)}")
            return {"error": str(e)}
    
    def _get_dns_records(self):
        """Resolve DNS records (A, MX, NS)"""
        dns_data = {
            "a_records": [],
            "mx_records": [],
            "ns_records": [],
            "txt_records": []
        }
        
        if not DNS_AVAILABLE:
            logger.warning("DNS resolver not available")
            return dns_data
        
        try:
            # A Records (IPv4 addresses)
            try:
                a_answers = dns.resolver.resolve(self.domain, 'A')
                dns_data["a_records"] = [str(rdata) for rdata in a_answers]
            except:
                pass
            
            # MX Records (Mail servers)
            try:
                mx_answers = dns.resolver.resolve(self.domain, 'MX')
                dns_data["mx_records"] = [str(rdata) for rdata in mx_answers]
            except:
                pass
            
            # NS Records (Nameservers)
            try:
                ns_answers = dns.resolver.resolve(self.domain, 'NS')
                dns_data["ns_records"] = [str(rdata) for rdata in ns_answers]
            except:
                pass
            
            # TXT Records (SPF, DKIM, DMARC)
            try:
                txt_answers = dns.resolver.resolve(self.domain, 'TXT')
                dns_data["txt_records"] = [str(rdata) for rdata in txt_answers]
            except:
                pass
            
            logger.debug(f"DNS resolution successful for {self.domain}")
        
        except Exception as e:
            logger.warning(f"DNS resolution error: {str(e)}")
        
        return dns_data
    
    def _get_ssl_certificate(self):
        """Extract SSL certificate details"""
        ssl_data = {
            "has_ssl": False,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "valid": False,
            "error": None
        }
        
        try:
            logger.debug(f"Fetching SSL certificate for {self.domain}")
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        ssl_data["has_ssl"] = True
                        
                        # Extract subject
                        subject = dict(x[0] for x in cert.get('subject', []))
                        ssl_data["subject"] = subject.get('commonName', 'Unknown')
                        
                        # Extract issuer
                        issuer = dict(x[0] for x in cert.get('issuer', []))
                        ssl_data["issuer"] = issuer.get('commonName', 'Unknown')
                        
                        # Extract dates
                        ssl_data["valid_from"] = cert.get('notBefore', 'Unknown')
                        ssl_data["valid_until"] = cert.get('notAfter', 'Unknown')
                        
                        # Check validity
                        ssl_data["valid"] = True
        
        except ssl.SSLError as e:
            ssl_data["error"] = f"SSL Error: {str(e)}"
            logger.debug(f"SSL error for {self.domain}: {str(e)}")
        
        except socket.timeout:
            ssl_data["error"] = "Connection timeout"
            logger.debug(f"SSL connection timeout for {self.domain}")
        
        except Exception as e:
            ssl_data["error"] = str(e)
            logger.debug(f"SSL certificate fetch error: {str(e)}")
        
        return ssl_data
    
    def _get_hosting_ip(self):
        """Get hosting IP address"""
        try:
            logger.debug(f"Resolving IP for {self.domain}")
            ip = socket.gethostbyname(self.domain)
            
            return {
                "ip": ip,
                "resolved": True
            }
        
        except socket.gaierror:
            return {
                "ip": None,
                "resolved": False,
                "error": "Could not resolve domain"
            }
        
        except Exception as e:
            return {
                "ip": None,
                "resolved": False,
                "error": str(e)
            }
