import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
import json  # Import the json module

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}


def scrape_hackernews():
    url = "https://news.ycombinator.com/jobs"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for row in soup.find_all("tr", class_="athing"):
            a = row.find("a")
            if a and "item?id=" in a.get("href", ""):
                offers.append({
                    "Source": "HackerNews",
                    "Titre": a.text.strip(),
                    "Entreprise": "N/A",
                    "Lien": "https://news.ycombinator.com/" + a["href"]
                })
        logging.info("Scraped HackerNews successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping HackerNews: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping HackerNews: {e}")
    return offers

def scrape_python_jobs():
    url = "https://www.python.org/jobs/"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for job in soup.select(".list-recent-jobs li"):
            title = job.h2.text.strip()
            company = job.find("span", class_="listing-company-name").text.strip()
            link = "https://www.python.org" + job.h2.a["href"]
            offers.append({
                "Source": "Python.org",
                "Titre": title,
                "Entreprise": company,
                "Lien": link
            })
        logging.info("Scraped Python.org successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping Python.org: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping Python.org: {e}")
    return offers


def scrape_jsremotely():
    url = "https://jsremotely.com/"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for div in soup.find_all("div", class_="job"):
            a = div.find("a")
            if a:
                title = a.text.strip()
                link = "https://jsremotely.com" + a["href"]
                offers.append({
                    "Source": "JSRemotely",
                    "Titre": title,
                    "Entreprise": "N/A",
                    "Lien": link
                })
        logging.info("Scraped JSRemotely successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping JSRemotely: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping JSRemotely: {e}")
    return offers

def scrape_remotive():
    url = "https://remotive.io/api/remote-jobs?category=software-dev"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        try:
            jobs = res.json()["jobs"]
            for job in jobs:
                offers.append({
                    "Source": "Remotive",
                    "Titre": job["title"],
                    "Entreprise": job["company_name"],
                    "Lien": job["url"]
                })
            logging.info("Scraped Remotive successfully.")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding Remotive JSON: {e}. Response text: {res.text}")
        except KeyError as e:
            logging.error(f"Error accessing key in Remotive JSON: {e}.  Check the JSON structure. Response text: {res.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping Remotive: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping Remotive: {e}")
    return offers


def scrape_workingnomads():
    url = "https://www.workingnomads.com/jobs"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for li in soup.select("div#jobsboard > a"):
            title = li.find("h3")
            company = li.find("h4")
            if title and company:
                offers.append({
                    "Source": "WorkingNomads",
                    "Titre": title.text.strip(),
                    "Entreprise": company.text.strip(),
                    "Lien": "https://www.workingnomads.com" + li["href"]
                })
        logging.info("Scraped WorkingNomads successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping WorkingNomads: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping WorkingNomads: {e}")
    return offers


def scrape_authenticjobs():
    url = "https://authenticjobs.com/"
    offers = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for job in soup.select(".job-listing"):
            title_tag = job.find("h4")
            company_tag = job.find("h5")
            a_tag = job.find("a", href=True)
            if title_tag and a_tag:
                offers.append({
                    "Source": "AuthenticJobs",
                    "Titre": title_tag.text.strip(),
                    "Entreprise": company_tag.text.strip() if company_tag else "N/A",
                    "Lien": "https://authenticjobs.com" + a_tag["href"]
                })
        logging.info("Scraped AuthenticJobs successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping AuthenticJobs: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping AuthenticJobs: {e}")
    return offers


def main():
    logging.info("Scraping started.")

    # Create the 'logs' directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    all_offers = []
    all_offers += scrape_hackernews()
    all_offers += scrape_python_jobs()
    all_offers += scrape_jsremotely()
#    all_offers += scrape_remotive()
    all_offers += scrape_workingnomads()
    all_offers += scrape_authenticjobs()

    # Create the 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    df = pd.DataFrame(all_offers)
    csv_filepath = "data/jobs.csv"
    df.to_csv(csv_filepath, index=False, encoding="utf-8")

    logging.info(f"Generated {csv_filepath} with {len(df)} job offers.")
    if not df.empty:
        logging.info(f"First 10 job offers: {df.head(10).to_string()}")
    else:
        logging.warning("No job offers found.")

    logging.info("Scraping completed.")

main()
