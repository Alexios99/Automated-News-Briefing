from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, abort, jsonify, session
from .forms import GenerateBriefingForm
from main import run_pipeline, fetch_articles_for_briefing, generate_briefing_from_articles
import os
import re
from .utils import list_briefings, load_config, save_config, reset_config
from fund_news_fetcher import fetch_news_for_funds
import json

main = Blueprint('main', __name__)

# Robust absolute path to output directory
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
ALLOWED_EXTENSIONS = {'.pdf', '.html', '.md'}
FILENAME_RE = re.compile(r'^briefing_\d{4}-\d{2}-\d{2}(_[\w-]+)?\.(pdf|html|md)$')

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/generate', methods=['GET', 'POST'])
def generate():
    form = GenerateBriefingForm()

    result = None
    error = None
    if form.validate_on_submit():
        days_ago = form.days_ago.data if form.days_ago.data is not None else 0
        custom_keywords = [k.strip() for k in form.custom_keywords.data.split(',')] if form.custom_keywords.data else None
        try:
            # Step 1: Fetch articles only
            articles = fetch_articles_for_briefing(custom_keywords, from_days_ago=days_ago)
            if not articles:
                error = 'No articles found.'
                return render_template('generate.html', form=form, result=None, error=error)
            # Store articles in session for human screening
            session['screen_articles'] = articles
            session['screen_index'] = 0
            session['accepted_articles'] = []
            return redirect(url_for('main.human_screen'))
        except Exception as e:
            error = str(e)
            flash(f'Error: {error}', 'danger')
    return render_template('generate.html', form=form, result=result, error=error)

@main.route('/download/<path:filename>')
def download_file(filename):
    if not FILENAME_RE.match(filename) or not os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS:
        abort(404)
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

@main.route('/view/<path:filename>')
def view_file(filename):
    if not FILENAME_RE.match(filename) or not os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS:
        abort(404)
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=False)

@main.route('/briefings')
def briefings():
    briefings_by_date = list_briefings()
    return render_template('briefings.html', briefings_by_date=briefings_by_date)

@main.route('/config', methods=['GET'])
def config():
    config_data = load_config()
    return render_template('config.html', config=config_data)

@main.route('/config/save', methods=['POST'])
def save_config_route():
    try:
        data = request.get_json()
        save_config(data)
        return jsonify({'success': True, 'message': 'Configuration saved successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error saving configuration: {str(e)}'}), 500

@main.route('/config/reset', methods=['POST'])
def reset_config_route():
    try:
        reset_config()
        return jsonify({'success': True, 'message': 'Configuration reset to default.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error resetting configuration: {str(e)}'}), 500

@main.route('/config/download', methods=['GET'])
def download_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    return send_from_directory(os.path.dirname(config_path), os.path.basename(config_path), as_attachment=True)

@main.route('/config/upload', methods=['POST'])
def upload_config():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file.'}), 400
    try:
        config_data = file.read().decode('utf-8')
        import json
        config_json = json.loads(config_data)
        save_config(config_json)
        return jsonify({'success': True, 'message': 'Configuration uploaded and saved.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error uploading configuration: {str(e)}'}), 500

