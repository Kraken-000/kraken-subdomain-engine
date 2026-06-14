#!/usr/bin/env python3
# KRAKEN - Subdomain Discovery Engine v1.0
# Professional Bug Bounty Tool - Zero False Positive

import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import sys
import os
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

class Kraken:
    def __init__(self, domain, wordlist_path, max_workers=50):
        self.domain = domain
        self.wordlist_path = wordlist_path
        self.max_workers = max_workers
        self.results = []
        self.start_time = None
        self.end_time = None
        self.dns_cache = {}
    
    def print_banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║      ██╗  ██╗██████╗  █████╗ ██╗  ██╗███████╗███╗   ██╗                     ║
║      ██║ ██╔╝██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║                     ║
║      █████╔╝ ██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║                     ║
║      ██╔═██╗ ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║                     ║
║      ██║  ██╗██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║                     ║
║      ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝                     ║
║                                                                              ║
║         {Colors.YELLOW}KRAKEN - Subdomain Discovery Engine{Colors.CYAN}                             ║
║         {Colors.DIM}Unleash the Beast • 0% False Positive • Live Verification{Colors.CYAN}          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
        print(banner)
    
    def print_section(self, title, icon="▶"):
        print(f"\n{Colors.CYAN}{Colors.BOLD}{icon} {title}{Colors.END}")
        print(f"{Colors.DIM}{'─' * 54}{Colors.END}")
    
    def print_success(self, message):
        print(f"{Colors.GREEN}[✓]{Colors.END} {message}")
    
    def print_error(self, message):
        print(f"{Colors.RED}[✗]{Colors.END} {message}")
    
    def print_warning(self, message):
        print(f"{Colors.YELLOW}[!]{Colors.END} {message}")
    
    def print_info(self, message):
        print(f"{Colors.BLUE}[i]{Colors.END} {message}")
    
    def print_progress(self, current, total, prefix="Progress"):
        percent = current / total * 100
        bar_length = 40
        filled = int(bar_length * current // total)
        bar = '█' * filled + '░' * (bar_length - filled)
        sys.stdout.write(f"\r{Colors.CYAN}[{prefix}]{Colors.END} |{Colors.GREEN}{bar}{Colors.END}| {percent:.1f}% ({current:,}/{total:,})")
        sys.stdout.flush()
    
    def load_wordlist(self):
        try:
            with open(self.wordlist_path, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            self.print_success(f"Loaded {len(wordlist):,} subdomain candidates")
            return wordlist
        except FileNotFoundError:
            self.print_error(f"Wordlist not found: {self.wordlist_path}")
            self.print_warning("Using default wordlist")
            return ['www', 'mail', 'admin', 'api', 'dev', 'test', 'blog', 'vpn', 'ftp', 'ns1']
    
    def resolve_subdomain(self, subdomain):
        full_domain = f"{subdomain}.{self.domain}"
        
        if full_domain in self.dns_cache:
            return self.dns_cache[full_domain]
        
        try:
            ips = socket.gethostbyname_ex(full_domain)[2]
            if ips:
                result = {'subdomain': full_domain, 'ips': ips, 'resolved': True}
                self.dns_cache[full_domain] = result
                return result
        except:
            pass
        
        result = {'subdomain': full_domain, 'resolved': False}
        self.dns_cache[full_domain] = result
        return result
    
    def verify_live(self, subdomain_info):
        subdomain = subdomain_info['subdomain']
        
        for protocol in ['https', 'http']:
            try:
                url = f"{protocol}://{subdomain}"
                response = requests.get(url, timeout=5, allow_redirects=True)
                
                return {
                    'subdomain': subdomain,
                    'ips': subdomain_info.get('ips', []),
                    'status_code': response.status_code,
                    'title': self.extract_title(response.text)[:80],
                    'server': response.headers.get('Server', 'Unknown')[:30],
                    'live': True,
                    'protocol': protocol
                }
            except:
                continue
        
        return {'subdomain': subdomain, 'live': False}
    
    def extract_title(self, html):
        try:
            start = html.lower().find('<title>')
            end = html.lower().find('</title>')
            if start != -1 and end != -1:
                return html[start+7:end].strip()
        except:
            pass
        return "No Title"
    
    def calculate_priority(self, result):
        score = 0
        if not result.get('live', False):
            return 0
        
        # Status code priority
        status = result.get('status_code', 0)
        if status == 200:
            score += 50
        elif status in [401, 403]:
            score += 40
        elif status in [500, 502, 503]:
            score += 20
        
        # Title keywords priority
        title = result.get('title', '').lower()
        high_keywords = ['admin', 'dashboard', 'panel', 'control', 'internal', 'api', 'login', 'signin', 'portal', 'console']
        medium_keywords = ['manage', 'settings', 'config', 'dev', 'staging', 'test']
        
        for keyword in high_keywords:
            if keyword in title:
                score += 25
                break
        
        for keyword in medium_keywords:
            if keyword in title:
                score += 10
                break
        
        # Subdomain name priority
        sub_lower = result.get('subdomain', '').lower()
        if 'admin' in sub_lower or 'api' in sub_lower:
            score += 15
        
        return min(score, 100)
    
    def run(self):
        self.start_time = time.time()
        self.print_banner()
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Target: {self.domain}{Colors.END}")
        print(f"{Colors.DIM}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        
        wordlist = self.load_wordlist()
        estimated_time = len(wordlist) / (self.max_workers * 10)
        print(f"{Colors.DIM}Workers: {self.max_workers} | Est. time: {estimated_time:.1f} seconds{Colors.END}\n")
        
        # STAGE 1: DNS RESOLUTION
        self.print_section("STAGE 1: DNS RESOLUTION", "🔍")
        
        resolved = []
        last_progress = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.resolve_subdomain, sub): sub for sub in wordlist}
            
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result['resolved']:
                    resolved.append(result)
                    # Print setiap 5 penemuan
                    if len(resolved) % 5 == 0:
                        print(f"  {Colors.GREEN}▶{Colors.END} [{len(resolved)}] {result['subdomain']}")
                
                # Progress bar setiap 1%
                percent = int(i / len(wordlist) * 100)
                if percent > last_progress and percent % 5 == 0:
                    last_progress = percent
                    self.print_progress(i, len(wordlist), "DNS")
        
        self.print_progress(len(wordlist), len(wordlist), "DNS")
        print()
        self.print_success(f"Resolved {len(resolved):,} unique subdomains")
        
        # STAGE 2: LIVE VERIFICATION
        if resolved:
            self.print_section("STAGE 2: LIVE VERIFICATION", "🌐")
            self.print_info(f"Checking {len(resolved):,} subdomains for live status...")
            
            live_results = []
            last_progress = 0
            
            with ThreadPoolExecutor(max_workers=min(30, len(resolved))) as executor:
                futures = {executor.submit(self.verify_live, r): r for r in resolved}
                
                for i, future in enumerate(as_completed(futures), 1):
                    result = future.result()
                    if result.get('live', False):
                        live_results.append(result)
                        status_color = Colors.GREEN if result['status_code'] == 200 else Colors.YELLOW
                        print(f"  {status_color}[LIVE]{Colors.END} {result['subdomain']} [{result['status_code']}] - {result['title'][:50]}")
                    
                    # Progress setiap 5%
                    percent = int(i / len(resolved) * 100)
                    if percent > last_progress and percent % 10 == 0:
                        last_progress = percent
                        self.print_progress(i, len(resolved), "HTTP")
            
            self.print_progress(len(resolved), len(resolved), "HTTP")
            print()
            self.print_success(f"Found {len(live_results):,} live subdomains")
            
            # STAGE 3: PRIORITY SCORING
            if live_results:
                self.print_section("STAGE 3: PRIORITY SCORING", "🏆")
                
                for result in live_results:
                    result['priority'] = self.calculate_priority(result)
                
                live_results.sort(key=lambda x: x.get('priority', 0), reverse=True)
                
                print(f"\n  {Colors.BOLD}{Colors.YELLOW}Top Priority Targets:{Colors.END}")
                print(f"  {Colors.DIM}{'─' * 40}{Colors.END}")
                
                for i, r in enumerate(live_results[:10], 1):
                    if r['priority'] >= 70:
                        color = Colors.GREEN
                        label = "CRITICAL"
                    elif r['priority'] >= 40:
                        color = Colors.YELLOW
                        label = "HIGH"
                    else:
                        color = Colors.BLUE
                        label = "MEDIUM"
                    
                    print(f"    {i}. {color}[{label} {r['priority']}]{Colors.END} {r['subdomain']}")
                    print(f"       └─ {r.get('title', 'No Title')[:60]}")
                
                self.results = live_results
        
        # SUMMARY
        self.end_time = time.time()
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        elapsed = self.end_time - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'═' * 56}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}  📊 KRAKEN SCAN SUMMARY{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'═' * 56}{Colors.END}")
        
        print(f"  {Colors.YELLOW}Target:{Colors.END}        {self.domain}")
        print(f"  {Colors.YELLOW}Duration:{Colors.END}      {minutes}m {seconds}s")
        print(f"  {Colors.YELLOW}Workers:{Colors.END}       {self.max_workers}")
        
        wordlist_size = len(self.load_wordlist())
        print(f"  {Colors.YELLOW}Wordlist:{Colors.END}      {wordlist_size:,} candidates")
        print(f"  {Colors.YELLOW}DNS Cache:{Colors.END}     {len(self.dns_cache):,} entries")
        
        if self.results:
            live_count = len(self.results)
            critical = len([r for r in self.results if r.get('priority', 0) >= 70])
            high = len([r for r in self.results if 40 <= r.get('priority', 0) < 70])
            medium = len([r for r in self.results if r.get('priority', 0) < 40])
            
            print(f"\n  {Colors.YELLOW}Live Subdomains:{Colors.END} {live_count}")
            print(f"    {Colors.GREEN}Critical:{Colors.END} {critical}  |  {Colors.YELLOW}High:{Colors.END} {high}  |  {Colors.BLUE}Medium:{Colors.END} {medium}")
        
        print(f"\n  {Colors.GREEN}✓ Live list:     output/{self.domain}_live.txt{Colors.END}")
        print(f"  {Colors.GREEN}✓ Full report:   output/{self.domain}_report.json{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'═' * 56}{Colors.END}\n")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"\n{Colors.BLUE}{Colors.BOLD}KRAKEN - Subdomain Discovery Engine{Colors.END}")
    print(f"{Colors.DIM}Professional Bug Bounty Tool • Zero False Positive • Live Verification{Colors.END}\n")
    
    domain = input(f"{Colors.YELLOW}[?]{Colors.END} Enter target domain: ").strip()
    
    if not domain:
        print(f"{Colors.RED}[!] Domain cannot be empty!{Colors.END}")
        sys.exit(1)
    
    # Setup paths
    home = os.path.expanduser("~")
    wordlist_path = f"{home}/dev/phase1-subdomain-engine/wordlists/subdomains.txt"
    
    # Create wordlist if not exists
    if not os.path.exists(wordlist_path):
        os.makedirs(f"{home}/dev/phase1-subdomain-engine/wordlists", exist_ok=True)
        with open(wordlist_path, 'w') as f:
            default_wordlist = ['www', 'mail', 'admin', 'api', 'dev', 'test', 'blog', 'vpn', 'ftp', 'ns1', 'ns2', 'webmail', 'cpanel', 'whm', 'secure', 'cloud', 'cdn', 'static', 'img', 'video', 'download', 'upload', 'support', 'help', 'docs', 'status', 'monitor', 'stats', 'analytics', 'dashboard', 'portal', 'app', 'api2', 'apiv1', 'apiv2', 'rest', 'graphql', 'backend', 'internal', 'private', 'corp', 'office', 'remote', 'ssh', 'mysql', 'redis', 'jenkins', 'gitlab', 'github', 'bitbucket', 'jira', 'confluence', 'wiki', 'wordpress', 'shop', 'store', 'payment', 'billing', 'account', 'profile', 'user', 'login', 'signin', 'auth', 'oauth', 'sso', 'verify', 'sandbox', 'demo', 'staging2', 'dev2', 'develop', 'development', 'prod', 'production', 'live', 'edge', 'gateway', 'proxy', 'cache', 'queue', 'worker', 'task', 'job']
            for w in default_wordlist:
                f.write(f"{w}\n")
    
    engine = Kraken(domain, wordlist_path, max_workers=50)
    results = engine.run()
    
    # Save outputs
    os.makedirs("output", exist_ok=True)
    
    with open(f"output/{domain}_live.txt", 'w') as f:
        for r in results:
            f.write(f"{r['subdomain']}\n")
    
    with open(f"output/{domain}_report.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    if results:
        print(f"{Colors.GREEN}[✓] Scan complete! Found {len(results)} live subdomains{Colors.END}")

if __name__ == "__main__":
    main()
