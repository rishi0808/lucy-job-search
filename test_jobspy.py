import csv
from jobspy import scrape_jobs

# Search for just a few jobs to test quickly
jobs = scrape_jobs(
    site_name=["indeed"],  # Limiting to just Indeed for faster testing
    search_term="software engineer",
    location="San Francisco, CA",
    results_wanted=5,  # Small number for testing
    hours_old=72,
    country_indeed='USA',
    verbose=2,  # Full logging
)

print(f"Found {len(jobs)} jobs")
print(jobs.head())

# Save to CSV
jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
print("Jobs saved to jobs.csv") 