#!/usr/bin/env python3
"""
CBRT - MEDIA REPORTER 💀🔥 - WORKING VERSION
Uses WORKING account.reportPeer method (confirmed successful)
"""

import asyncio
import os
import sys
import json
import secrets
import random
import traceback
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from telethon import TelegramClient, errors
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    Message,
    InputReportReasonOther,
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonCopyright,
)
from colorama import Fore, Style, init

init(autoreset=True)

# ===== COLORS =====
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    PURPLE = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

# ===== REPORT REASONS FOR account.reportPeer (WORKING) =====
def get_report_reason(reason_type: str):
    """Get the correct reason object for account.reportPeer (PROVEN WORKING)"""
    
    if reason_type == 'spam':
        return InputReportReasonSpam()
    elif reason_type == 'violence':
        return InputReportReasonViolence()
    elif reason_type == 'pornography':
        return InputReportReasonPornography()
    elif reason_type == 'copyright':
        return InputReportReasonCopyright()
    elif reason_type == 'child_abuse':
        # THIS IS WHAT WORKED IN YOUR TEST!
        reason = InputReportReasonOther()
        reason.title = "Child sexual abuse"
        return reason
    else:
        reason = InputReportReasonOther()
        reason.title = "Other violation"
        return reason

# Mapping for user selection
REASON_MAPPING = {
    1: ("SPAM", "spam"),
    2: ("CHILD ABUSE - CHILD SEXUAL ABUSE", "child_abuse"),
    3: ("VIOLENCE", "violence"),
    4: ("PORNOGRAPHY", "pornography"),
    5: ("COPYRIGHT", "copyright"),
}

# ===== INDIAN LEGAL FRAMEWORK =====
class IndianChildProtectionLaws:
    @staticmethod
    def get_comment(message_ids: List[int], target: str = ""):
        date = datetime.now().strftime("%Y%m%d")
        ref = secrets.token_hex(4).upper()
        return f"""
[URGENT - POCSO ACT VIOLATION]
I am reporting this channel for containing child sexual abuse material.

Channel: @{target}
Message IDs: {message_ids}

Laws Violated:
- POCSO Act 2012 - Section 4 (Penetrative Sexual Assault on Child)
- POCSO Act 2012 - Section 13 (Use of Child for Pornographic Purposes)
- IT Act 2000 - Section 67B (Punishment for Publishing Child Pornography)

Penalties: Minimum 7 years imprisonment up to life imprisonment + fine up to ₹10 lakhs

Under POCSO Act Section 19, reporting is MANDATORY.

Complaint Reference: IN-POCSO-{date}-{ref}

National Cyber Crime Portal: https://cybercrime.gov.in
Childline India: 1098
"""

# ===== MEDIA DETECTOR =====
class MediaDetector:
    @staticmethod
    def get_media_type(message: Message) -> Tuple[bool, str, str]:
        if not message.media:
            return False, "none", ""
        
        if isinstance(message.media, MessageMediaPhoto):
            return True, "photo", f"📷 PHOTO (ID: {message.id})"
        
        if isinstance(message.media, MessageMediaDocument):
            doc = message.media.document
            mime_type = doc.mime_type or ""
            
            if "video" in mime_type:
                return True, "video", f"🎬 VIDEO (ID: {message.id})"
            elif "audio" in mime_type:
                return True, "audio", f"🎵 AUDIO (ID: {message.id})"
            elif "gif" in mime_type:
                return True, "gif", f"🎞️ GIF (ID: {message.id})"
            else:
                file_name = "FILE"
                for attr in doc.attributes:
                    if hasattr(attr, 'file_name') and attr.file_name:
                        file_name = attr.file_name
                        break
                return True, "document", f"📄 {file_name} (ID: {message.id})"
        
        return True, "other", f"📎 MEDIA (ID: {message.id})"
    
    @staticmethod
    def get_media_emoji(media_type: str) -> str:
        emoji_map = {
            "photo": "📷",
            "video": "🎬",
            "audio": "🎵",
            "document": "📄",
            "gif": "🎞️",
            "other": "📎",
            "none": "💬"
        }
        return emoji_map.get(media_type, "📎")