@main.route('/preview/<path:filename>')
def preview_file(filename):
    # Only allow .md or .html
    ext = os.path.splitext(filename)[1]
    if not FILENAME_RE.match(filename) or ext not in ['.md', '.html']:
        return jsonify({'error': 'Invalid file type.'}), 400
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found.'}), 404
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [next(f) for _ in range(20)]  # First 20 lines
        preview = ''.join(lines)
        # Optionally, truncate if too long
        if len(preview) > 2000:
            preview = preview[:2000] + '\n...'
        return jsonify({'preview': preview})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    if not FILENAME_RE.match(filename) or not os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file.'}), 400
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found.'}), 404
    try:
        os.remove(file_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/update_fund_news', methods=['POST'])
def update_fund_news():
    try:
        fetch_news_for_funds()
        return jsonify({'success': True, 'message': 'Fund news updated.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error updating fund news: {str(e)}'}), 500

@main.route('/fund_news', methods=['GET'])
def fund_news():
    try:
        with open('data/marketaux_news_results.json', 'r', encoding='utf-8') as f:
            news = json.load(f)
    except Exception:
        news = []
    return render_template('fund_news.html', news=news)

@main.route('/create_briefing_from_fund_news', methods=['GET', 'POST'])
def create_briefing_from_fund_news():
    import os
    from datetime import datetime
    result = None
    error = None
    # Load all fund news
    try:
        with open('data/marketaux_news_results.json', 'r', encoding='utf-8') as f:
            all_news = json.load(f)
    except Exception:
        all_news = []
    # Format published_at for readability
    def format_date(date_str):
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%d %b %Y, %H:%M')
        except Exception:
            return date_str
    for art in all_news:
        date_val = art.get('published_at') or art.get('publishedAt')
        if date_val:
            art['published_at_readable'] = format_date(date_val)
    # Extract all unique funds
    fund_set = set()
    for art in all_news:
        for fund in art.get('funds', []):
            fund_set.add(fund)
    funds = sorted(fund_set)
    # GET: show selection UI
    if request.method == 'GET':
        return render_template('create_briefing_from_fund_news.html', news=all_news, funds=funds, result=None, error=None)
    # POST: generate briefing from selected articles
    selected_uuids = request.form.getlist('selected_articles')
    selected_articles = [art for art in all_news if str(art.get('uuid')) in selected_uuids]
    if not selected_articles:
        error = 'No articles selected.'
        return render_template('create_briefing_from_fund_news.html', news=all_news, funds=funds, result=None, error=error)
    # Generate briefing using the same format as the pipeline
    # Use today's date for output
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    markdown_path = os.path.join(output_dir, f'briefing_{date_str}_custom.md')
    html_path = os.path.join(output_dir, f'briefing_{date_str}_custom.html')
    pdf_path = os.path.join(output_dir, f'briefing_{date_str}_custom.pdf')
    # Use the same formatter as the pipeline
    from formatter import generate_markdown, generate_html, generate_pdf
    from reporter import build_briefing
    # Build a minimal briefing dict
    briefing = build_briefing(selected_articles)
    # Optionally add a custom intro or fund performance if desired
    generate_markdown(briefing, markdown_path)
    html_content = generate_html(briefing, logo_path='images/logo.png')
    with open(html_path, 'w') as html_file:
        html_file.write(html_content)
    generate_pdf(briefing, pdf_path, logo_path='images/logo.png')
    result = {
        'markdown': os.path.basename(markdown_path),
        'html': os.path.basename(html_path),
        'pdf': os.path.basename(pdf_path)
    }
    return render_template('create_briefing_from_fund_news.html', news=all_news, funds=funds, result=result, error=None)

@main.route('/human_screen', methods=['GET', 'POST'])
def human_screen():
    # Use articles from session, not from file
    all_articles = session.get('screen_articles', [])
    if not all_articles:
        # If no articles in session, redirect to generate
        flash('No articles to screen. Please generate briefing first.', 'warning')
        return redirect(url_for('main.generate'))

    # Initialize session state if not present
    if 'screen_index' not in session or request.method == 'GET':
        session['screen_index'] = 0
        session['accepted_articles'] = []

    screen_index = session.get('screen_index', 0)
    accepted_articles = session.get('accepted_articles', [])

    # Handle POST actions
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'accept':
            # Accept current article
            if 0 <= screen_index < len(all_articles):
                if all_articles[screen_index] not in accepted_articles:
                    accepted_articles.append(all_articles[screen_index])
                session['accepted_articles'] = accepted_articles
            screen_index += 1
        elif action == 'reject':
            # Just move to next article
            screen_index += 1
        elif action == 'back':
            # Move to previous article, remove from accepted if it was accepted
            if screen_index > 0:
                screen_index -= 1
                article = all_articles[screen_index]
                if article in accepted_articles:
                    accepted_articles.remove(article)
                session['accepted_articles'] = accepted_articles
        elif action == 'finish':
            # Finish screening, generate briefing from accepted articles
            if not accepted_articles:
                return render_template('human_screen.html',
                                       finished=True,
                                       accepted_articles=[],
                                       total=len(all_articles),
                                       result=None,
                                       error='No articles accepted.')
            # Generate briefing
            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
            result = generate_briefing_from_articles(accepted_articles, output_dir=output_dir)
            # Clean up session
            session.pop('screen_articles', None)
            session.pop('screen_index', None)
            session.pop('accepted_articles', None)
            return render_template('human_screen.html',
                                   finished=True,
                                   accepted_articles=accepted_articles,
                                   total=len(all_articles),
                                   result=result,
                                   error=None)
        session['screen_index'] = screen_index

    # If finished all articles, generate briefing automatically
    if screen_index >= len(all_articles):
        if not accepted_articles:
            return render_template('human_screen.html',
                                   finished=True,
                                   accepted_articles=[],
                                   total=len(all_articles),
                                   result=None,
                                   error='No articles accepted.')
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
        result = generate_briefing_from_articles(accepted_articles, output_dir=output_dir)
        # Clean up session
        session.pop('screen_articles', None)
        session.pop('screen_index', None)
        session.pop('accepted_articles', None)
        return render_template('human_screen.html',
                               finished=True,
                               accepted_articles=accepted_articles,
                               total=len(all_articles),
                               result=result,
                               error=None)

    # Show current article
    article = all_articles[screen_index]
    return render_template('human_screen.html',
                           article=article,
                           index=screen_index+1,
                           total=len(all_articles),
                           finished=False,
                           result=None,
                           error=None) 