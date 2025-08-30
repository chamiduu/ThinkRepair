import pandas as pd
import json

# --- User Configuration ---
# 1. Set the name of your local JSON file here
input_json_filename = "./D4J.json"

# 2. Set the desired name for the output CSV file
output_csv_filename = "test_analysis_results.csv"
# --------------------------


def analyze_test_data(json_data):
    """Processes the JSON data and returns a pandas DataFrame."""
    results_for_csv = []
    print("TOTAL :: ", len(json_data.items()))
    for test_name, rounds in json_data.items():
        num_rounds = len(rounds)
        found_valid = False
        total_takes = 0
        
        result_row = {
            "test_name": test_name,
            "num_rounds": num_rounds,
            "finished_with_valid_answer": "No",
            "valid_answer_round": None,
            "takes_in_valid_round": None,
            "total_takes_for_valid": None
        }

        for round_idx, takes_in_round in enumerate(rounds):
            if found_valid:
                break
            
            for take_idx, take_data in enumerate(takes_in_round):
                total_takes += 1
                if take_data.get("valid"):
                    found_valid = True
                    result_row.update({
                        "finished_with_valid_answer": "Yes",
                        "valid_answer_round": round_idx + 1,
                        "takes_in_valid_round": take_idx + 1,
                        "total_takes_for_valid": total_takes
                    })
                    break
        
        results_for_csv.append(result_row)
    
    return pd.DataFrame(results_for_csv)


# --- Main execution block ---
try:
    print(f"Reading data from '{input_json_filename}'...")
    
    # Read the data from the local JSON file
    with open(input_json_filename, 'r') as f:
        data = json.load(f)
    
    print("File read successfully.")

    # Process the data to create the analysis DataFrame
    df = analyze_test_data(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_filename, index=False)
    
    print(f"✅ Analysis complete! Results have been saved to '{output_csv_filename}'.")

except FileNotFoundError:
    print(f"❌ ERROR: The file '{input_json_filename}' was not found.")
    print("Please make sure the file is in the same directory as the script and the filename is correct.")
except json.JSONDecodeError:
    print(f"❌ ERROR: The file '{input_json_filename}' is not a valid JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")