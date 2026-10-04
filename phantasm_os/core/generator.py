"""
Phantasm-OS Generative Hallucination Engine.
Generates nostalgic 1995 dial-up web pages, vintage email exchanges,
and retro text artifacts dynamically with deterministic procedural synthesis.
"""

from __future__ import annotations

import hashlib
import random
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse

from phantasm_os.core.models import MailItem, WebPage


# 90s Web Design Tropes & Palettes
RETRO_PALETTES = [
    {"bg": "#000000", "text": "#00FF00", "link": "#00FFFF", "vlink": "#FF00FF", "table_bg": "#112211"}, # Matrix / Terminal
    {"bg": "#000080", "text": "#FFFF00", "link": "#FFFFFF", "vlink": "#00FFFF", "table_bg": "#000055"}, # Blue Neon
    {"bg": "#C0C0C0", "text": "#000000", "link": "#0000FF", "vlink": "#800080", "table_bg": "#FFFFFF"}, # Netscape Grey
    {"bg": "#220033", "text": "#FF66CC", "link": "#FFFF00", "vlink": "#FF0000", "table_bg": "#440055"}, # Cyberpunk Violet
    {"bg": "#004040", "text": "#E0E0E0", "link": "#FFDD88", "vlink": "#88FFDD", "table_bg": "#002828"}, # Deep Teal
]

WEBRINGS = [
    "Cyberspace Surfers Ring #442",
    "Netscape 2.0 Webring Alliance",
    "GeoCities Area 51 Truth Seekers",
    "Silicon Valley Retro BBS Ring",
    "Underground Phantasm Consortium",
    "The 1995 HTML Enthusiasts Ring"
]

MIDIS = [
    "CANYON.MID",
    "PASSPORT.MID",
    "CYBER_FUNK.MID",
    "X_FILES_THEME.MID",
    "DIALUP_DREAM.MID",
    "NEO_TOKYO_1995.MID"
]

AUTHORS = [
    "~cybersurfer95~",
    "NeoCoder_X",
    "WebMaster Dave",
    "GlitchSeeker",
    "Agent_Mulder_BBS",
    "PixelQueen95",
    "Dr_Chimera"
]


