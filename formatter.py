import os
from typing import Dict, Any, Optional
import markdown2
import markdown
from playwright.sync_api import sync_playwright
import tempfile
from datetime import datetime


def generate_markdown(briefing: Dict, output_path: str) -> None:
    """Converts a structured briefing dict to a Markdown (.md) file."""
    lines = []
    lines.append(f"# COMPANY End of Week Briefing – {str(briefing.get('date', ''))}")
    lines.append("")
    lines.append(f"_{str(briefing.get('intro', ''))}_")
    lines.append("\n---\n")

    # Fund Performance Section
    if briefing.get("fund_performance"):
        fund_data = briefing["fund_performance"]
        lines.append("## Listed Fund Performance Summary")
        if fund_data.get("last_updated"):
            lines.append(f"_(Fund data last updated: {fund_data['last_updated']})_")
        lines.append("")

        if fund_data.get("best_performers"):
            lines.append("### Smallest Discounts")
            lines.append("| Fund | Price | NAV | Discount |")
            lines.append("|------|-------|-----|----------|")
            for fund in fund_data["best_performers"][:5]:
                lines.append(f"| {fund['Fund Name']} | £{fund['Close Price']:.2f} | £{fund['NAV']:.2f} | {fund['Discount (%)']:.1f}% |")
            lines.append("")

        if fund_data.get("worst_performers"):
            lines.append("### Largest Discounts")
            lines.append("| Fund | Price | NAV | Discount |")
            lines.append("|------|-------|-----|----------|")
            for fund in fund_data["worst_performers"][:5]:
                lines.append(f"| {fund['Fund Name']} | £{fund['Close Price']:.2f} | £{fund['NAV']:.2f} | {fund['Discount (%)']:.1f}% |")
            lines.append("")
        lines.append("\n---\n")

    lines.append("## Article Highlights\n")
    for i, article in enumerate(briefing["articles"], 1):
        lines.append(f"### {i}. {str(article.get('title', ''))}")
        lines.append(f"**Source:** {str(article.get('source', ''))} | **Date:** {str(article.get('date', ''))}")
        lines.append(f"[Read full article]({str(article.get('url', ''))})\n")

        lines.append(f"**Sentiment:** {str(article.get('sentiment', '')).capitalize()}")
        lines.append("")
        lines.append(str(article.get("summary", "")))
        lines.append("\n---\n")

    # Write Markdown to file
    with open(output_path, "w") as f:
        f.write("\n".join(lines))


def generate_pdf(briefing: Dict, output_path: str, logo_path) -> None:
    """
    Renders briefing as a PDF using a headless Chromium browser via Playwright.
    Args:
        briefing (Dict): The structured briefing data.
        output_path (str): Destination path for the generated PDF.
        logo_path (str): Optional path to a local logo image used in the HTML.
    """
    html_content = generate_html(briefing, logo_path or "")
    with tempfile.TemporaryDirectory() as temp_dir:
        html_file_path = os.path.join(temp_dir, "briefing.html")

        # Replace logo path with absolute path if provided
        if logo_path:
            html_content = html_content.replace(str(logo_path), f"file://{os.path.abspath(logo_path)}")

        # Save HTML to temp file
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_file_path}", wait_until="load")
            page.pdf(path=output_path, format="A4", print_background=True)
            browser.close()


def generate_fund_performance_section(fund_data_path: str) -> Optional[Dict[str, Any]]:
    """Generate HTML/Markdown for fund performance data"""
    try:
        import pandas as pd
        df = pd.read_csv(fund_data_path)
        
        # Sort by discount % (best to worst performing)
        df_sorted = df.sort_values('Discount (%)', ascending=False)
        
        # Categorize funds by discount levels
        best_performers = df_sorted[df_sorted['Discount (%)'] > -30]  # Less than 15% discount
        worst_performers = df_sorted[df_sorted['Discount (%)'] < -30]  # More than 30% discount
        
        # Get last modified time of the data file
        last_modified_timestamp = os.path.getmtime(fund_data_path)
        last_modified_dt = datetime.fromtimestamp(last_modified_timestamp)
        last_modified_str = last_modified_dt.strftime('%Y-%m-%d %H:%M:%S')

        return {
            'best_performers': best_performers.to_dict('records'), # type: ignore
            'worst_performers': worst_performers.to_dict('records'), # type: ignore
            'last_updated': last_modified_str,
        }
    except Exception as e:
        print(f"Error processing fund data: {e}")
        return None





