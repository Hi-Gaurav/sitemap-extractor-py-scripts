import requests
import csv
import os
from datetime import datetime
from bs4 import BeautifulSoup


def get_sitemap_urls(url):
    """
    Returns a list of URLs found in the sitemap at the specified URL.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text for loc in soup.findAll('loc')]
    return urls


def save_urls_to_csv(urls, file_path):
    """
    Saves a list of URLs to a CSV file at the specified file path.
    """
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for url in urls:
            writer.writerow([url])


def crawl_sitemap(url, save_all_sitemaps):
    """
    Crawls the sitemap at the specified URL and its nested sitemaps, and saves the URLs to CSV files.
    If save_all_sitemaps is True, saves each sitemap and its nested sitemaps in a separate CSV file.
    If save_all_sitemaps is False, saves all URLs in a single CSV file.
    """
    sitemap_urls = get_sitemap_urls(url)
    save_path = os.path.join(os.getcwd(), 'sitemaps')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if save_all_sitemaps:
        save_path = os.path.join(save_path, f'{datetime.now().strftime("%Y%m%d%H%M%S")}_sitemap.csv')
        save_urls_to_csv(sitemap_urls, save_path)
    else:
        save_path = os.path.join(save_path, 'all_sitemaps.csv')
        save_urls_to_csv(sitemap_urls, save_path)
    
    print(f'Crawled {len(sitemap_urls)} URLs from {url}')
    for sitemap_url in sitemap_urls:
        if 'sitemap' in sitemap_url:
            crawl_sitemap(sitemap_url, save_all_sitemaps)


if __name__ == '__main__':
    print('''
░██████╗░░█████╗░██╗░░░██╗██████╗░░█████╗░██╗░░░██╗  ████████╗░█████╗░███╗░░██╗░██╗░░░░░░░██╗░█████╗░██████╗░
██╔════╝░██╔══██╗██║░░░██║██╔══██╗██╔══██╗██║░░░██║  ╚══██╔══╝██╔══██╗████╗░██║░██║░░██╗░░██║██╔══██╗██╔══██╗
██║░░██╗░███████║██║░░░██║██████╔╝███████║╚██╗░██╔╝  ░░░██║░░░███████║██╔██╗██║░╚██╗████╗██╔╝███████║██████╔╝
██║░░╚██╗██╔══██║██║░░░██║██╔══██╗██╔══██║░╚████╔╝░  ░░░██║░░░██╔══██║██║╚████║░░████╔═████║░██╔══██║██╔══██╗
╚██████╔╝██║░░██║╚██████╔╝██║░░██║██║░░██║░░╚██╔╝░░  ░░░██║░░░██║░░██║██║░╚███║░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║
░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝
    ''')
    url = input('Enter the URL of the sitemap to crawl: ')
    save_all_sitemaps = input('Do you want to save all sitemaps and their nested sitemaps separately in CSV files? (y/n) ') == 'y'
    crawl_sitemap(url, save_all_sitemaps)
