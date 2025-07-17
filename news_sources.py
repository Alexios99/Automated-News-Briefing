import json
from typing import List

def get_urls_with_content_status(file_path: str = "data/marketaux_news_with_content.json") -> List[dict]:
    """
    Extract all URLs and their content status from the marketaux news JSON file.
    
    Args:
        file_path: Path to the JSON file containing news data
        
    Returns:
        List of dictionaries with URL and content status
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            news_data = json.load(file)
        
        url_data = []
        for news_item in news_data:
            if 'url' in news_item and news_item['url']:
                has_content = 'content' in news_item and news_item['content'] is not None and news_item['content'].strip()
                url_data.append({
                    'url': news_item['url'],
                    'has_content': has_content
                })
        
        return url_data
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{file_path}'.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def print_all_urls(file_path: str = "data/marketaux_news_with_content.json") -> None:
    """
    Print all URLs from the news file with content status.
    """
    url_data = get_urls_with_content_status(file_path)
    
    if url_data:
        print(f"Found {len(url_data)} URLs:")
        for i, item in enumerate(url_data, 1):
            content_status = "✓ Has content" if item['has_content'] else "✗ No content"
            print(f"{i}. {item['url']} - {content_status}")
    else:
        print("No URLs found.")

if __name__ == "__main__":
    # Example usage
    urls = get_urls_with_content_status()
    print(f"Extracted {len(urls)} URLs from the news file")
    
    # Uncomment to print all URLs
    print_all_urls()