def generate_html(briefing: Dict, logo_path) -> str:
    """Converts a structured briefing dict to a modern, professional HTML string for PDF output."""
    logo_path = logo_path or ""
    style = '''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            background: #ffffff;
            color: #1f2937;
            line-height: 1.6;
            font-size: 14px;
        }
        
        .document-container {
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            min-height: 297mm;
        }
        
        .header {
            background: linear-gradient(135deg, #065f46 0%, #0891b2 50%, #1e40af 100%);
            color: white;
            padding: 40px 32px 32px 32px;
            position: relative;
        }

        .watermark {
            position: fixed;
            top: 35%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 120px;
            color: #065f46;
            opacity: 0.08;
            font-weight: 900;
            pointer-events: none;
            z-index: 9999;
            white-space: nowrap;
            user-select: none;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #10b981, #06b6d4, #3b82f6);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }
        
        .logo-section img {
            max-height: 60px;
            width: auto;
        }
        
        .document-info {
            text-align: right;
            font-size: 12px;
            opacity: 0.9;
        }
        
        .briefing-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        
        .briefing-subtitle {
            font-size: 16px;
            font-weight: 400;
            opacity: 0.9;
            margin-bottom: 4px;
        }
        
        .briefing-date {
            font-size: 14px;
            opacity: 0.8;
            font-weight: 300;
        }
        
        .executive-summary {
            background: linear-gradient(135deg, #f0fdf4 0%, #f0f9ff 100%);
            border-left: 4px solid #059669;
            border-right: 4px solid #0891b2;
            margin: 32px 32px 40px 32px;
            padding: 24px 28px;
            border-radius: 8px;
            position: relative;
        }
        
        .executive-summary::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #059669, #0891b2);
        }
        
        .executive-summary h2 {
            font-size: 18px;
            font-weight: 600;
            color: #065f46;
            margin-bottom: 12px;
        }
        
        .executive-summary p {
            color: #374151;
            font-size: 15px;
            line-height: 1.7;
        }
        
        .articles-section {
            padding: 0 32px 32px 32px;
        }
        
        .section-header {
            font-size: 20px;
            font-weight: 600;
            background: linear-gradient(90deg, #065f46, #0891b2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 24px;
            padding-bottom: 8px;
            border-bottom: 2px solid transparent;
            border-image: linear-gradient(90deg, #10b981, #06b6d4) 1;
        }
        
        .article-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            margin-bottom: 24px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(5, 95, 70, 0.08);
            transition: all 0.2s ease;
            position: relative;
        }
        
        .article-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #10b981, #06b6d4);
            border-radius: 12px 12px 0 0;
        }
        
        .article-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .article-number {
            background: linear-gradient(135deg, #059669, #0891b2);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 600;
            flex-shrink: 0;
            margin-right: 16px;
            box-shadow: 0 2px 4px rgba(5, 95, 70, 0.2);
        }
        
        .article-title {
            font-size: 16px;
            font-weight: 600;
            color: #1f2937;
            line-height: 1.4;
            margin: 0;
            flex-grow: 1;
        }
        
        .article-meta {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 12px;
            color: #6b7280;
        }
        
        .meta-row {
            display: flex;
            gap: 24px;
            flex-wrap: wrap;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 6px;
            min-width: 0;
        }
        
        .meta-label {
            font-weight: 500;
            color: #059669;
            flex-shrink: 0;
        }
        
        .meta-value {
            color: #374151;
        }
        
        .sentiment-indicator {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 20px;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .sentiment-positive {
            background: linear-gradient(135deg, #dcfce7, #d1fae5);
            color: #065f46;
            border: 1px solid #10b981;
        }
        
        .sentiment-positive::before {
            color: #10b981;
        }
        
        .sentiment-neutral {
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            color: #0c4a6e;
            border: 1px solid #0891b2;
        }
        
        .sentiment-neutral::before {
            color: #0891b2;
        }
        
        .sentiment-negative {
            background: linear-gradient(135deg, #fef2f2, #fee2e2);
            color: #991b1b;
            border: 1px solid #ef4444;
        }
        
        .sentiment-negative::before {
            color: #ef4444;
        }
        
        .article-summary {
            color: #374151;
            line-height: 1.7;
            margin-bottom: 16px;
            font-size: 14px;
        }
        
        .article-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, #059669, #0891b2);
            color: white;
            text-decoration: none;
            font-weight: 500;
            font-size: 13px;
            padding: 10px 18px;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(5, 95, 70, 0.2);
        }
        
        .article-link::after {
            content: '→';
            transition: transform 0.2s ease;
        }
        
        .article-link:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(5, 95, 70, 0.3);
        }
        
        .article-link:hover::after {
            transform: translateX(2px);
        }
        
        .footer {
            background: linear-gradient(135deg, #f0fdf4 0%, #f0f9ff 100%);
            border-top: 3px solid transparent;
            border-image: linear-gradient(90deg, #10b981, #06b6d4) 1;
            padding: 24px 32px;
            margin-top: 40px;
            text-align: center;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            font-size: 12px;
            color: #065f46;
        }
        
        .footer-copyright {
            font-size: 11px;
            color: #6b7280;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        @media print {
            .article-card {
                break-inside: avoid;
            }
        }
        .fund-performance-section {
            margin: 32px 32px 40px 32px;
            padding: 24px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }

        .performance-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .perf-card {
            background: white;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .perf-card.best { border-left: 4px solid #10b981; }
        .perf-card.worst { border-left: 4px solid #ef4444; }

        .fund-tables {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }

        .fund-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }

        .fund-table th, .fund-table td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }

        .discount-positive { color: #059669; font-weight: 600; }
        .discount-negative { color: #dc2626; font-weight: 600; }
    </style>
    '''
    
    lines = []
    lines.append(f"<html><head><title>{str(briefing.get('title', ''))}</title>{style}</head><body>")
    lines.append('<div class="document-container">')
    lines.append('<div class="watermark">DRAFT</div>')
    
    # Header
    lines.append('<div class="header">')
    lines.append('<div class="header-content">')
    lines.append('<div class="logo-section">')
    if logo_path:
        lines.append(f'<img src="{str(logo_path)}" alt="Logo" />')
    lines.append('</div>')
    lines.append('<div class="document-info">')
    lines.append(f'<div>Report Date: {str(briefing.get("date", ""))}</div>')
    lines.append('</div>')
    lines.append('</div>')
    lines.append(f'<div class="briefing-title">{str(briefing.get("title", "Weekly Market Briefing"))}</div>')
    lines.append(f'<div class="briefing-date">Week Ending {str(briefing.get("date", ""))}</div>')
    lines.append('</div>')
    
    # Executive Summary
    lines.append('<div class="executive-summary">')
    lines.append('<h2>Weekly Summary</h2>')
    lines.append(f'<p>{str(briefing.get("intro", ""))}</p>')
    lines.append('</div>')

    # Fund Data
    if briefing.get("fund_performance"):
        fund_data = briefing["fund_performance"]
        
        lines.append('<div class="fund-performance-section">')
        lines.append('<h2 class="section-header">Listed Fund Performance Summary</h2>')
        if fund_data.get("last_updated"):
            lines.append(f'<p style="text-align:center; font-size: 12px; color: #6b7280; margin-bottom: 20px;">Fund data last updated: {fund_data["last_updated"]}</p>')

        # Top/Bottom performers tables
        if fund_data.get("best_performers"):
            lines.append('<div class="fund-tables">')
            lines.append('<div class="fund-table-container">')
            lines.append('<h3>Smallest Discounts</h3>')
            lines.append('<table class="fund-table">')
            lines.append('<tr><th>Fund</th><th>Price</th><th>NAV</th><th>Discount</th></tr>')
            for fund in fund_data["best_performers"][:5]:  # Top 5
                lines.append(f'<tr><td>{fund["Fund Name"]}</td><td>£{fund["Close Price"]:.2f}</td><td>£{fund["NAV"]:.2f}</td><td class="discount-positive">{fund["Discount (%)"]:.1f}%</td></tr>')
            lines.append('</table>')
            lines.append('</div>')
        
        if fund_data.get("worst_performers"):
            lines.append('<div class="fund-table-container">')
            lines.append('<h3>Largest Discounts</h3>')
            lines.append('<table class="fund-table">')
            lines.append('<tr><th>Fund</th><th>Price</th><th>NAV</th><th>Discount</th></tr>')
            for fund in fund_data["worst_performers"][:5]:  # Bottom 5
                lines.append(f'<tr><td>{fund["Fund Name"]}</td><td>£{fund["Close Price"]:.2f}</td><td>£{fund["NAV"]:.2f}</td><td class="discount-negative">{fund["Discount (%)"]:.1f}%</td></tr>')
            lines.append('</table>')
            lines.append('</div>')
            lines.append('</div>')
    
    # Articles Section
    lines.append('<div class="articles-section">')
    lines.append('<h2 class="section-header">COMPANY Intelligence</h2>')
    
    for i, article in enumerate(briefing["articles"], 1):
        sentiment = str(article.get('sentiment', '')).lower()
        sentiment_label = 'Neutral'
        sentiment_class = 'sentiment-neutral'
        
        if sentiment in ['pos', 'positive']:
            sentiment_class = 'sentiment-positive'
            sentiment_label = 'Positive'
        elif sentiment in ['neg', 'negative']:
            sentiment_class = 'sentiment-negative'
            sentiment_label = 'Negative'
        
        lines.append('<div class="article-card">')
        lines.append('<div class="article-header">')
        lines.append(f'<div class="article-number">{i}</div>')
        lines.append(f'<h3 class="article-title">{str(article.get("title", ""))}</h3>')
        lines.append('</div>')
        
        lines.append('<div class="article-meta">')
        lines.append('<div class="meta-row">')
        lines.append(f'<div class="meta-item"><span class="meta-label">Source:</span><span class="meta-value">{str(article.get("source", ""))}</span></div>')
        lines.append(f'<div class="meta-item"><span class="meta-label">Published:</span><span class="meta-value">{str(article.get("date", ""))}</span></div>')
        lines.append('</div>')
        lines.append('</div>')
        
        lines.append(f'<div class="sentiment-indicator {sentiment_class}">{sentiment_label} Impact</div>')
        lines.append(f'<div class="article-summary">{markdown.markdown(str(article.get("summary", "")))}</div>')  
        lines.append(f'<a class="article-link" href="{str(article.get("url", ""))}" target="_blank">Read Full Article</a>')
        lines.append('</div>')
    
    lines.append('</div>')
    
    # Footer
    lines.append('<div class="footer">')
    lines.append('<div class="footer-content">')
    lines.append('<div>COMPANY</div>')
    lines.append(f'<div>Generated on {str(briefing.get("date", ""))}</div>')
    lines.append('</div>')
    lines.append('<div class="footer-copyright">&copy; COMPANY</div>')
    lines.append('</div>')
    
    lines.append('</div>')
    lines.append('</body></html>')
    return "\n".join(lines)


