import pytest
from pathlib import Path
from formatter import generate_markdown, generate_html, generate_pdf


@pytest.fixture
def sample_briefing():
    return {
        "date": "2025-06-18",
        "intro": "This week's sustainable finance update...",
        "articles": [
            {
                "title": "Green bonds rise",
                "summary": "• Investors are piling into ESG assets.",
                "url": "https://example.com",
                "date": "2025-06-17",
                "source": "ESG Newswire"
            }
        ],
        "topic_counts": {"Market Trends": 1},
        "company_mentions": {"BlackRock": 1}
    }


def test_generate_markdown_file(tmp_path, sample_briefing):
    md_path = tmp_path / "briefing.md"
    generate_markdown(sample_briefing, str(md_path))
    assert md_path.exists()
    content = md_path.read_text(encoding="utf-8")
    assert "Green bonds rise" in content


def test_generate_html_structure(sample_briefing):
    html = generate_html(sample_briefing)
    assert html.startswith("<html>")
    assert "Green bonds rise" in html
    assert "SAFL End of Week Briefing" in html


def test_generate_html_with_logo_path(tmp_path, sample_briefing):
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-image-data")  # Dummy logo file
    html = generate_html(sample_briefing, logo_path=str(logo_path))
    assert f'src="{str(logo_path)}"' in html or "data:image" in html


def test_generate_pdf_output(tmp_path, sample_briefing):
    pdf_path = tmp_path / "briefing.pdf"
    generate_pdf(sample_briefing, output_path=str(pdf_path))
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
