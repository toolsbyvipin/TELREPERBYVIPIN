# ==================================================
# SHΔDØW WORM-AI💀🔥 - ADVANCED TELEGRAM REPORTER v4.0
# INDIAN LEGAL FRAMEWORK | MEDIA DETECTION | PRIVATE CHANNEL SUPPORT
# ==================================================

import asyncio
import os
import sys
import json
import random
import base64
import secrets
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from urllib.parse import urlparse
from cryptography.fernet import Fernet
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ReportRequest, ImportChatInviteRequest, CheckChatInviteRequest
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import (
    InputReportReasonSpam, InputReportReasonViolence, InputReportReasonPornography,
    InputReportReasonCopyright, InputReportReasonOther, MessageMediaPhoto, 
    MessageMediaDocument, MessageMediaWebPage, PeerChannel, InputPeerChannel,
    ChatInvite, Message, Channel, User
)
from telethon.tl.functions.messages import GetHistoryRequest
import socks
from colorama import Fore, Style, init

init(autoreset=True)

# ===== CONFIGURATION =====
CONFIG_VERSION = "4.0"
ENCRYPTION_KEY_FILE = "reporter.key"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ===== INDIAN LEGAL FRAMEWORK =====
class IndianLegalFramework:
    """Indian laws applicable to Telegram content violations"""
    
    VIOLATIONS = {
        "spam": {
            "acts": [
                "IT Act 2000 - Section 66A (though struck down, related to annoying messages)",
                "IT Rules 2021 - Intermediary Guidelines Rule 3(2)(b)"
            ],
            "penalties": "Up to 3 years imprisonment or fine up to ₹5 lakhs",
            "legal_text": "Under Indian IT Rules 2021, intermediaries must remove spam content within 24 hours of report. Persistent spam violates user privacy and platform guidelines."
        },
        "violence": {
            "acts": [
                "IPC Section 153A - Promoting enmity between groups",
                "IPC Section 505 - Statements conducing to public mischief",
                "IT Act 2000 - Section 69A (blocking for national security)"
            ],
            "penalties": "Up to 5 years imprisonment with fine",
            "legal_text": "Content promoting violence violates IPC Section 153A. Under Indian law, incitement to violence is a cognizable offense. Telegram must remove such content under IT Rules 2021."
        },
        "abuse": {
            "acts": [
                "IPC Section 354A - Sexual harassment",
                "IPC Section 509 - Word, gesture or act intended to insult modesty of woman",
                "IT Act 2000 - Section 67 (punishment for publishing obscene material)"
            ],
            "penalties": "Imprisonment up to 3 years and fine",
            "legal_text": "Harassment and abusive content violates IPC 354A and IT Act 67. Platform required to remove within 24 hours under IT Rules 2021."
        },
        "porn": {
            "acts": [
                "IT Act 2000 - Section 67 (Publishing obscene material)",
                "IT Act 2000 - Section 67A (Publishing sexually explicit material)",
                "POCSO Act 2012 - Section 14 (Child pornography)"
            ],
            "penalties": "First conviction: 3-5 years imprisonment + fine. Subsequent: up to 7 years",
            "legal_text": "Pornographic content, especially involving minors, is strictly prohibited under IT Act 67A and POCSO Act. Immediate removal mandated by Indian law."
        },
        "copyright": {
            "acts": [
                "Copyright Act 1957 - Section 63 (Infringement)",
                "IT Act 2000 - Section 72 (Breach of confidentiality)"
            ],
            "penalties": "6 months to 3 years imprisonment with fine up to ₹2 lakhs",
            "legal_text": "Copyright infringement violates the Copyright Act 1957. Platforms must remove infringing content upon receiving valid complaint under IT Rules 2021."
        },
        "drugs": {
            "acts": [
                "NDPS Act 1985 - Section 27 (Illegal drug trade)",
                "IT Act 2000 - Section 67C (Preservation of information)"
            ],
            "penalties": "Rigorous imprisonment up to 20 years depending on quantity",
            "legal_text": "Promotion or sale of drugs violates NDPS Act 1985. Telegram must report such content to law enforcement under IT Rules 2021."
        },
        "fake": {
            "acts": [
                "IPC Section 419 - Punishment for cheating by impersonation",
                "IPC Section 465 - Forgery",
                "IT Act 2000 - Section 66D (Punishment for cheating by personation)"
            ],
            "penalties": "Imprisonment up to 3 years and fine",
            "legal_text": "Fake accounts and impersonation violate IPC 419 and IT Act 66D. Platforms must verify and remove such accounts."
        },
        "harassment": {
            "acts": [
                "IPC Section 354D - Stalking",
                "IPC Section 507 - Criminal intimidation by anonymous communication",
                "IT Act 2000 - Section 66E (Violation of privacy)"
            ],
            "penalties": "Imprisonment up to 3 years with fine",
            "legal_text": "Cyber stalking and harassment are punishable under IPC 354D and IT Act 66E. Immediate action required under IT Rules 2021."
        },
        "defamation": {
            "acts": [
                "IPC Section 499 - Defamation",
                "IPC Section 500 - Punishment for defamation"
            ],
            "penalties": "Simple imprisonment up to 2 years, or fine, or both",
            "legal_text": "Defamatory content violates IPC 499. Platforms must remove defamatory material upon receiving legal notice."
        },
        "child_safety": {
            "acts": [
                "POCSO Act 2012 - Section 14 (Child pornography)",
                "IT Act 2000 - Section 67B (Punishment for publishing child porn)",
                "Juvenile Justice Act 2015 - Section 75"
            ],
            "penalties": "Minimum 5 years imprisonment up to 7 years + fine up to ₹10 lakhs",
            "legal_text": "ANY content involving minors is strictly prohibited. This includes CSAM, grooming, and inappropriate interactions. Immediate reporting to cybercrime cell mandated."
        }
    }
    
    @staticmethod
    def get_legal_text(violation_type: str) -> str:
        """Get formatted legal text for violation"""
        if violation_type not in IndianLegalFramework.VIOLATIONS:
            return ""
        
        v = IndianLegalFramework.VIOLATIONS[violation_type]
        legal_text = f"""
[INDIAN LEGAL NOTICE]
Violation: {violation_type.upper()}
Applicable Laws: {', '.join(v['acts'])}
Penalties: {v['penalties']}

{v['legal_text']}

Under IT Rules 2021 (Intermediary Guidelines), Telegram is required to:
• Remove illegal content within 24 hours of reporting
• Preserve records for 180 days
• Cooperate with law enforcement agencies

Complaint Reference: IN-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}
"""
        return legal_text
    
    @staticmethod
    def get_report_comment(violation_type: str, target_info: str = "") -> str:
        """Generate comprehensive report comment with legal backing"""
        v = IndianLegalFramework.VIOLATIONS.get(violation_type, {})
        acts = v.get('acts', ['Telegram Terms of Service'])
        
        comment_templates = [
            f"URGENT: {violation_type.upper()} violation detected. Legal basis: {acts[0]}. {target_info} Requires immediate removal under IT Rules 2021.",
            f"INDIAN LEGAL COMPLAINT: This {violation_type} content violates {acts[0]}. Telegram must remove within 24 hours per Intermediary Guidelines 2021.",
            f"CYBER CRIME REPORT: {violation_type.upper()} content. Legal provisions: {', '.join(acts[:2])}. Request immediate takedown and preserve logs.",
            f"COMPLIANCE NOTICE: {violation_type.upper()} violates Indian IT Act 2000 and IT Rules 2021. {target_info} Action required within 24 hours.",
            f"LEGAL TAKEDOWN REQUEST: {violation_type} content. Applicable laws: {acts[0]}. Reference: IN-{datetime.now().strftime('%Y%m%d')}"
        ]
        
        comment = random.choice(comment_templates)
        if IndianLegalFramework.VIOLATIONS.get(violation_type, {}).get('penalties'):
            comment += f" Penalties: {IndianLegalFramework.VIOLATIONS[violation_type]['penalties']}"
        
        return comment

