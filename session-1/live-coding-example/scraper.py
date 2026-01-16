"""
AI Jobs Scraper - A simple web scraper for aijobs.ai

This script scrapes job listings from aijobs.ai, extracting:
- Job title
- Company name
- Salary range (min and max)
- Job description

Usage:
    python scraper.py
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re

# Constants
BASE_URL = "https://aijobs.ai"
LISTING_URL = "https://aijobs.ai/united-states"
REQUEST_DELAY = 1  # Seconds between requests (be polite!)


def get_page(url: str) -> str:
    """
    Fetches HTML content from a URL.

    Args:
        url: The URL to fetch

    Returns:
        HTML content as a string
    """
    # Use a realistic User-Agent to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text


def extract_job_links(html: str) -> list[str]:
    """
    Extracts job listing URLs from a listing page.

    Args:
        html: HTML content of the listing page

    Returns:
        List of full job URLs
    """
    soup = BeautifulSoup(html, "html.parser")

    # Find all job card links with class 'jobcardStyle1'
    job_cards = soup.find_all("a", class_="jobcardStyle1")

    # Extract the href attribute from each card
    job_links = []
    for card in job_cards:
        href = card.get("href")
        if href:
            # Make sure we have a full URL
            if href.startswith("/"):
                href = BASE_URL + href
            job_links.append(href)

    return job_links


def parse_salary(salary_text: str) -> tuple[int | None, int | None]:
    """
    Parses salary text like "$158,000 - $198,000" into numeric values.

    Args:
        salary_text: Raw salary string from the page

    Returns:
        Tuple of (min_salary, max_salary) as integers, or (None, None) if parsing fails
    """
    if not salary_text:
        return (None, None)

    # Find all dollar amounts in the text
    # Pattern matches: $123,456 or $123456
    amounts = re.findall(r"\$[\d,]+", salary_text)

    if not amounts:
        return (None, None)

    # Convert to integers (remove $ and commas)
    parsed = []
    for amount in amounts:
        clean = amount.replace("$", "").replace(",", "")
        try:
            parsed.append(int(clean))
        except ValueError:
            continue

    if len(parsed) == 0:
        return (None, None)
    elif len(parsed) == 1:
        # Only one value found - could be min or single salary
        return (parsed[0], parsed[0])
    else:
        # Return min and max
        return (min(parsed), max(parsed))


def extract_job_details(html: str) -> dict:
    """
    Extracts job details from a job detail page.

    Args:
        html: HTML content of the job detail page

    Returns:
        Dictionary with keys: title, company, description, min_salary, max_salary
    """
    soup = BeautifulSoup(html, "html.parser")

    # Extract job title from div.post-main-title2
    title_elem = soup.find("div", class_="post-main-title2")
    title = title_elem.get_text(strip=True) if title_elem else ""

    # Extract company name from .post-info2
    # The company is in a span after "at" text
    company = ""
    post_info = soup.find("div", class_="post-info2")
    if post_info:
        # Look for text that contains "at" followed by company name
        info_text = post_info.get_text()
        # Try to find company after "at "
        if " at " in info_text:
            parts = info_text.split(" at ")
            if len(parts) > 1:
                # Company name might have location info after it
                company = parts[1].split("\n")[0].strip()

    # Extract salary from div.col-sm.salery h2 (note: typo in class name)
    salary_elem = soup.find("div", class_="salery")
    salary_text = ""
    if salary_elem:
        h2 = salary_elem.find("h2")
        if h2:
            salary_text = h2.get_text(strip=True)

    min_salary, max_salary = parse_salary(salary_text)

    # Extract job description from div.job-description-container
    desc_elem = soup.find("div", class_="job-description-container")
    description = desc_elem.get_text(strip=True) if desc_elem else ""

    return {
        "title": title,
        "company": company,
        "description": description,
        "min_salary": min_salary,
        "max_salary": max_salary,
    }


def scrape_all_jobs(num_pages: int = 5) -> list[dict]:
    """
    Main function to scrape jobs from multiple listing pages.

    Args:
        num_pages: Number of listing pages to scrape (default: 5)

    Returns:
        List of job dictionaries with all details
    """
    all_job_links = []

    # Step 1: Collect all job links from listing pages
    print(f"Collecting job links from {num_pages} pages...")

    for page in range(1, num_pages + 1):
        url = f"{LISTING_URL}?page={page}"
        print(f"  Fetching page {page}...")

        try:
            html = get_page(url)
            links = extract_job_links(html)
            all_job_links.extend(links)
            print(f"    Found {len(links)} jobs")
        except requests.RequestException as e:
            print(f"    Error fetching page {page}: {e}")

        # Be polite - wait between requests
        time.sleep(REQUEST_DELAY)

    print(f"\nTotal job links collected: {len(all_job_links)}")

    # Remove duplicates while preserving order
    all_job_links = list(dict.fromkeys(all_job_links))
    print(f"Unique jobs: {len(all_job_links)}")

    # Step 2: Scrape details for each job
    print(f"\nScraping job details...")

    jobs = []
    for i, job_url in enumerate(all_job_links, 1):
        print(f"  [{i}/{len(all_job_links)}] {job_url}")

        try:
            html = get_page(job_url)
            job_data = extract_job_details(html)
            job_data["url"] = job_url  # Add the URL to the data
            jobs.append(job_data)
        except requests.RequestException as e:
            print(f"    Error: {e}")

        # Be polite - wait between requests
        time.sleep(REQUEST_DELAY)

    return jobs


def save_to_csv(jobs: list[dict], filename: str = "jobs.csv") -> None:
    """
    Saves job data to a CSV file.

    Args:
        jobs: List of job dictionaries
        filename: Output filename (default: jobs.csv)
    """
    if not jobs:
        print("No jobs to save!")
        return

    # Define column order
    fieldnames = ["title", "company", "min_salary", "max_salary", "url", "description"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Saved {len(jobs)} jobs to {filename}")


def main():
    """
    Entry point for the scraper.
    """
    print("=" * 50)
    print("AI Jobs Scraper")
    print("=" * 50)
    print()

    # Scrape jobs from 5 pages
    jobs = scrape_all_jobs(num_pages=5)

    # Save to CSV
    if jobs:
        save_to_csv(jobs, "jobs.csv")

        # Print summary
        print("\n" + "=" * 50)
        print("Summary")
        print("=" * 50)
        print(f"Total jobs scraped: {len(jobs)}")

        # Count jobs with salary info
        with_salary = sum(1 for j in jobs if j["min_salary"] is not None)
        print(f"Jobs with salary info: {with_salary}")

        # Show sample job
        if jobs:
            print("\nSample job:")
            sample = jobs[0]
            print(f"  Title: {sample['title']}")
            print(f"  Company: {sample['company']}")
            if sample['min_salary']:
                print(f"  Salary: ${sample['min_salary']:,} - ${sample['max_salary']:,}")
            else:
                print(f"  Salary: Not specified")
    else:
        print("No jobs were scraped.")


if __name__ == "__main__":
    main()
