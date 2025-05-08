import random
from datetime import datetime, timedelta
import subprocess
import os
import argparse

# Path to the Python file
PATH = "./contribution_log.py"

def validate_date(date_str):
    """
    Validate and parse date string.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Use YYYY-MM-DD. Got: {date_str}")

def write_to_python_file(data):
    """
    Write data to a Python file as a variable.
    """
    variable_name = "commit_log"
    try:
        with open(PATH, "w") as file:
            file.write("# Auto-generated file with commit data\n")
            file.write(f"{variable_name} = {repr(data)}\n")
    except Exception as e:
        print(f"Failed to write data to {PATH}: {e}")

def mark_commit(commit_date):
    """
    Create a single commit on a specific date with random time.
    """
    try:
        # Add random time to the commit date for multiple commits in a day
        commit_time = commit_date.replace(
            hour=random.randint(0, 23), 
            minute=random.randint(0, 59), 
            second=random.randint(0, 59)
        )
        date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Write the date to the Python file
        data = {"date": date_str}
        write_to_python_file(data)
        
        try:
            # Add and commit changes with the generated timestamp
            subprocess.run(['git', 'add', PATH], check=True)
            subprocess.run([
                'git', 'commit', 
                '-m', f'Contribution on {date_str}', 
                f'--date={date_str}'
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e}")
            
    except Exception as e:
        print(f"Unexpected error creating commit: {e}")

def generate_commits(start_date, end_date, min_commits_per_day=1, max_commits_per_day=5, commit_probability=0.5):
    """
    Generate commits within a specified date range with a range of commits per day and random times.
    """
    # Verify git configuration
    try:
        username_result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
        email_result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
        
        print("Git User Configuration:")
        print(f"Username: {username_result.stdout.strip()}")
        print(f"Email: {email_result.stdout.strip()}")
        
        # Verify if in a git repository
        repo_check = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True)
        if repo_check.stdout.strip() != 'true':
            print("Error: Not in a Git repository!")
            return
    except Exception as e:
        print(f"Git configuration check failed: {e}")
        return

    # Calculate total days in the range
    total_days = (end_date - start_date).days + 1
    successful_commits = 0
    failed_commits = 0
    
    for days_offset in range(total_days):
        current_date = start_date + timedelta(days=days_offset)
        
        # Probabilistic commit generation
        if random.random() >= commit_probability:
            continue
        
        # Randomly determine number of commits within the specified range
        num_commits = random.randint(min_commits_per_day, max_commits_per_day)
        print(f"Attempting {num_commits} commits for {current_date.strftime('%Y-%m-%d')}")

        for _ in range(num_commits):
            if mark_commit(current_date):
                successful_commits += 1
            else:
                failed_commits += 1
    
    # Reporting
    print(f"\nCommit Generation Summary:")
    print(f"Successful Commits: {successful_commits}")
    print(f"Failed Commits: {failed_commits}")
    
    # Push commits only if there are successful commits
    if successful_commits > 0:
        try:
            push_result = subprocess.run(['git', 'push'], check=True, text=True)
            print(f"Pushed {successful_commits} commits successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error pushing commits: {e}")

def main():
    """
    Main function to parse arguments and generate commits
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate GitHub commits within a specified date range')
    
    parser.add_argument('--start-date', 
                        type=validate_date, 
                        required=True, 
                        help='Start date for commit generation (YYYY-MM-DD)')
    
    parser.add_argument('--end-date', 
                        type=validate_date, 
                        required=True, 
                        help='End date for commit generation (YYYY-MM-DD)')
    
    parser.add_argument('--min-commits', 
                        type=int, 
                        default=1, 
                        help='Minimum number of commits per day (default: 3)')
    
    parser.add_argument('--max-commits', 
                        type=int, 
                        default=5, 
                        help='Maximum number of commits per day (default: 15)')
    
    parser.add_argument('--commit-probability', 
                        type=float, 
                        default=0.5, 
                        help='Probability of making commits on a day (default: 0.7)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate date range and commit numbers
    if args.start_date > args.end_date:
        parser.error("Start date must be before or equal to end date")
    
    if args.min_commits > args.max_commits:
        parser.error("Minimum commits must be less than or equal to maximum commits")
    
    try:
        generate_commits(
            start_date=args.start_date, 
            end_date=args.end_date, 
            min_commits_per_day=args.min_commits,
            max_commits_per_day=args.max_commits, 
            commit_probability=args.commit_probability
        )
    except Exception as e:
        print(f"An error occurred during commit generation: {e}")

if __name__ == "__main__":
    main()
