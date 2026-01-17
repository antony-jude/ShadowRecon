"""
ShadowRecon Main Entry Point
Interactive CLI for OSINT framework
"""

import asyncio
import sys
import logging
from config import Config, logger
from modules import UsernameRecon, DomainRecon, IPRecon, EmailRecon, ReputationRecon
from report import ReportGenerator
from utils import Utils

class ShadowRecon:
    """Main OSINT framework controller"""
    
    def __init__(self):
        self.reporter = ReportGenerator()
        self.logger = logger
    
    async def recon_username(self, username):
        """Execute username reconnaissance"""
        try:
            recon = UsernameRecon()
            results = await recon.check_username(username)
            summary = recon.get_summary()
            
            findings = {
                "username": username,
                "timestamp": Utils.format_timestamp(),
                "platforms_checked": results,
                "summary": summary,
                "risk_score": 0,  # Username alone has minimal risk
                "risk_level": "MINIMAL"
            }
            
            # Save report
            self.reporter.save_report(username, findings, "username")
            
            return findings
        
        except Exception as e:
            self.logger.error(f"Username recon error: {str(e)}")
            return {"error": str(e)}
    
    def recon_domain(self, domain):
        """Execute domain reconnaissance"""
        try:
            recon = DomainRecon(domain)
            findings = recon.recon()
            
            # Add reputation check
            try:
                rep = ReputationRecon(domain, 'domain')
                reputation = rep.recon()
                findings["reputation"] = reputation
            except:
                pass
            
            # Calculate risk score
            findings["risk_score"] = Utils.calculate_risk_score(findings)
            findings["risk_level"] = Utils.get_risk_level(findings["risk_score"])
            
            # Save report
            self.reporter.save_report(domain, findings, "domain")
            
            return findings
        
        except Exception as e:
            self.logger.error(f"Domain recon error: {str(e)}")
            return {"error": str(e)}
    
    def recon_ip(self, ip):
        """Execute IP reconnaissance"""
        try:
            recon = IPRecon(ip)
            findings = recon.recon()
            
            # Add reputation check
            try:
                rep = ReputationRecon(ip, 'ip')
                reputation = rep.recon()
                findings["reputation"] = reputation
            except:
                pass
            
            # Save report
            self.reporter.save_report(ip, findings, "ip")
            
            return findings
        
        except Exception as e:
            self.logger.error(f"IP recon error: {str(e)}")
            return {"error": str(e)}
    
    def recon_email(self, email):
        """Execute email reconnaissance"""
        try:
            recon = EmailRecon(email)
            findings = recon.recon()
            
            # Calculate risk
            if findings["hibp"]["breach_status"] == "BREACHED":
                findings["risk_score"] = 75
                findings["risk_level"] = "HIGH"
            else:
                findings["risk_score"] = 10
                findings["risk_level"] = "MINIMAL"
            
            # Save report
            self.reporter.save_report(email, findings, "email")
            
            return findings
        
        except Exception as e:
            self.logger.error(f"Email recon error: {str(e)}")
            return {"error": str(e)}
    
    def display_results(self, results, title=None):
        """Display results in formatted output"""
        if title:
            print(f"\n{'='*70}")
            print(f"  {title}")
            print(f"{'='*70}\n")
        
        if "error" in results:
            print(f"❌ Error: {results['error']}")
            return
        
        # Display findings
        self._print_dict(results, indent=0)
        
        # Display risk assessment if available
        if "risk_score" in results or "risk_level" in results:
            print(f"\n{'─'*70}")
            print(f"RISK ASSESSMENT")
            print(f"{'─'*70}")
            print(f"Risk Score:  {results.get('risk_score', 'N/A')}/100")
            print(f"Risk Level:  {results.get('risk_level', 'UNKNOWN')}")
    
    def _print_dict(self, d, indent=0):
        """Recursively print dictionary with formatting"""
        if not isinstance(d, dict):
            print(f"{str(d)}")
            return
        
        for key, value in d.items():
            if key in ['timestamp', 'url']:
                continue
            
            prefix = "  " * indent
            
            if isinstance(value, dict):
                print(f"{prefix}{key}:")
                self._print_dict(value, indent + 1)
            
            elif isinstance(value, list):
                if len(value) == 0:
                    print(f"{prefix}{key}: []")
                elif len(value) <= 3:
                    print(f"{prefix}{key}: {value}")
                else:
                    print(f"{prefix}{key}:")
                    for item in value:
                        print(f"{prefix}  - {item}")
            
            else:
                print(f"{prefix}{key}: {value}")