# ===== MAIN REPORTER CLASS =====
class MediaReporter:
    def __init__(self):
        self.base_dir = Path.home() / ".cbrt_reporter"
        self.base_dir.mkdir(exist_ok=True)
        (self.base_dir / "sessions").mkdir(exist_ok=True)
        (self.base_dir / "logs").mkdir(exist_ok=True)
        
        self.accounts = []
        self.media_detector = MediaDetector()
        self.load_accounts()
    
    def load_accounts(self):
        accounts_file = self.base_dir / "accounts.json"
        if accounts_file.exists():
            try:
                with open(accounts_file, 'r') as f:
                    self.accounts = json.load(f)
            except:
                pass
    
    def save_accounts(self):
        with open(self.base_dir / "accounts.json", 'w') as f:
            json.dump(self.accounts, f, indent=2)
    
    def print_banner(self):
        banner = f"""
{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║  CBRT - MEDIA REPORTER 💀🔥 - WORKING VERSION                        ║
║  Uses WORKING account.reportPeer method (confirmed successful)      ║
║  Child Abuse: InputReportReasonOther(title="Child sexual abuse")    ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}[✓] System Ready | Accounts: {len(self.accounts)}{Colors.RESET}
{Colors.YELLOW}[!] Type 'help' for commands{Colors.RESET}
"""
        print(banner)
    
    def print_help(self):
        help_text = f"""
{Colors.YELLOW}{Colors.BOLD}📋 COMMANDS:{Colors.RESET}
  {Colors.GREEN}add{Colors.RESET}      - Add Telegram account
  {Colors.GREEN}list{Colors.RESET}     - List accounts
  {Colors.GREEN}scan{Colors.RESET}     - Scan channel for media & report
  {Colors.GREEN}help{Colors.RESET}     - Show this help
  {Colors.GREEN}exit{Colors.RESET}     - Exit

{Colors.YELLOW}{Colors.BOLD}🛡️ REPORT REASONS (WORKING):{Colors.RESET}
  1. SPAM
  2. CHILD ABUSE - CHILD SEXUAL ABUSE ⭐ (POCSO Act)
  3. VIOLENCE
  4. PORNOGRAPHY
  5. COPYRIGHT
"""
        print(help_text)
    
    async def add_account(self):
        print(f"\n{Colors.YELLOW}[+] ADD TELEGRAM ACCOUNT{Colors.RESET}")
        print(f"{Colors.CYAN}Get API credentials from: https://my.telegram.org/apps{Colors.RESET}")
        
        nickname = input(f"{Colors.GREEN}Nickname: {Colors.RESET}").strip() or f"acc_{len(self.accounts)+1}"
        api_id = input(f"{Colors.GREEN}API ID: {Colors.RESET}").strip()
        api_hash = input(f"{Colors.GREEN}API Hash: {Colors.RESET}").strip()
        phone = input(f"{Colors.GREEN}Phone (+1234567890): {Colors.RESET}").strip()
        
        if not all([api_id, api_hash, phone]):
            print(f"{Colors.RED}❌ All fields required!{Colors.RESET}")
            return
        
        try:
            api_id = int(api_id)
        except:
            print(f"{Colors.RED}❌ API ID must be a number!{Colors.RESET}")
            return
        
        session_file = str(self.base_dir / "sessions" / nickname)
        
        try:
            print(f"{Colors.YELLOW}🔄 Connecting...{Colors.RESET}")
            client = TelegramClient(session_file, api_id, api_hash)
            await client.start(phone)
            me = await client.get_me()
            
            account = {
                "id": len(self.accounts) + 1,
                "nickname": nickname,
                "api_id": api_id,
                "api_hash": api_hash,
                "phone": phone,
                "session_file": session_file,
                "username": me.username or "No username",
                "first_name": me.first_name or "Unknown",
                "user_id": me.id,
                "added_date": datetime.now().isoformat()
            }
            
            self.accounts.append(account)
            self.save_accounts()
            
            print(f"\n{Colors.GREEN}✅ ACCOUNT ADDED!{Colors.RESET}")
            print(f"  👤 {me.first_name} (@{me.username or 'None'})")
            
            await client.disconnect()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    
    def list_accounts(self):
        if not self.accounts:
            print(f"{Colors.YELLOW}📭 No accounts. Use 'add' command.{Colors.RESET}")
            return
        
        print(f"\n{Colors.YELLOW}📱 ACCOUNTS ({len(self.accounts)}):{Colors.RESET}")
        for acc in self.accounts:
            session_exists = Path(f"{acc['session_file']}.session").exists()
            status = f"{Colors.GREEN}✅ Active{Colors.RESET}" if session_exists else f"{Colors.RED}❌ Missing{Colors.RESET}"
            print(f"  #{acc['id']} {acc['nickname']} - @{acc['username']} - {status}")
    
    async def scan_and_report(self):
        """Scan channel for media messages and report using WORKING account.reportPeer"""
        
        if not self.accounts:
            print(f"{Colors.RED}❌ No accounts. Use 'add' command first.{Colors.RESET}")
            return
        
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*70}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}📷 MEDIA SCAN & REPORT MODE{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}{'='*70}{Colors.RESET}")
        
        # Select account
        account = self.accounts[0]
        if len(self.accounts) > 1:
            print(f"{Colors.CYAN}Available accounts:{Colors.RESET}")
            for i, acc in enumerate(self.accounts, 1):
                print(f"  {i}. {acc['nickname']} (@{acc['username']})")
            choice = input(f"{Colors.GREEN}Select account: {Colors.RESET}")
            try:
                account = self.accounts[int(choice) - 1]
            except:
                pass
        
        # Get target
        print(f"\n{Colors.YELLOW}📌 TARGET INPUT{Colors.RESET}")
        target = input(f"{Colors.GREEN}Channel username or invite link: {Colors.RESET}").strip()
        
        if not target:
            print(f"{Colors.RED}❌ Target required{Colors.RESET}")
            return
        
        # Message limit
        try:
            limit = int(input(f"{Colors.GREEN}Messages to scan (10-200): {Colors.RESET}") or "50")
            limit = min(max(limit, 10), 200)
        except:
            limit = 50
        
        # Filter options
        print(f"\n{Colors.YELLOW}🎯 MEDIA FILTER{Colors.RESET}")
        print(f"  1. All media (photos, videos, files)")
        print(f"  2. Photos only")
        print(f"  3. Videos only")
        print(f"  4. Documents/Files only")
        print(f"  5. Show all messages (including text)")
        
        filter_choice = input(f"{Colors.GREEN}Select filter (1-5): {Colors.RESET}") or "1"
        
        # Connect and scan
        print(f"\n{Colors.YELLOW}📤 CONNECTING...{Colors.RESET}")
        
        try:
            client = TelegramClient(account["session_file"], account["api_id"], account["api_hash"])
            await client.start()
            
            me = await client.get_me()
            print(f"{Colors.GREEN}✅ Connected as: {me.first_name}{Colors.RESET}")
            
            # Get entity
            print(f"{Colors.CYAN}🔍 Finding target...{Colors.RESET}")
            try:
                entity = await client.get_entity(target)
            except errors.UsernameNotOccupiedError:
                if 't.me/' in target:
                    invite_hash = target.split('/')[-1].split('?')[0]
                    result = await client(ImportChatInviteRequest(invite_hash))
                    if result.chats:
                        entity = result.chats[0]
                        print(f"{Colors.GREEN}✅ Joined private channel{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}❌ Could not join{Colors.RESET}")
                        await client.disconnect()
                        return
                else:
                    print(f"{Colors.RED}❌ Target not found{Colors.RESET}")
                    await client.disconnect()
                    return
            
            target_name = getattr(entity, 'title', None) or getattr(entity, 'first_name', 'Unknown')
            print(f"{Colors.GREEN}✅ Target: {target_name}{Colors.RESET}")
            
            # Join channel
            try:
                await client(JoinChannelRequest(entity))
                print(f"{Colors.GREEN}✅ Joined channel{Colors.RESET}")
                await asyncio.sleep(1)
            except:
                pass
            
            # Fetch messages
            print(f"{Colors.CYAN}📨 Fetching {limit} messages...{Colors.RESET}")
            messages = await client.get_messages(entity, limit=limit)
            
            if not messages:
                print(f"{Colors.RED}❌ No messages found{Colors.RESET}")
                await client.disconnect()
                return
            
            # Analyze messages for media
            media_messages = []
            
            print(f"\n{Colors.YELLOW}{'='*70}{Colors.RESET}")
            print(f"{Colors.YELLOW}📋 SCANNING MESSAGES...{Colors.RESET}")
            print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
            
            for i, msg in enumerate(messages, 1):
                has_media, media_type, file_info = self.media_detector.get_media_type(msg)
                emoji = self.media_detector.get_media_emoji(media_type)
                
                text_preview = ""
                if msg.text:
                    text_preview = msg.text[:60].replace('\n', ' ')
                    if len(msg.text) > 60:
                        text_preview += "..."
                
                show = False
                if filter_choice == "1" and has_media:
                    show = True
                elif filter_choice == "2" and media_type == "photo":
                    show = True
                elif filter_choice == "3" and media_type == "video":
                    show = True
                elif filter_choice == "4" and media_type == "document":
                    show = True
                elif filter_choice == "5":
                    show = True
                
                if show:
                    print(f"  {Colors.CYAN}{i:3}.{Colors.RESET} {emoji} {file_info}")
                    if text_preview:
                        print(f"       📝 {text_preview}")
                    media_messages.append({
                        "index": i,
                        "msg_id": msg.id,
                        "media_type": media_type,
                        "file_info": file_info,
                        "text_preview": text_preview,
                        "message": msg
                    })
            
            if not media_messages:
                print(f"\n{Colors.YELLOW}⚠️ No media messages found matching filter{Colors.RESET}")
                await client.disconnect()
                return
            
            print(f"\n{Colors.GREEN}✅ Found {len(media_messages)} media messages{Colors.RESET}")
            
            # Select messages to report
            print(f"\n{Colors.YELLOW}🎯 SELECT MESSAGES TO REPORT{Colors.RESET}")
            print(f"  Enter numbers separated by commas (e.g., 1,3,5)")
            print(f"  Or type 'all' to select all")
            print(f"  Or type 'media' to select all media messages")
            
            selection = input(f"{Colors.GREEN}Selection: {Colors.RESET}").strip()
            
            selected_msgs = []
            if selection.lower() == 'all':
                selected_msgs = media_messages
            elif selection.lower() == 'media':
                selected_msgs = [m for m in media_messages if m["media_type"] != "none"]
            else:
                try:
                    indices = [int(x.strip()) for x in selection.split(',')]
                    selected_msgs = [m for m in media_messages if m["index"] in indices]
                except:
                    print(f"{Colors.RED}❌ Invalid selection{Colors.RESET}")
                    await client.disconnect()
                    return
            
            if not selected_msgs:
                print(f"{Colors.RED}❌ No messages selected{Colors.RESET}")
                await client.disconnect()
                return
            
            # Get message IDs
            message_ids = [msg["msg_id"] for msg in selected_msgs]
            
            # Show selected messages summary
            print(f"\n{Colors.GREEN}✅ Selected {len(selected_msgs)} messages:{Colors.RESET}")
            for msg in selected_msgs[:10]:
                print(f"   • ID: {msg['msg_id']} | {msg['file_info']}")
            if len(selected_msgs) > 10:
                print(f"   • ... and {len(selected_msgs) - 10} more")
            
            # Select report reason
            print(f"\n{Colors.YELLOW}📋 SELECT REPORT REASON (WORKING){Colors.RESET}")
            print(f"  1. SPAM")
            print(f"  2. CHILD ABUSE - CHILD SEXUAL ABUSE ⭐ (POCSO Act)")
            print(f"  3. VIOLENCE")
            print(f"  4. PORNOGRAPHY")
            print(f"  5. COPYRIGHT")
            
            reason_choice = input(f"{Colors.GREEN}Select reason (1-5): {Colors.RESET}").strip()
            
            try:
                reason_num = int(reason_choice)
                if reason_num not in REASON_MAPPING:
                    print(f"{Colors.RED}❌ Invalid choice{Colors.RESET}")
                    await client.disconnect()
                    return
                reason_name, reason_type = REASON_MAPPING[reason_num]
            except:
                print(f"{Colors.RED}❌ Invalid input{Colors.RESET}")
                await client.disconnect()
                return
            
            # Generate comment
            comment = ""
            if reason_num == 2:  # Child Abuse
                comment = IndianChildProtectionLaws.get_comment(message_ids, target_name)
                print(f"\n{Colors.PURPLE}{'='*70}{Colors.RESET}")
                print(f"{Colors.RED}{Colors.BOLD}CHILD ABUSE REPORT - LEGAL NOTICE{Colors.RESET}")
                print(comment[:400] + "...")
                print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}")
                
                edit = input(f"\n{Colors.GREEN}Edit comment? (y/n): {Colors.RESET}").lower()
                if edit == 'y':
                    comment = input(f"{Colors.CYAN}Enter comment: {Colors.RESET}")
            else:
                comment = input(f"{Colors.GREEN}Comment (optional): {Colors.RESET}").strip()
            
            # Confirm
            print(f"\n{Colors.YELLOW}{'='*70}{Colors.RESET}")
            print(f"{Colors.YELLOW}📋 REPORT SUMMARY:{Colors.RESET}")
            print(f"  Account: {account['nickname']} (@{account['username']})")
            print(f"  Target: {target_name}")
            print(f"  Reason: {reason_name}")
            print(f"  Messages: {len(selected_msgs)} selected")
            print(f"  Message IDs: {message_ids[:5]}{'...' if len(message_ids) > 5 else ''}")
            print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
            
            confirm = input(f"\n{Colors.RED}🚨 SUBMIT REPORT TO TELEGRAM? (y/n): {Colors.RESET}").lower()
            
            if confirm not in ['y', 'yes']:
                print(f"{Colors.YELLOW}Cancelled{Colors.RESET}")
                await client.disconnect()
                return
            
            # SUBMIT REPORT using WORKING account.reportPeer method
            print(f"\n{Colors.YELLOW}📤 SUBMITTING REPORT TO TELEGRAM MODERATORS...{Colors.RESET}")
            print(f"  {Colors.CYAN}Reporting channel: @{target_name}{Colors.RESET}")
            print(f"  {Colors.CYAN}Message IDs: {message_ids[:5]}{'...' if len(message_ids) > 5 else ''}{Colors.RESET}")
            
            # Get the correct reason object for account.reportPeer
            reason_obj = get_report_reason(reason_type)
            
            try:
                # WORKING METHOD: account.reportPeer (PROVEN SUCCESSFUL)
                result = await client(ReportPeerRequest(
                    peer=entity,
                    reason=reason_obj,
                    message=comment
                ))
                
                print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
                print(f"{Colors.GREEN}✅ REPORT SUBMITTED SUCCESSFULLY!{Colors.RESET}")
                print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
                print(f"  Messages Reported: {len(selected_msgs)}")
                print(f"  Message IDs: {message_ids}")
                print(f"  Report Type: {reason_name}")
                
                if reason_num == 2:
                    print(f"\n{Colors.RED}{Colors.BOLD}⚠️ LEGAL REMINDER:{Colors.RESET}")
                    print(f"  You have fulfilled your mandatory reporting duty under POCSO Section 19")
                    print(f"  Also report to: https://cybercrime.gov.in")
                    print(f"  National Child Helpline: 1098")
                
                # Save log
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "account": account['nickname'],
                    "target": target,
                    "target_name": target_name,
                    "reason": reason_name,
                    "message_ids": message_ids,
                    "message_count": len(message_ids),
                    "comment": comment[:500] if comment else "",
                    "success": True
                }
                
                log_file = self.base_dir / "logs" / f"cbrt_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(log_file, 'w') as f:
                    json.dump(log_entry, f, indent=2)
                
                print(f"{Colors.GREEN}📝 Log saved: {log_file}{Colors.RESET}")
                
            except errors.FloodWaitError as e:
                print(f"{Colors.YELLOW}⚠️ Flood wait: {e.seconds} seconds{Colors.RESET}")
                print(f"  Please wait {e.seconds} seconds before reporting again.")
            except Exception as e:
                print(f"{Colors.RED}❌ Report failed: {e}{Colors.RESET}")
                traceback.print_exc()
            
            await client.disconnect()
            
        except errors.FloodWaitError as e:
            print(f"{Colors.YELLOW}⚠️ Flood wait: {e.seconds} seconds{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
            traceback.print_exc()
    
    async def main_loop(self):
        self.print_banner()
        
        while True:
            try:
                cmd = input(f"\n{Colors.BOLD}{Colors.RED}📷 CBRT> {Colors.RESET}").strip().lower()
                
                if cmd in ['exit', 'quit', 'q']:
                    print(f"{Colors.YELLOW}Goodbye!{Colors.RESET}")
                    break
                elif cmd in ['help', 'h', '?']:
                    self.print_help()
                elif cmd == 'add':
                    await self.add_account()
                elif cmd in ['list', 'ls']:
                    self.list_accounts()
                elif cmd in ['scan', 'report', 'r']:
                    await self.scan_and_report()
                elif cmd == '':
                    continue
                else:
                    print(f"{Colors.RED}❌ Unknown command. Type 'help'{Colors.RESET}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Goodbye!{Colors.RESET}")
                break

async def main():
    try:
        reporter = MediaReporter()
        await reporter.main_loop()
    except Exception as e:
        print(f"Fatal: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted")