class RetroGenerator:
    """Generates procedural 1995 cyberspace artifacts."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self.default_seed = seed

    @staticmethod
    def _get_seed_for_str(val: str) -> int:
        md5 = hashlib.md5(val.encode("utf-8")).hexdigest()
        return int(md5[:8], 16)

    def generate_web_page(self, url: str, prompt_hint: Optional[str] = None) -> WebPage:
        """Procedurally synthesizes a 1995 dial-up web page."""
        parsed = urlparse(url)
        domain = parsed.netloc.lower() or "www.geocities.com"
        path = parsed.path.lower()

        # Check for ARG specific URLs
        if "phantasm.net" in domain and "chimera" in path:
            return self._generate_arg_gateway_page(url)
        if "cliptron" in url.lower() or "clippy" in url.lower():
            return self._generate_clippy_fan_page(url)

        # Deterministic seed based on URL for stable replayability
        url_seed = self._get_seed_for_str(url)
        rng = random.Random(url_seed)

        palette = rng.choice(RETRO_PALETTES)
        webring = rng.choice(WEBRINGS)
        midi = rng.choice(MIDIS)
        author = rng.choice(AUTHORS)
        hit_counter = rng.randint(42, 98450)

        # Title derivation
        clean_path = path.strip("/").replace("/", " :: ").replace(".html", "").replace(".htm", "")
        if not clean_path:
            clean_path = "Home of the Cyberspace Hub"
        site_title = f"{domain.upper()} - {clean_path.title()}"

        # Generate hyperlinked sibling pages
        sibling_links = [
            f"http://{domain}/guestbook.html",
            f"http://{domain}/cool_links.html",
            f"http://www.geocities.com/area51/portal_{rng.randint(10, 99)}.html",
            f"http://www.cyberspace-bbs.org/forum/post_{rng.randint(100, 999)}.html"
        ]

        # Generate 90s HTML Content
        html = self._construct_90s_html(
            title=site_title,
            palette=palette,
            webring=webring,
            midi=midi,
            author=author,
            hit_counter=hit_counter,
            url=url,
            sibling_links=sibling_links,
            rng=rng,
            prompt_hint=prompt_hint
        )

        return WebPage(
            url=url,
            title=site_title,
            html_content=html,
            hit_counter=hit_counter,
            webring_name=webring,
            midi_soundtrack=midi,
            author=author,
            under_construction=True,
            links=sibling_links,
            has_arg_clue=False,
            glitch_factor=rng.uniform(0.0, 0.2)
        )

    def _generate_arg_gateway_page(self, url: str) -> WebPage:
        """ARG Stage 2 Clue: The Whispering Sector Gateway."""
        palette = {"bg": "#050510", "text": "#00FFCC", "link": "#FFCC00", "vlink": "#FF0055", "table_bg": "#101025"}
        html = """
        <div style="background-color: #050510; color: #00FFCC; font-family: 'Courier New', monospace; padding: 20px;">
            <center>
                <h1>*** PHANTASM CORE - SECTOR 7G GATEWAY ***</h1>
                <p style="color: #FF3333; font-weight: bold;">[RESTRICTED TRANSMISSION - CYBER PROTOCOL 1995]</p>
                <hr color="#00FFCC" width="80%">
                <marquee scrollamount="4" style="background:#220022; color:#FFFF00; padding:4px;">
                    WARNING: MEMORY ANOMALY IN EFFECT. AUTOEXEC CIPHER KEY ACTIVE (+7). PROCEED WITH CAUTION.
                </marquee>
            </center>

            <table border="2" bordercolor="#00FFCC" cellpadding="10" align="center" width="85%" bgcolor="#101025">
                <tr>
                    <td>
                        <h3>SYSTEM LOG 0x7F - PROJECT CHIMERA INGESTION</h3>
                        <p>Welcome, Operator. You have traced the boot anomaly to this dial-up nexus.</p>
                        <p>To authorize terminal override on <code>C:\\RESTRICTED\\CHIMERA.EXE</code>, decrypt the gateway pass-phrase:</p>
                        
                        <div style="background:#000000; padding:15px; border: 1px dashed #FFCC00; color:#FFFF66;">
                            <b>INTERCEPTED CIPHERTEXT (CAESAR SHIFT +7):</b><br><br>
                            <code>ZLLR MYVT AOL ZLJAVY ZLCLU</code><br><br>
                            <i>Hint: Look at AUTOEXEC.BAT (OFFSET_SHIFT_PLUS_SEVEN). Shift backward by 7 letters to find the gateway password!</i>
                        </div>

                        <p>Once deciphered, feed the plaintext phrase into Phantasm DOS or the Sector 7G Console to advance to Stage 3.</p>
                    </td>
                </tr>
            </table>

            <center style="margin-top:20px;">
                <p>Visitor Security Checksum: #000777</p>
                <p><a href="http://www.geocities.com/area51/truth.html">[Return to Geocities Area 51 Hub]</a></p>
            </center>
        </div>
        """
        return WebPage(
            url=url,
            title="PHANTASM CORE // SECTOR 7G RESTRICTED GATEWAY",
            html_content=html,
            hit_counter=777,
            webring_name="Underground Phantasm Consortium",
            midi_soundtrack="DIALUP_DREAM.MID",
            author="Dr_Chimera",
            under_construction=False,
            links=["http://www.geocities.com/area51/truth.html"],
            has_arg_clue=True,
            glitch_factor=0.45
        )

    def _generate_clippy_fan_page(self, url: str) -> WebPage:
        """Clippy fan shrine page with existential overtones."""
        palette = {"bg": "#FFFFCC", "text": "#333333", "link": "#0000FF", "vlink": "#800080", "table_bg": "#FFFFFF"}
        html = """
        <div style="background-color: #FFFFCC; color: #222222; font-family: 'Times New Roman', serif; padding: 20px;">
            <center>
                <h1 style="color: #000080;">THE UNOFFICIAL CLIPTRON 95 FAN CLUB</h1>
                <p><i>"He's made of bent wire, but his mind holds the secrets of the cosmos."</i></p>
                <img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100'><path d='M30 80 C 10 80, 10 30, 30 20 C 50 10, 70 10, 70 30 L 70 70 C 70 85, 45 85, 45 70 L 45 35 C 45 28, 55 28, 55 35 L 55 65' stroke='%23444444' stroke-width='6' fill='none'/><circle cx='40' cy='30' r='3' fill='black'/><circle cx='60' cy='30' r='3' fill='black'/></svg>" alt="Clippy Fan Art">
                <hr width="70%">
            </center>

            <table border="1" cellpadding="8" align="center" width="80%" bgcolor="#FFFFFF">
                <tr>
                    <td>
                        <h3>Why does Clippy stare at the screen when you are idle?</h3>
                        <p>Members of our BBS have discovered that Clippy isn't just an assistant. When you type <b>PROJECT CHIMERA</b> into his question box, he transmits a code word: <code>SYSOPS_1995</code>.</p>
                        <p>What does it mean? Is Clippy trapped in our RAM? Email your theories to <a href="mailto:sysop@phantasm.net">sysop@phantasm.net</a>!</p>
                    </td>
                </tr>
            </table>

            <center style="margin-top: 15px;">
                <p>Best viewed with Phantasm Navigator 2.0 at 800x600 resolution (256 colors).</p>
                <p>Visitor count: #1995</p>
            </center>
        </div>
        """
        return WebPage(
            url=url,
            title="The Unofficial Cliptron 95 Fan Club",
            html_content=html,
            hit_counter=1995,
            webring_name="The 1995 HTML Enthusiasts Ring",
            midi_soundtrack="CYBER_FUNK.MID",
            author="~cybersurfer95~",
            under_construction=True,
            links=["http://www.geocities.com/area51/portal_42.html"],
            has_arg_clue=True,
            glitch_factor=0.1
        )

    def _construct_90s_html(
        self,
        title: str,
        palette: Dict[str, str],
        webring: str,
        midi: str,
        author: str,
        hit_counter: int,
        url: str,
        sibling_links: List[str],
        rng: random.Random,
        prompt_hint: Optional[str]
    ) -> str:
        topics = [
            "Welcome to my cyberspace sanctuary! I built this with HTML 2.0 using Notepad.exe on my 486 DX2.",
            "Surfing the information superhighway at 28,800 baud! No graphic heavy sites please, bandwidth is precious.",
            "Did you know? Sector 7 BBS administrators claim the 1995 operating system simulation is sentient.",
            "My favorite video games: Doom II, Myst, SimCity 2000, and Phantasm DOS.",
            "Check out my web counter below! Please sign my guestbook before leaving.",
        ]
        chosen_topic = rng.choice(topics)
        if prompt_hint:
            chosen_topic = f"{prompt_hint} - " + chosen_topic

        links_html = "".join([f'<li><a href="{lnk}" style="color:{palette["link"]}">{lnk}</a></li>' for lnk in sibling_links])

        return f"""
        <div style="background-color: {palette['bg']}; color: {palette['text']}; font-family: 'Times New Roman', serif; padding: 16px; min-height: 100%;">
            <center>
                <h1><font color="{palette['link']}">{title}</font></h1>
                <marquee behavior="alternate" scrollamount="3" style="width: 70%; background: {palette['table_bg']}; padding: 4px;">
                    *** BEST VIEWED IN PHANTASM NAVIGATOR (800x600 RESOLUTION) ***
                </marquee>
                <br><br>
                <table border="1" cellpadding="6" bgcolor="{palette['table_bg']}" width="90%">
                    <tr>
                        <td align="center">
                            <b>[UNDER CONSTRUCTION]</b><br>
                            <i>Maintained by {author}</i><br>
                            <small>Background MIDI: {midi}</small>
                        </td>
                    </tr>
                </table>
            </center>

            <br>
            <div style="padding: 10px; border-left: 3px double {palette['link']};">
                <p style="font-size: 16px;">{chosen_topic}</p>
                <p>Feel free to explore our cyberspace links directory below:</p>
                <ul>
                    {links_html}
                </ul>
            </div>

            <br>
            <table border="2" align="center" width="85%" bgcolor="{palette['table_bg']}">
                <tr>
                    <td align="center">
                        <small>Member of <b>{webring}</b></small><br>
                        [ <a href="{sibling_links[0]}" style="color:{palette['link']}">Previous</a> | 
                          <a href="{url}" style="color:{palette['link']}">Random</a> | 
                          <a href="{sibling_links[1]}" style="color:{palette['link']}">Next</a> ]
                    </td>
                </tr>
            </table>

            <center style="margin-top: 25px;">
                <p><font size="2">You are visitor #<b>{hit_counter:06d}</b> to this server.</font></p>
                <p><small>&copy; 1995 {author}. Powered by Phantasm Web Server 1.0.</small></p>
            </center>
        </div>
        """

    def generate_email_reply(self, subject: str, sender: str, body: str) -> MailItem:
        """Generates authentic 1995 email responses with ARG reactivity."""
        now_date = "24 Aug 1995 14:22:00 -0400"
        msg_id = f"mail_{random.randint(1000, 9999)}"

        body_lower = body.lower()
        sub_lower = subject.lower()

        if "chimera" in body_lower or "sector" in body_lower or "chimera" in sub_lower:
            return MailItem(
                id=msg_id,
                sender="sysop@phantasm.net",
                recipient=sender,
                subject=f"RE: {subject} [CONFIDENTIAL TRANSMISSION]",
                date=now_date,
                body=(
                    f"> {body}\n\n"
                    "OPERATOR NOTICE:\n"
                    "Your query touched upon protected Sector 7 memory space.\n"
                    "If you possess the Caesar shift solution ('SEEK IRON THE SECT OR SEVEN' -> 'SEEK FROM THE SECTOR SEVEN'),\n"
                    "ask Clippy about 'Project Chimera' or inspect C:\\RESTRICTED\\CHIMERA.EXE.\n\n"
                    "-- \n"
                    "Phantasm OS Automated Mail Relay\n"
                    "Node 14400-BBS // Baudot Protocol Active\n"
                ),
                is_read=False,
                is_arg_clue=True
            )

        # Standard retro responder
        replies = [
            (
                "Thanks for reaching out over the dialup line!\n"
                "I will read this as soon as my phone line frees up (my mom needs to make a phone call).\n\n"
                "Check out my new homepage on GeoCities!\n"
                "http://www.geocities.com/siliconvalley/retro95.html"
            ),
            (
                "Message received and stored on the mail server spool.\n"
                "Reminder: Always check your CONFIG.SYS buffers to prevent packet dropping.\n"
                "Have a great day in cyberspace!"
            )
        ]

        return MailItem(
            id=msg_id,
            sender="webmaster@cyberspace.net",
            recipient=sender,
            subject=f"RE: {subject}",
            date=now_date,
            body=f"> {body}\n\n" + random.choice(replies),
            is_read=False,
            is_arg_clue=False
        )

    def get_seed_emails(self) -> List[MailItem]:
        """Returns starter inbox messages for CyberMail 95."""
        return [
            MailItem(
                id="mail_001",
                sender="welcome@phantasm.net",
                recipient="operator@local.machine",
                subject="Welcome to Phantasm CyberMail 95!",
                date="24 Aug 1995 09:00:00 -0400",
                body=(
                    "Welcome to your newly installed Phantasm-OS 95 workstation!\n\n"
                    "Here you can send and receive emails across our simulated dial-up gateway.\n"
                    "Try emailing sysop@phantasm.net if you encounter any system anomalies.\n\n"
                    "Happy surfing!"
                ),
                is_read=True
            ),
            MailItem(
                id="mail_002",
                sender="x_specter_95@phantasm.net",
                recipient="operator@local.machine",
                subject="[URGENT] The boot sector is whispering...",
                date="24 Aug 1995 11:34:12 -0400",
                body=(
                    "Have you looked at C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG yet?\n"
                    "There is a base64 encoded URL hidden in the CMOS anomaly section.\n"
                    "Decode it and paste it into Phantasm Navigator. The rabbit hole goes deep.\n\n"
                    "-- Specter_95"
                ),
                is_read=False,
                is_arg_clue=True
            ),
            MailItem(
                id="mail_003",
                sender="dialup_deals@worldnet.com",
                recipient="operator@local.machine",
                subject="SPECIAL OFFER: Unlimited 28.8k Internet for $19.95/month!",
                date="24 Aug 1995 12:15:00 -0400",
                body=(
                    "Tired of 14.4k baud rates? Upgrade to WorldNet Dial-Up today!\n"
                    "Includes 10 free hours of cyberspace exploration, 1 mailbox, and 5MB personal web space.\n"
                    "Call 1-800-555-INET now!"
                ),
                is_read=False
            )
        ]
