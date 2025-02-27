# Lucy - Smart Job Search Aggregator

![Lucy Logo](https://img.shields.io/badge/Lucy-Job%20Search-FF4B4B?style=for-the-badge)

Lucy is a powerful job search aggregator that pulls together job listings from multiple popular job boards in one place, saving you time and effort in your job search.

## Features

- **Search Multiple Job Boards Simultaneously**: Search Indeed, LinkedIn, Glassdoor, ZipRecruiter, Google Jobs, and Bayt all at once
- **Smart Filtering**: Filter job results by job board, job type, and more
- **Salary Information**: View salary ranges when available
- **Unified Interface**: All job listings in a consistent, easy-to-read format
- **Export Functionality**: Download your job search results as a CSV file

## Live Demo

Try Lucy here: [https://lucy-job-search.streamlit.app/](https://lucy-job-search.streamlit.app/)

## Built With

- [Streamlit](https://streamlit.io/) - The web framework
- [JobSpy](https://github.com/cullenwatson/JobSpy) - The job scraping library
- [Pandas](https://pandas.pydata.org/) - For data handling

## How It Works

Lucy uses JobSpy to search multiple job boards concurrently and then presents the aggregated results in a unified interface. The app allows you to customize your search with various filters and parameters.

## Running Locally

To run Lucy locally:

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run jobspy_app.py
   ```

## Deploying to Streamlit Cloud

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Screenshot

![Lucy App Screenshot](https://img.shields.io/badge/Screenshot-Coming%20Soon-lightgrey)

## Important Notes

- Some job boards have rate limits or geo-restrictions that may affect search results
- For optimal performance, limit the number of results per job board when searching

## Acknowledgments

- Built on top of [JobSpy](https://github.com/cullenwatson/JobSpy) by Cullen Watson
- Inspired by the frustration of having to search multiple job sites separately

## License

This project is licensed under the MIT License - see the LICENSE file for details.