# ===== MEDIA DETECTION ENGINE =====
class MediaDetector:
    """Detect and classify media content types"""
    
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf']
    AUDIO_EXTENSIONS = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']
    ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z', '.tar', '.gz']
    
    SUSPICIOUS_PATTERNS = {
        "adult": [r'porn', r'adult', r'xxx', r'nude', r'nsfw', r'sex', r'18\+', r'mature'],
        "violence": [r'kill', r'murder', r'weapon', r'gun', r'violence', r'blood', r'gore', r'execute'],
        "drugs": [r'drug', r'weed', r'cocaine', r'heroin', r'mdma', r'narcotic', r'pharma'],
        "spam": [r'click here', r'earn money', r'get rich', r'bitcoin', r'crypto', r'promotion'],
        "scam": [r'lottery', r'prize', r'winner', r'bank details', r'upi', r'paytm']
    }
    
    @staticmethod
    def detect_media_type(message: Message) -> Dict[str, Any]:
        """Analyze message and return media type information"""
        result = {
            "has_media": False,
            "media_type": None,
            "file_name": None,
            "file_ext": None,
            "mime_type": None,
            "size": None,
            "caption": message.text or ""
        }
        
        if message.media:
            result["has_media"] = True
            
            if isinstance(message.media, MessageMediaPhoto):
                result["media_type"] = "photo"
                result["mime_type"] = "image/jpeg"
                
            elif isinstance(message.media, MessageMediaDocument):
                doc = message.media.document
                result["media_type"] = "document"
                result["mime_type"] = doc.mime_type
                result["size"] = doc.size
                
                # Get file name and extension
                for attr in doc.attributes:
                    if hasattr(attr, 'file_name') and attr.file_name:
                        result["file_name"] = attr.file_name
                        result["file_ext"] = os.path.splitext(attr.file_name)[1].lower()
                        break
                
                # Classify based on extension
                if result["file_ext"] in MediaDetector.IMAGE_EXTENSIONS:
                    result["media_type"] = "image"
                elif result["file_ext"] in MediaDetector.VIDEO_EXTENSIONS:
                    result["media_type"] = "video"
                elif result["file_ext"] in MediaDetector.AUDIO_EXTENSIONS:
                    result["media_type"] = "audio"
                elif result["file_ext"] in MediaDetector.DOCUMENT_EXTENSIONS:
                    result["media_type"] = "document"
                elif result["file_ext"] in MediaDetector.ARCHIVE_EXTENSIONS:
                    result["media_type"] = "archive"
                    
            elif isinstance(message.media, MessageMediaWebPage):
                result["media_type"] = "webpage"
                if message.media.webpage:
                    result["caption"] = message.media.webpage.title or result["caption"]
        
        return result
    
    @staticmethod
    def analyze_content(text: str) -> List[Tuple[str, str]]:
        """Analyze text content for violations with Indian context"""
        detected = []
        text_lower = text.lower()
        
        for violation, patterns in MediaDetector.SUSPICIOUS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected.append((violation, pattern))
                    break
        
        # Indian-specific patterns
        indian_scam_patterns = [
            (r'kbc', "KBC lottery scam - IPC 420"),
            (r'lottery', "Lottery scam - IPC 420, IT Act 66D"),
            (r'job.*payment', "Fake job scam - IPC 420"),
            (r'loan.*upi', "Loan scam - RBI guidelines violation"),
            (r'free.*recharge', "Mobile recharge scam - IT Act 66"),
            (r'girl.*number', "Matrimonial scam - IPC 420"),
            (r'call.*girl', "Prostitution promotion - IPC 372/373")
        ]
        
        for pattern, description in indian_scam_patterns:
            if re.search(pattern, text_lower):
                detected.append(("scam_indian", description))
        
        return detected
    
    @staticmethod
    def generate_report_comment(media_info: Dict, violation: str, legal_text: str) -> str:
        """Generate specific report comment based on media type and violation"""
        base = legal_text
        
        if media_info["has_media"]:
            base += f"\n\nMedia Content Detected: {media_info['media_type'].upper()}"
            if media_info.get("file_name"):
                base += f"\nFile: {media_info['file_name']}"
            base += f"\nMIME Type: {media_info['mime_type']}"
        
        if violation in IndianLegalFramework.VIOLATIONS:
            base += f"\n\nViolation Category: {violation.upper()}"
        
        return base

