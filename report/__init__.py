"""
ShadowRecon Report Generator
Create structured JSON reports from OSINT findings
"""

import json
import os
import logging
from datetime import datetime

logger = logging.getLogger("ShadowRecon")

class ReportGenerator:
    """Generate and save OSINT reports"""
    
    def __init__(self, output_dir="scans"):
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
    
    def save_report(self, target, findings, report_type="full"):
        """
        Save findings as JSON report
        
        Args:
            target: Target identifier (username, domain, IP, email)
            findings: Dictionary of findings
            report_type: 'full', 'summary', or 'threat'
        
        Returns:
            Filepath of saved report
        """
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{target}_{report_type}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(findings, f, indent=2, default=str)
            
            logger.info(f"Report saved: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
            return None
    
    def create_summary_report(self, findings):
        """Create human-readable summary from findings"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "findings": findings,
            "analysis": self._analyze_findings(findings)
        }
        
        return summary
    
    def _analyze_findings(self, findings):
        """Analyze findings and extract key indicators"""
        analysis = {
            "type": "Unknown",
            "indicators": [],
            "risks": [],
            "recommendations": []
        }
        
        # Determine target type and extract indicators
        if 'domain' in findings:
            analysis["type"] = "Domain"
            analysis.update(self._analyze_domain(findings))
        
        elif 'ip' in findings:
            analysis["type"] = "IP Address"
            analysis.update(self._analyze_ip(findings))
        
        elif 'email' in findings:
            analysis["type"] = "Email Address"
            analysis.update(self._analyze_email(findings))
        
        elif any(key.startswith('username') for key in findings.keys()):
            analysis["type"] = "Username"
            analysis.update(self._analyze_username(findings))
        
        return analysis
    
    def _analyze_domain(self, findings):
        """Analyze domain findings"""
        indicators = []
        risks = []
        
        if findings.get('ssl', {}).get('has_ssl'):
            indicators.append("✓ Valid SSL/TLS certificate")
        else:
            risks.append("⚠️  No SSL certificate found")
        
        if findings.get('whois', {}).get('registrar'):
            indicators.append(f"Registrar: {findings['whois']['registrar']}")
        
        if findings.get('virustotal', {}).get('malicious_count', 0) > 0:
            risks.append(
                f"⚠️  Flagged by {findings['virustotal']['malicious_count']} VirusTotal vendors"
            )
        
        return {
            "indicators": indicators,
            "risks": risks
        }
    
    def _analyze_ip(self, findings):
        """Analyze IP findings"""
        indicators = []
        risks = []
        
        geo = findings.get('geolocation', {})
        if geo.get('country'):
            indicators.append(f"Location: {geo['city']}, {geo['country']}")
        
        if geo.get('isp'):
            indicators.append(f"ISP: {geo['isp']}")
        
        shodan = findings.get('shodan', {})
        if shodan and shodan.get('open_ports'):
            risks.append(f"⚠️  {len(shodan['open_ports'])} open ports detected")
        
        if findings.get('virustotal', {}).get('malicious_count', 0) > 0:
            risks.append(
                f"⚠️  Flagged by {findings['virustotal']['malicious_count']} VirusTotal vendors"
            )
        
        return {
            "indicators": indicators,
            "risks": risks
        }
    
    def _analyze_email(self, findings):
        """Analyze email findings"""
        indicators = []
        risks = []
        
        hibp = findings.get('hibp', {})
        
        if hibp.get('breach_status') == 'BREACHED':
            risks.append(
                f"🔴 Email found in {hibp.get('breach_count', 0)} known data breach(es)"
            )
            for breach in hibp.get('breaches', [])[:3]:  # Show top 3
                risks.append(f"   - {breach.get('name', 'Unknown')} ({breach.get('date', 'N/A')})")
        
        elif hibp.get('breach_status') == 'NO BREACHES':
            indicators.append("✓ No breaches detected in known databases")
        
        domain_valid = findings.get('domain_valid', {})
        if domain_valid.get('valid'):
            indicators.append("✓ Email domain is valid")
        
        return {
            "indicators": indicators,
            "risks": risks
        }
    
    def _analyze_username(self, findings):
        """Analyze username findings"""
        indicators = []
        
        summary = findings.get('summary', {})
        if summary.get('found_count', 0) > 0:
            indicators.append(f"Found on {summary['found_count']} platform(s)")
            for platform in summary.get('found_platforms', [])[:5]:
                indicators.append(f"  - {platform}")
        
        return {
            "indicators": indicators,
            "risks": []
        }
    
    def generate_html_report(self, findings, output_file=None):
        """Generate HTML report for browser viewing"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_dir, f"report_{timestamp}.html")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ShadowRecon OSINT Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; }}
                h1 {{ color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }}
                h2 {{ color: #555; margin-top: 30px; }}
                .section {{ margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #007acc; }}
                .indicator {{ padding: 8px; margin: 5px 0; background-color: #e8f5e9; border-left: 4px solid #4caf50; }}
                .risk {{ padding: 8px; margin: 5px 0; background-color: #ffebee; border-left: 4px solid #f44336; }}
                .risk_score {{ font-size: 24px; color: #f44336; font-weight: bold; }}
                pre {{ background-color: #f4f4f4; padding: 10px; overflow-x: auto; }}
                .timestamp {{ color: #999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 ShadowRecon OSINT Report</h1>
                <p class="timestamp">Generated: {datetime.now().isoformat()}</p>
                
                <div class="section">
                    <h2>Findings Summary</h2>
                    <pre>{json.dumps(findings, indent=2, default=str)}</pre>
                </div>
            </div>
        </body>
        </html>
        """
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report saved: {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"Failed to save HTML report: {str(e)}")
            return None
