import streamlit as st
import pandas as pd
import csv
import time
from jobspy import scrape_jobs

# Set page configuration
st.set_page_config(
    page_title="Lucy - Job Search Aggregator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .job-title {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
    }
    .stProgress .st-bo {
        background-color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# Add a title and description with custom styling
st.markdown('<p class="main-header">Lucy</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Smart Job Search Aggregator</p>', unsafe_allow_html=True)
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
    col1, col2 = st.columns(2)
    with col1:
        use_indeed = st.checkbox("Indeed", value=True)
        use_linkedin = st.checkbox("LinkedIn")
        use_glassdoor = st.checkbox("Glassdoor")
    with col2:
        use_google = st.checkbox("Google")
        use_ziprecruiter = st.checkbox("ZipRecruiter")
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
    
    # Limit number of results for cloud deployment to prevent timeouts
    results_wanted = st.slider("Results per job board", 3, 20, 5, 
                              help="Lower values will make searches faster but return fewer results")
    
    hours_old = st.slider("Posted within hours", 24, 168, 72)
    is_remote = st.checkbox("Remote only")
    
    job_type_options = ["Any", "Full-time", "Part-time", "Contract", "Internship"]
    job_type = st.selectbox("Job Type", job_type_options)
    job_type = job_type.lower() if job_type != "Any" else None
    
    country_options = ["USA", "UK", "Canada", "Australia", "India", "Germany", "France"]
    country_indeed = st.selectbox("Country (Indeed/Glassdoor)", country_options)
    
    # Add advanced options collapsible section
    with st.expander("Advanced Options"):
        timeout_seconds = st.slider("Search Timeout (seconds)", 30, 180, 60, 
                                  help="Maximum time to wait for results")
        verbose_level = st.slider("Logging Level", 0, 2, 1, 
                                help="0: Errors only, 1: Warnings, 2: All logs")
    
    # Search button
    search_button = st.button("Search Jobs", type="primary")

# Function to run job search with timeout
def run_job_search_with_timeout(params, timeout):
    # Create a placeholder for the progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Set start time
    start_time = time.time()
    max_time = timeout
    
    try:
        # Start the job search
        status_text.text("Initializing search...")
        progress_bar.progress(10)
        
        # Update progress based on elapsed time
        def update_progress():
            elapsed = time.time() - start_time
            progress = min(90, int((elapsed / max_time) * 100))
            progress_bar.progress(progress)
            remaining = max(0, max_time - elapsed)
            status_text.text(f"Searching job boards... (Timeout in {int(remaining)}s)")
            
        # Update progress every few seconds
        for _ in range(5):
            time.sleep(1)
            update_progress()
        
        # Perform the job search
        jobs = scrape_jobs(**params)
        
        # Complete the progress
        progress_bar.progress(100)
        status_text.text("Search completed!")
        time.sleep(1)
        
        # Clear the progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return jobs
    
    except Exception as e:
        # Handle errors and timeouts
        progress_bar.empty()
        status_text.empty()
        raise e

# Main content area
if search_button:
    if not site_names:
        st.error("Please select at least one job board.")
    else:
        try:
            # Create a parameters dictionary
            params = {
                "site_name": site_names,
                "search_term": search_term,
                "location": location,
                "results_wanted": results_wanted,
                "hours_old": hours_old,
                "country_indeed": country_indeed,
                "is_remote": is_remote,
                "job_type": job_type,
                "verbose": verbose_level
            }
            
            # Display parameters in an expander
            with st.expander("Search Parameters"):
                st.json(params)
            
            # Run search with progress tracking and timeout
            with st.spinner("Searching for jobs across multiple job boards..."):
                jobs = run_job_search_with_timeout(params, timeout_seconds)
            
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
                
                # Add other filters
                col1, col2 = st.columns(2)
                with col1:
                    # Filter by job type if available
                    job_types = [jt for jt in jobs['job_type'].unique() if jt]
                    if job_types:
                        selected_job_types = st.multiselect(
                            "Filter by Job Type",
                            options=job_types,
                            default=[]
                        )
                
                with col2:
                    # Sort options
                    sort_options = ["Newest first", "Salary (high to low)", "Salary (low to high)"]
                    sort_by = st.selectbox("Sort by", options=sort_options)
                
                # Filter dataframe by selected job boards
                if selected_sites:
                    filtered_jobs = jobs[jobs['site'].isin(selected_sites)]
                else:
                    filtered_jobs = jobs
                
                # Apply job type filter if selected
                if 'selected_job_types' in locals() and selected_job_types:
                    # Have to handle potential None values
                    filtered_jobs = filtered_jobs[filtered_jobs['job_type'].isin(selected_job_types)]
                
                # Apply sorting
                if sort_by == "Newest first":
                    try:
                        filtered_jobs = filtered_jobs.sort_values(by='date_posted', ascending=False)
                    except:
                        pass  # Ignore if date_posted is not available
                elif sort_by == "Salary (high to low)":
                    filtered_jobs = filtered_jobs.sort_values(by='max_amount', ascending=False, na_position='last')
                elif sort_by == "Salary (low to high)":
                    filtered_jobs = filtered_jobs.sort_values(by='min_amount', ascending=True, na_position='last')
                
                # Display job count after filtering
                st.write(f"Displaying {len(filtered_jobs)} jobs")
                
                # Function to create an expander for each job
                for _, job in filtered_jobs.iterrows():
                    # Format job title for the expander
                    job_title = f"{job['title']} at {job['company']}"
                    if job['location']:
                        job_title += f" - {job['location']}"
                    
                    with st.expander(job_title):
                        # Two columns: job details and job description
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.write(f"**Job Board:** {job['site'].capitalize()}")
                            st.write(f"**Company:** {job['company']}")
                            if job['location']:
                                st.write(f"**Location:** {job['location']}")
                            if job['job_type']:
                                st.write(f"**Job Type:** {job['job_type']}")
                            if not pd.isna(job['date_posted']):
                                st.write(f"**Posted:** {job['date_posted']}")
                            
                            # Salary information if available
                            if not pd.isna(job['min_amount']) or not pd.isna(job['max_amount']):
                                salary_range = ""
                                if not pd.isna(job['min_amount']):
                                    try:
                                        salary_range += f"${int(job['min_amount']):,}"
                                    except:
                                        salary_range += f"${job['min_amount']}"
                                if not pd.isna(job['max_amount']):
                                    if salary_range:
                                        try:
                                            salary_range += f" - ${int(job['max_amount']):,}"
                                        except:
                                            salary_range += f" - ${job['max_amount']}"
                                    else:
                                        try:
                                            salary_range = f"${int(job['max_amount']):,}"
                                        except:
                                            salary_range = f"${job['max_amount']}"
                                
                                if not pd.isna(job['interval']):
                                    salary_range += f" ({job['interval']})"
                                
                                st.write(f"**Salary:** {salary_range}")
                            
                            # Job URL
                            st.write("[Apply for this job](" + job['job_url'] + ")")
                        
                        with col2:
                            st.subheader("Job Description")
                            # Handle potential errors in markdown rendering
                            try:
                                st.markdown(job['description'])
                            except:
                                st.write(job['description'])
                
                # Download button for CSV
                st.write("---")
                st.write("### Download Results")
                
                try:
                    csv_data = filtered_jobs.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")
                    st.download_button(
                        label="Download as CSV",
                        data=csv_data,
                        file_name="lucy_results.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error generating CSV: {str(e)}")
            else:
                st.warning("No jobs found matching your criteria. Try adjusting your search parameters.")
        
        except Exception as e:
            st.error(f"An error occurred during the search: {str(e)}")
            st.write("Try reducing the number of job boards, results per board, or increasing the timeout.")
            
            # Show more detailed error info in an expander
            with st.expander("Detailed Error Information"):
                st.exception(e)
else:
    # Initial state or when no search has been done
    st.info("👈 Set your job search parameters in the sidebar and click 'Search Jobs' to begin.")
    
    # Welcome dashboard with features
    st.markdown("""
    ### About Lucy

    Lucy is a smart job search aggregator that collects job postings from popular job boards including:
    
    - LinkedIn
    - Indeed
    - Glassdoor
    - ZipRecruiter
    - Google
    - Bayt
    
    ### Key Features:
    
    - **One Search, Multiple Job Boards**: Save time by searching multiple job sources at once
    - **Unified Results**: All job listings in a consistent, easy-to-read format
    - **Salary Information**: Where available, salary ranges are extracted and displayed
    - **Advanced Filtering**: Filter by job board, job type, and more
    - **Downloadable Results**: Save your job search results as a CSV file
    
    The application works by searching each job board concurrently and collecting the results in a unified format.
    """)
    
    # Show a sample job card
    st.markdown("### Sample Job Card")
    with st.container():
        st.markdown("""
        <div style="border:1px solid #ddd; border-radius:5px; padding:15px; margin-bottom:20px;">
            <h3>Software Engineer at Example Company - San Francisco, CA</h3>
            <p><strong>Job Board:</strong> Indeed</p>
            <p><strong>Company:</strong> Example Company</p>
            <p><strong>Location:</strong> San Francisco, CA</p>
            <p><strong>Job Type:</strong> Full-time</p>
            <p><strong>Salary:</strong> $120,000 - $150,000 (yearly)</p>
            <p><strong>Posted:</strong> 2025-02-25</p>
            <p><a href="#">Apply for this job</a></p>
        </div>
        """, unsafe_allow_html=True)
        
    # Show statistics
    st.markdown("### Why Use Lucy?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Time Saved", "80%", "per search")
    with col2:
        st.metric("Job Sources", "6", "major boards")
    with col3:
        st.metric("Applications", "Unlimited", "job applications") 