# ===== PRIVATE CHANNEL HANDLER =====
class PrivateChannelHandler:
    """Handle private channel/group joining and reporting"""
    
    @staticmethod
    async def join_private_channel(client: TelegramClient, identifier: str) -> Optional[Any]:
        """
        Join private channel using invite link or username
        Returns entity if successful, None otherwise
        """
        try:
            # Check if it's an invite link
            if 't.me/' in identifier or 'telegram.me/' in identifier:
                invite_hash = identifier.split('/')[-1]
                # Remove any query parameters
                invite_hash = invite_hash.split('?')[0]
                
                # Check invite validity
                try:
                    invite_info = await client(CheckChatInviteRequest(invite_hash))
                    if isinstance(invite_info, ChatInvite):
                        print(f"{Colors.CYAN}📋 Invite info: {invite_info.title} - {invite_info.participants_count} members{Colors.RESET}")
                        
                        # Join
                        result = await client(ImportChatInviteRequest(invite_hash))
                        await asyncio.sleep(1)
                        
                        # Get the joined channel
                        if result.chats:
                            return result.chats[0]
                        
                except errors.InviteHashExpiredError:
                    print(f"{Colors.RED}❌ Invite link expired{Colors.RESET}")
                    return None
                except errors.InviteHashInvalidError:
                    print(f"{Colors.RED}❌ Invalid invite link{Colors.RESET}")
                    return None
                    
            else:
                # Try as username
                try:
                    entity = await client.get_entity(identifier)
                    if hasattr(entity, 'username') and entity.username:
                        # Public channel
                        try:
                            await client(JoinChannelRequest(entity))
                            return entity
                        except errors.FloodWaitError as e:
                            print(f"{Colors.YELLOW}⚠️ Flood wait: {e.seconds}s{Colors.RESET}")
                            await asyncio.sleep(e.seconds)
                            return entity
                except errors.ChannelPrivateError:
                    print(f"{Colors.RED}❌ Private channel - need invite link{Colors.RESET}")
                    return None
                except errors.UsernameNotOccupiedError:
                    print(f"{Colors.RED}❌ Username not found{Colors.RESET}")
                    return None
                    
        except Exception as e:
            print(f"{Colors.RED}❌ Join error: {str(e)[:50]}{Colors.RESET}")
            return None
        
        return None
    
    @staticmethod
    async def get_channel_messages(client: TelegramClient, entity: Any, limit: int = 50) -> List[Message]:
        """Get messages from channel/group with proper access"""
        try:
            messages = await client(GetHistoryRequest(
                peer=entity,
                limit=limit,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))
            return messages.messages
        except errors.FloodWaitError as e:
            print(f"{Colors.YELLOW}⚠️ Flood wait: {e.seconds}s{Colors.RESET}")
            await asyncio.sleep(e.seconds)
            return []
        except errors.ChannelPrivateError:
            print(f"{Colors.RED}❌ Cannot access private channel messages{Colors.RESET}")
            return []
        except Exception as e:
            print(f"{Colors.RED}❌ Message fetch error: {str(e)[:50]}{Colors.RESET}")
            return []

