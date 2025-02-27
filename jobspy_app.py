import streamlit as st
import pandas as pd
import csv
from jobspy import scrape_jobs

st.set_page_config(
    page_title="Lucy - Job Search Aggregator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a title and description
st.title("Lucy - Job Search Aggregator")
st.markdown("Search for jobs across multiple job boards with a single query.")

# Create sidebar for search parameters
with st.sidebar:
    st.header("Search Parameters")
    
    # Job search term
    search_term = st.text_input("Job Title/Keywords", value="Software Engineer")
    
    # Location
    location = st.text_input("Location", value="San Francisco, CA")
    
    # Job boards
    st.subheader("Job Boards")
    use_indeed = st.checkbox("Indeed", value=True)
    use_linkedin = st.checkbox("LinkedIn")
    use_ziprecruiter = st.checkbox("ZipRecruiter")
    use_glassdoor = st.checkbox("Glassdoor")
    use_google = st.checkbox("Google")
    use_bayt = st.checkbox("Bayt")
    
    # Only add selected job boards to the list
    site_names = []
    if use_indeed:
        site_names.append("indeed")
    if use_linkedin:
        site_names.append("linkedin")
    if use_ziprecruiter:
        site_names.append("zip_recruiter")
    if use_glassdoor:
        site_names.append("glassdoor")
    if use_google:
        site_names.append("google")
    if use_bayt:
        site_names.append("bayt")
    
    # Additional search parameters
    st.subheader("Additional Filters")
    results_wanted = st.slider("Number of results per job board", 5, 50, 10)
    hours_old = st.slider("Posted within hours", 24, 168, 72)
    is_remote = st.checkbox("Remote only")
    
    job_type_options = ["Any", "Full-time", "Part-time", "Contract", "Internship"]
    job_type = st.selectbox("Job Type", job_type_options)
    job_type = job_type.lower() if job_type != "Any" else None
    
    country_options = ["USA", "UK", "Canada", "Australia", "India", "Germany", "France"]
    country_indeed = st.selectbox("Country (Indeed/Glassdoor)", country_options)
    
    # Search button
    search_button = st.button("Search Jobs", type="primary")

# Main content area
if search_button:
    if not site_names:
        st.error("Please select at least one job board.")
    else:
        with st.spinner("Searching for jobs... This may take a minute."):
            try:
                # Create a parameters dictionary for easier debugging
                params = {
                    "site_name": site_names,
                    "search_term": search_term,
                    "location": location,
                    "results_wanted": results_wanted,
                    "hours_old": hours_old,
                    "country_indeed": country_indeed,
                    "is_remote": is_remote,
                    "job_type": job_type,
                    "verbose": 1  # Less verbose to avoid cluttering the UI
                }
                
                # Display parameters for debugging
                with st.expander("Search Parameters"):
                    st.json(params)
                
                # Perform the job search
                jobs = scrape_jobs(**params)
                
                # Show results
                st.subheader(f"Found {len(jobs)} jobs")
                
                if len(jobs) > 0:
                    # Add job board filter
                    unique_sites = jobs['site'].unique().tolist()
                    selected_sites = st.multiselect(
                        "Filter by Job Board",
                        options=unique_sites,
                        default=unique_sites
                    )
                    
                    # Filter dataframe by selected job boards
                    if selected_sites:
                        filtered_jobs = jobs[jobs['site'].isin(selected_sites)]
                    else:
                        filtered_jobs = jobs
                    
                    # Display job count after filtering
                    st.write(f"Displaying {len(filtered_jobs)} jobs")
                    
                    # Function to create an expander for each job
                    for _, job in filtered_jobs.iterrows():
                        with st.expander(f"{job['title']} at {job['company']} - {job['location']}"):
                            # Two columns: job details and job description
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                st.write(f"**Job Board:** {job['site'].capitalize()}")
                                st.write(f"**Company:** {job['company']}")
                                st.write(f"**Location:** {job['location']}")
                                if job['job_type']:
                                    st.write(f"**Job Type:** {job['job_type']}")
                                if not pd.isna(job['date_posted']):
                                    st.write(f"**Posted:** {job['date_posted']}")
                                
                                # Salary information if available
                                if not pd.isna(job['min_amount']) or not pd.isna(job['max_amount']):
                                    salary_range = ""
                                    if not pd.isna(job['min_amount']):
                                        salary_range += f"${int(job['min_amount']):,}"
                                    if not pd.isna(job['max_amount']):
                                        if salary_range:
                                            salary_range += f" - ${int(job['max_amount']):,}"
                                        else:
                                            salary_range = f"${int(job['max_amount']):,}"
                                    
                                    if not pd.isna(job['interval']):
                                        salary_range += f" ({job['interval']})"
                                    
                                    st.write(f"**Salary:** {salary_range}")
                                
                                # Job URL
                                st.write("[Apply for this job](" + job['job_url'] + ")")
                            
                            with col2:
                                st.subheader("Job Description")
                                st.markdown(job['description'])
                    
                    # Download button for CSV
                    csv_data = filtered_jobs.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")
                    st.download_button(
                        label="Download as CSV",
                        data=csv_data,
                        file_name="lucy_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No jobs found matching your criteria. Try adjusting your search parameters.")
            
            except Exception as e:
                st.error(f"An error occurred during the search: {str(e)}")
                st.write("Try reducing the number of job boards or results per board, or check your network connection.")
else:
    # Initial state or when no search has been done
    st.info("👈 Set your job search parameters in the sidebar and click 'Search Jobs' to begin.")
    st.markdown("""
    ### About Lucy
    
    Lucy is a smart job search aggregator that collects job postings from popular job boards including:
    
    - LinkedIn
    - Indeed
    - Glassdoor
    - ZipRecruiter
    - Google
    - Bayt
    
    The application works by searching each job board concurrently and collecting the results in a unified format.
    """) 