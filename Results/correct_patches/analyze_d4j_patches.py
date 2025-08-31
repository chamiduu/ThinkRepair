import os
import csv
import sys

def analyze_patch_file(file_path):
    """
    Analyzes a single patch file to count changed files, edits, and line changes.
    
    Args:
        file_path (str): The full path to the patch file.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    stats = {
        "files_changed": 0,
        "edit_locations": 0,
        "lines_added": 0,
        "lines_removed": 0
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Count files changed (each diff starts with 'diff --git')
                if line.startswith('diff --git'):
                    stats["files_changed"] += 1
                # Count edit locations (each "hunk" starts with '@@')
                elif line.startswith('@@'):
                    stats["edit_locations"] += 1
                # Count added lines (starts with '+' but not '+++')
                elif line.startswith('+') and not line.startswith('+++'):
                    stats["lines_added"] += 1
                # Count removed lines (starts with '-' but not '---')
                elif line.startswith('-') and not line.startswith('---'):
                    stats["lines_removed"] += 1
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}", file=sys.stderr)
        return None
        
    return stats

def create_analysis_report(main_folder_path, output_csv_path):
    """
    Traverses a directory, analyzes patch files, and writes a CSV report.
    This version expects the structure: main_folder/ProjectName/Patches/*.patch

    Args:
        main_folder_path (str): The path to the main folder containing project folders.
        output_csv_path (str): The path to save the output CSV file.
    """
    header = ['identifier', 'files_changed', 'edit_locations', 'lines_added', 'lines_removed']
    analyzed_patches = 0

    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            print(f"Scanning directory: '{main_folder_path}'...")
            
            # Iterate through each project folder (e.g., 'Lang', 'Chart')
            for project_name in sorted(os.listdir(main_folder_path)):
                project_path = os.path.join(main_folder_path, project_name)
                
                if os.path.isdir(project_path):
                    # Define the expected path to the "Patches" subfolder
                    patches_folder_path = os.path.join(project_path, "patches")
                    
                    # Check if the "Patches" subfolder actually exists
                    if os.path.isdir(patches_folder_path):
                        # Iterate through files in the "Patches" directory
                        for filename in sorted(os.listdir(patches_folder_path)):
                            if filename.endswith('.src.patch'):
                                patch_number = filename.split('.')[0]
                                identifier = f"{project_name}-{patch_number}"
                                file_path = os.path.join(patches_folder_path, filename)
                                
                                stats = analyze_patch_file(file_path)
                                
                                if stats:
                                    writer.writerow([
                                        identifier,
                                        stats["files_changed"],
                                        stats["edit_locations"],
                                        stats["lines_added"],
                                        stats["lines_removed"]
                                    ])
                                    analyzed_patches += 1

        print(f"✅ Analysis complete. Processed {analyzed_patches} patch files.")
        print(f"Report saved to: '{output_csv_path}'")

    except FileNotFoundError:
        print(f"❌ ERROR: The main folder '{main_folder_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    # 1. SET THE PATH to the main folder containing your projects.
    main_directory = "./Patches"
    
    # 2. SET THE NAME for your output report file.
    output_report_file = "patch_analysis_report.csv"
    
    create_analysis_report(main_directory, output_report_file)