# ===== MAIN REPORTER CLASS =====
class ShadowReporterV4:
    def __init__(self):
        self.base_dir = self._setup_dirs()
        self.config_file = f"{self.base_dir}/config.enc"
        self.logs_file = f"{self.base_dir}/reports_log.json"
        self.encryption_key = self._load_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        self.accounts: List[Dict] = []
        self.proxies: List[Dict] = []
        self.report_history = []
        self.legal_framework = IndianLegalFramework()
        self.media_detector = MediaDetector()
        self.private_handler = PrivateChannelHandler()
        self._load_config()
        self._load_logs()
        
    def _setup_dirs(self) -> str:
        try:
            base = '/data/data/ru.iiec.pydroid3/files/.shadow_reporter'
            os.makedirs(base, exist_ok=True)
            os.makedirs(f"{base}/sessions", exist_ok=True)
            os.makedirs(f"{base}/logs", exist_ok=True)
            os.makedirs(f"{base}/evidence", exist_ok=True)
        except:
            base = os.path.join(os.getcwd(), ".shadow_reporter")
            os.makedirs(base, exist_ok=True)
            os.makedirs(f"{base}/sessions", exist_ok=True)
            os.makedirs(f"{base}/logs", exist_ok=True)
            os.makedirs(f"{base}/evidence", exist_ok=True)
        return base
    
    def _load_or_create_key(self) -> bytes:
        key_path = os.path.join(self.base_dir, ENCRYPTION_KEY_FILE)
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(key)
            return key
    
    def _load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "rb") as f:
                    encrypted_data = f.read()
                decrypted = self.cipher.decrypt(encrypted_data)
                data = json.loads(decrypted)
                self.accounts = data.get("accounts", [])
                self.proxies = data.get("proxies", [])
            except:
                self.accounts = []
                self.proxies = []
    
    def _save_config(self):
        data = {
            "accounts": self.accounts,
            "proxies": self.proxies,
            "version": CONFIG_VERSION,
            "updated": datetime.now().isoformat()
        }
        encrypted = self.cipher.encrypt(json.dumps(data).encode())
        with open(self.config_file, "wb") as f:
            f.write(encrypted)
    
    def _load_logs(self):
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, "r") as f:
                    self.report_history = json.load(f)
            except:
                self.report_history = []
    
    def _save_log(self, entry: Dict):
        self.report_history.append(entry)
        with open(self.logs_file, "w") as f:
            json.dump(self.report_history[-500:], f, indent=2)
    
    def _random_delay(self, min_sec: float = 1.0, max_sec: float = 4.0):
        return random.uniform(min_sec, max_sec)
    
    def _get_proxy_for_account(self, account: Dict) -> Optional[Tuple]:
        if not self.proxies:
            return None
        proxy_id = account.get("proxy_id", 0)
        if proxy_id >= len(self.proxies):
            proxy_id = 0
        p = self.proxies[proxy_id]
        if p["type"].lower() == "socks5":
            return (socks.SOCKS5, p["host"], p["port"], p.get("username"), p.get("password"))
        return None
    
    async def _validate_session(self, account: Dict) -> bool:
        try:
            client = TelegramClient(
                account["session_file"],
                account["api_id"],
                account["api_hash"],
                proxy=self._get_proxy_for_account(account)
            )
            await client.connect()
            if not await client.is_user_authorized():
                return False
            me = await client.get_me()
            account["username"] = me.username or account.get("username", "unknown")
            account["first_name"] = me.first_name or account.get("first_name", "unknown")
            await client.disconnect()
            return True
        except:
            return False
    
    async def add_account(self):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[+] ADD ACCOUNT - SHADOW MODE V4{Colors.RESET}")
        nickname = input(f"{Colors.GREEN}Nickname: {Colors.RESET}") or f"acc_{len(self.accounts)+1}"
        api_id = int(input(f"{Colors.GREEN}API ID: {Colors.RESET}"))
        api_hash = input(f"{Colors.GREEN}API Hash: {Colors.RESET}")
        phone = input(f"{Colors.GREEN}Phone (+1234567890): {Colors.RESET}")
        
        use_proxy = input(f"{Colors.GREEN}Use proxy? (y/n): {Colors.RESET}").lower() == 'y'
        proxy_id = None
        if use_proxy and self.proxies:
            self._list_proxies()
            proxy_idx = int(input(f"{Colors.GREEN}Select proxy: {Colors.RESET}")) - 1
            if 0 <= proxy_idx < len(self.proxies):
                proxy_id = proxy_idx
        
        session_file = f"{self.base_dir}/sessions/{nickname}_{len(self.accounts)+1}"
        
        client = TelegramClient(session_file, api_id, api_hash, proxy=self._get_proxy_by_id(proxy_id))
        await client.start(phone)
        me = await client.get_me()
        
        account = {
            "id": len(self.accounts) + 1,
            "nickname": nickname,
            "api_id": api_id,
            "api_hash": api_hash,
            "phone": phone,
            "session_file": session_file,
            "username": me.username,
            "first_name": me.first_name,
            "user_id": me.id,
            "proxy_id": proxy_id,
            "added_date": datetime.now().isoformat()
        }
        self.accounts.append(account)
        self._save_config()
        
        print(f"{Colors.GREEN}✅ Account added: @{me.username} ({me.first_name}){Colors.RESET}")
        await client.disconnect()
    
    def _list_proxies(self):
        for i, p in enumerate(self.proxies):
            print(f"  {i+1}. {p['type']}://{p['host']}:{p['port']}")
    
    def _get_proxy_by_id(self, proxy_id: Optional[int]) -> Optional[Tuple]:
        if proxy_id is None or not self.proxies or proxy_id >= len(self.proxies):
            return None
        p = self.proxies[proxy_id]
        if p["type"].lower() == "socks5":
            return (socks.SOCKS5, p["host"], p["port"], p.get("username"), p.get("password"))
        return None
    
    async def add_proxy(self):
        print(f"\n{Colors.YELLOW}[+] ADD PROXY{Colors.RESET}")
        ptype = input(f"{Colors.GREEN}Type (socks5/http): {Colors.RESET}").lower()
        host = input(f"{Colors.GREEN}Host: {Colors.RESET}")
        port = int(input(f"{Colors.GREEN}Port: {Colors.RESET}"))
        username = input(f"{Colors.GREEN}Username (optional): {Colors.RESET}") or None
        password = input(f"{Colors.GREEN}Password (optional): {Colors.RESET}") or None
        
        self.proxies.append({
            "type": ptype,
            "host": host,
            "port": port,
            "username": username,
            "password": password
        })
        self._save_config()
        print(f"{Colors.GREEN}✅ Proxy added{Colors.RESET}")
    
    async def find_and_report_content(self):
        """Main function to find specific content and report with Indian laws"""
        if not self.accounts:
            print(f"{Colors.RED}❌ No accounts. Use 'add' command.{Colors.RESET}")
            return
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[+] CONTENT DETECTION & REPORTING MODE{Colors.RESET}")
        
        # Validate accounts
        valid_accounts = []
        for acc in self.accounts:
            if await self._validate_session(acc):
                valid_accounts.append(acc)
        
        if not valid_accounts:
            print(f"{Colors.RED}❌ No valid accounts.{Colors.RESET}")
            return
        
        # Target input
        target_input = input(f"{Colors.GREEN}Enter target (username or invite link): {Colors.RESET}").strip()
        
        # Media type to filter
        print(f"\n{Colors.CYAN}Media types to detect:{Colors.RESET}")
        media_types = ["all", "photos", "videos", "documents", "links", "text_only"]
        for i, mt in enumerate(media_types, 1):
            print(f"  {i}. {mt}")
        media_choice = input(f"{Colors.GREEN}Select media type: {Colors.RESET}") or "1"
        media_filter = media_types[int(media_choice) - 1] if media_choice.isdigit() else "all"
        
        # Violation type
        print(f"\n{Colors.CYAN}Violation types (Indian laws):{Colors.RESET}")
        violations = list(IndianLegalFramework.VIOLATIONS.keys())
        for i, v in enumerate(violations, 1):
            print(f"  {i}. {v.upper()}")
        v_choice = input(f"{Colors.GREEN}Select violation: {Colors.RESET}") or "1"
        violation = violations[int(v_choice) - 1] if v_choice.isdigit() else "spam"
        
        # Message limit
        msg_limit = int(input(f"{Colors.GREEN}Messages to scan (10-200): {Colors.RESET}") or "50")
        msg_limit = min(max(msg_limit, 10), 200)
        
        print(f"\n{Colors.YELLOW}Starting scan with account: {valid_accounts[0]['nickname']}{Colors.RESET}")
        
        # Use first valid account to scan
        client = TelegramClient(
            valid_accounts[0]["session_file"],
            valid_accounts[0]["api_id"],
            valid_accounts[0]["api_hash"],
            proxy=self._get_proxy_for_account(valid_accounts[0])
        )
        await client.start()
        
        # Join/access private channel
        entity = await self.private_handler.join_private_channel(client, target_input)
        if not entity:
            print(f"{Colors.RED}❌ Could not access target{Colors.RESET}")
            await client.disconnect()
            return
        
        # Get messages
        messages = await self.private_handler.get_channel_messages(client, entity, msg_limit)
        if not messages:
            print(f"{Colors.YELLOW}⚠️ No messages found{Colors.RESET}")
            await client.disconnect()
            return
        
        print(f"{Colors.GREEN}✅ Found {len(messages)} messages{Colors.RESET}")
        
        # Analyze messages
        reportable_messages = []
        for msg in messages:
            if not msg.text and not msg.media:
                continue
            
            media_info = self.media_detector.detect_media_type(msg)
            
            # Filter by media type
            if media_filter != "all":
                if media_filter == "text_only" and media_info["has_media"]:
                    continue
                elif media_filter == "photos" and media_info["media_type"] not in ["photo", "image"]:
                    continue
                elif media_filter == "videos" and media_info["media_type"] != "video":
                    continue
                elif media_filter == "documents" and media_info["media_type"] != "document":
                    continue
                elif media_filter == "links" and media_info["media_type"] != "webpage":
                    continue
            
            # Analyze content
            content_violations = []
            if msg.text:
                content_violations = self.media_detector.analyze_content(msg.text)
            
            reportable_messages.append({
                "message": msg,
                "msg_id": msg.id,
                "text": msg.text or "",
                "media_info": media_info,
                "detected_violations": content_violations,
                "date": msg.date
            })
        
        if not reportable_messages:
            print(f"{Colors.YELLOW}⚠️ No reportable messages found{Colors.RESET}")
            await client.disconnect()
            return
        
        print(f"\n{Colors.GREEN}📊 Found {len(reportable_messages)} reportable messages{Colors.RESET}")
        
        # Display messages for selection
        for i, rm in enumerate(reportable_messages[:10], 1):
            media_type = rm["media_info"]["media_type"] or "text"
            text_preview = rm["text"][:50] if rm["text"] else "[No text]"
            print(f"  {i}. [ID:{rm['msg_id']}] [{media_type}] {text_preview}...")
        
        selection = input(f"\n{Colors.GREEN}Select messages to report (1-{len(reportable_messages)} or 'all'): {Colors.RESET}")
        
        if selection.lower() == 'all':
            selected_messages = reportable_messages
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected_messages = [reportable_messages[i] for i in indices if 0 <= i < len(reportable_messages)]
            except:
                print(f"{Colors.RED}Invalid selection{Colors.RESET}")
                await client.disconnect()
                return
        
        print(f"\n{Colors.YELLOW}Selected {len(selected_messages)} messages for reporting{Colors.RESET}")
        
        # Generate legal report
        legal_text = self.legal_framework.get_legal_text(violation)
        print(f"\n{Colors.CYAN}Legal basis for report:{Colors.RESET}")
        print(legal_text[:500] + "..." if len(legal_text) > 500 else legal_text)
        
        confirm = input(f"\n{Colors.GREEN}Proceed with reporting? (y/n): {Colors.RESET}").lower()
        if confirm != 'y':
            await client.disconnect()
            return
        
        # Execute reports with all accounts
        results = await self._execute_batch_reports_with_messages(
            valid_accounts, entity, selected_messages, violation, legal_text
        )
        
        # Save evidence
        evidence_file = f"{self.base_dir}/evidence/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(evidence_file, 'w') as f:
            json.dump({
                "target": target_input,
                "violation": violation,
                "messages_reported": [rm["msg_id"] for rm in selected_messages],
                "results": results,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n{Colors.GREEN}✅ Evidence saved to {evidence_file}{Colors.RESET}")
        
        await client.disconnect()
    
    async def _execute_batch_reports_with_messages(self, accounts: List[Dict], entity: Any, messages: List[Dict], violation: str, legal_text: str) -> Dict:
        """Execute reports with specific messages"""
        semaphore = asyncio.Semaphore(3)
        results = {"success": 0, "failed": 0}
        
        async def report_with_account(account: Dict):
            async with semaphore:
                return await self._report_messages_with_account(account, entity, messages, violation, legal_text)
        
        tasks = [report_with_account(acc) for acc in accounts]
        account_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for res in account_results:
            if isinstance(res, dict):
                results["success"] += res.get("success", 0)
                results["failed"] += res.get("failed", 0)
        
       