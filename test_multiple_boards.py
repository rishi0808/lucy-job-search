import csv
from jobspy import scrape_jobs

# Search for jobs from multiple job boards
jobs = scrape_jobs(
    site_name=["indeed", "linkedin"],  # Testing multiple job boards
    search_term="data engineer",
    location="New York, NY",
    results_wanted=3,  # Small number for testing
    hours_old=72,
    country_indeed='USA',
    verbose=2,  # Full logging
)

print(f"Found {len(jobs)} jobs")
print(jobs.head())

# Print unique job boards found
print("\nJob boards represented in results:")
print(jobs['site'].unique())

# Save to CSV
jobs.to_csv("multiple_jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
print("Jobs saved to multiple_jobs.csv") 