def show_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("  🔍 ShadowRecon - Advanced OSINT Framework")
    print("="*70)
    print("\n[1] Username Reconnaissance")
    print("[2] Domain Reconnaissance")
    print("[3] IP Address Reconnaissance")
    print("[4] Email Reconnaissance")
    print("[5] Reputation & Threat Intel")
    print("[0] Exit")
    print("\n" + "─"*70)

def get_input(prompt, validation_func=None):
    """Get and validate user input"""
    while True:
        user_input = input(prompt).strip()
        
        if not user_input:
            print("⚠️  Input cannot be empty")
            continue
        
        if validation_func and not validation_func(user_input):
            print("⚠️  Invalid input format")
            continue
        
        return user_input

async def main():
    """Main application loop"""
    framework = ShadowRecon()
    
    print("\n🚀 Starting ShadowRecon OSINT Framework...")
    print(f"📝 Logs saved to: {Config.LOG_FILE}")
    print(f"📊 Reports saved to: scans/")
    
    while True:
        show_menu()
        choice = input("Select option (0-5): ").strip()
        
        if choice == "0":
            print("\n✅ Exiting ShadowRecon. Thank you!")
            break
        
        elif choice == "1":
            # Username Recon
            username = get_input("\n👤 Enter username: ")
            print("\n⏳ Checking platforms (async)...")
            
            results = await framework.recon_username(username)
            framework.display_results(results, f"Username Reconnaissance: {username}")
            
            summary = results.get("summary", {})
            print(f"\n📊 Found on {summary.get('found_count', 0)} platform(s)")
        
        elif choice == "2":
            # Domain Recon
            domain = get_input("\n🌐 Enter domain: ", Utils.validate_domain)
            print("\n⏳ Gathering domain intelligence...")
            
            results = framework.recon_domain(domain)
            framework.display_results(results, f"Domain Reconnaissance: {domain}")
        
        elif choice == "3":
            # IP Recon
            ip = get_input("\n🖥️  Enter IP address: ", Utils.validate_ip)
            print("\n⏳ Analyzing IP address...")
            
            results = framework.recon_ip(ip)
            framework.display_results(results, f"IP Reconnaissance: {ip}")
        
        elif choice == "4":
            # Email Recon
            email = get_input("\n📧 Enter email address: ", Utils.validate_email)
            print("\n⏳ Checking email security databases...")
            
            results = framework.recon_email(email)
            
            # Enhanced email display
            framework.display_results(results, f"Email Reconnaissance: {email}")
            
            hibp = results.get("hibp", {})
            if hibp.get("breach_status") == "BREACHED":
                print(f"\n🚨 ALERT: Email found in {hibp.get('breach_count', 0)} breach(es):")
                for breach in hibp.get("breaches", []):
                    print(f"  - {breach.get('name')} ({breach.get('date')})")
            else:
                print("\n✅ No breaches detected in HaveIBeenPwned database")
        
        elif choice == "5":
            # Reputation Check
            print("\n🎯 Reputation & Threat Intelligence")
            print("[1] Domain reputation")
            print("[2] IP reputation")
            
            rep_choice = input("Select target type (1-2): ").strip()
            
            if rep_choice == "1":
                domain = get_input("\n🌐 Enter domain: ", Utils.validate_domain)
                print("\n⏳ Checking threat intelligence...")
                
                rep = ReputationRecon(domain, 'domain')
                results = rep.recon()
                framework.display_results(results, f"Reputation Check: {domain}")
                print(f"\n{rep.get_threat_summary()['recommendation']}")
            
            elif rep_choice == "2":
                ip = get_input("\n🖥️  Enter IP address: ", Utils.validate_ip)
                print("\n⏳ Checking threat intelligence...")
                
                rep = ReputationRecon(ip, 'ip')
                results = rep.recon()
                framework.display_results(results, f"Reputation Check: {ip}")
                print(f"\n{rep.get_threat_summary()['recommendation']}")
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Framework terminated by user")
        sys.exit(0)
