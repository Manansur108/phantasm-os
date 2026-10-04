"""
Unit tests for Generative Hallucination Engine.
"""

from phantasm_os.core.generator import RetroGenerator


def test_generate_web_page_structure():
    gen = RetroGenerator()
    page = gen.generate_web_page("http://www.geocities.com/siliconvalley/tech")
    assert page.url == "http://www.geocities.com/siliconvalley/tech"
    assert "GEOCITIES.COM" in page.title
    assert page.hit_counter > 0
    assert len(page.links) > 0
    assert "<marquee" in page.html_content
    assert page.under_construction is True


def test_deterministic_generation_for_same_url():
    gen = RetroGenerator()
    url = "http://www.conspiracy-bbs.net/forum/ufo"
    page1 = gen.generate_web_page(url)
    page2 = gen.generate_web_page(url)

    assert page1.title == page2.title
    assert page1.hit_counter == page2.hit_counter
    assert page1.author == page2.author
    assert page1.midi_soundtrack == page2.midi_soundtrack


def test_arg_gateway_page_trigger():
    gen = RetroGenerator()
    url = "http://www.phantasm.net/sector7/chimera"
    page = gen.generate_web_page(url)

    assert page.has_arg_clue is True
    assert "PHANTASM CORE" in page.title
    assert "ZLLR MYVT AOL ZLJAVY ZLCLU" in page.html_content


def test_clippy_fan_page_trigger():
    gen = RetroGenerator()
    url = "http://www.geocities.com/cliptron-shrine"
    page = gen.generate_web_page(url)

    assert "CLIPTRON" in page.title.upper()
    assert "SYSOPS_1995" in page.html_content


def test_generate_email_normal_and_arg_reply():
    gen = RetroGenerator()

    # Normal email
    normal_reply = gen.generate_email_reply(
        subject="Hello from cyberspace",
        sender="surfer@aol.com",
        body="How is the dial-up connection today?"
    )
    assert "RE: Hello from cyberspace" in normal_reply.subject
    assert normal_reply.is_arg_clue is False

    # ARG trigger email
    arg_reply = gen.generate_email_reply(
        subject="Project Chimera investigation",
        sender="surfer@aol.com",
        body="I found Sector 7 logs, what is Project Chimera?"
    )
    assert arg_reply.is_arg_clue is True
    assert "sysop@phantasm.net" in arg_reply.sender
    assert "Sector 7" in arg_reply.body


def test_seed_emails():
    gen = RetroGenerator()
    emails = gen.get_seed_emails()
    assert len(emails) >= 3
    assert any(m.is_arg_clue for m in emails)
