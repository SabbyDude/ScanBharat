# main.py
# This script is the core of Project 'BharatScan'. It handles reading simulated
# scam data, preprocessing the text, detecting predefined scam patterns using
# keywords and phrases, categorizing the messages, and writing the analysis
# results to an output file.

import re
from scam_patterns import SCAM_PATTERNS

# --- Text Preprocessing Functions ---

def preprocess_text(text):
    """
    Applies a series of preprocessing steps to the input text to clean it up
    for better analysis. These steps include:
    1. Converting the text to lowercase.
    2. Removing URLs.
    3. Removing numbers.
    4. Removing punctuation.
    5. Removing extra whitespace.

    Args:
        text (str): The input string to be preprocessed.

    Returns:
        str: The cleaned and preprocessed string.
    """
    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove URLs (a simple regex for URLs)
    # This regex looks for common URL patterns starting with http/https or www.
    text = re.sub(r'http\S+|www\S+', '', text)

    # 3. Remove numbers (digits 0-9)
    text = re.sub(r'\d+', '', text)

    # 4. Remove punctuation (any character that is not a word character or whitespace)
    # Using re.sub with a regex pattern [^\w\s] which means "not a word character and not a whitespace character".
    text = re.sub(r'[^\w\s]', '', text)

    # 5. Remove extra whitespace (replace multiple spaces with a single space and strip leading/trailing spaces)
    # \s+ matches one or more whitespace characters.
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# --- Scam Detection and Categorization Functions ---

def detect_scam_keywords(text):
    """
    Detects the presence of predefined scam keywords and phrases within a given
    preprocessed text.

    Args:
        text (str): The preprocessed text to analyze.

    Returns:
        list: A list of unique scam keywords/phrases found in the text.
    """
    found_keywords = []
    # Iterate through each scam type and its associated keywords defined in SCAM_PATTERNS
    for scam_type, patterns in SCAM_PATTERNS.items():
        # Iterate through each pattern (keyword or phrase) for the current scam type
        for pattern in patterns:
            # Check if the pattern is present in the text.
            # Using r'\b' for word boundaries to ensure whole word matching for keywords,
            # but for phrases, we check for the phrase directly.
            if len(pattern.split()) > 1:  # It's a phrase
                if pattern in text:
                    found_keywords.append(pattern)
            else:  # It's a single keyword
                if re.search(r'\b' + re.escape(pattern) + r'\b', text):
                    found_keywords.append(pattern)
    # Return only unique keywords found
    return list(set(found_keywords))

def categorize_scam(original_message, found_keywords):
    """
    Categorizes a message into a specific scam type and assigns a suspicion flag
    based on the detected keywords.

    Args:
        original_message (str): The original message (before preprocessing).
        found_keywords (list): A list of scam keywords/phrases found in the message.

    Returns:
        tuple: A tuple containing:
            - str: The detected scam type (e.g., "WhatsApp Scam", "Digital Arrest Scam").
                   Returns "Unknown/Generic Scam" if no specific category is matched,
                   and "Not a Scam" if no keywords are found.
            - bool: A boolean flag indicating if the message is suspicious (True/False).
    """
    scam_type = "Not a Scam"
    is_suspicious = False

    if not found_keywords:
        return scam_type, is_suspicious

    is_suspicious = True
    matched_categories = []

    # Check for specific scam categories based on keywords
    for category, patterns in SCAM_PATTERNS.items():
        # Check if any of the found keywords belong to the current category's patterns
        if any(keyword in patterns for keyword in found_keywords):
            matched_categories.append(category)

    if not matched_categories:
        scam_type = "Unknown/Generic Scam"
    elif len(matched_categories) == 1:
        scam_type = matched_categories[0]
    else:
        # If keywords from multiple categories are found, indicate multiple indicators
        scam_type = "Multiple Scam Indicators: " + ", ".join(matched_categories)

    return scam_type, is_suspicious

# --- Main Analysis Function ---

def analyze_scam_data(input_file_path, output_file_path):
    """
    Reads simulated scam messages from an input file, processes each message,
    detects scam patterns, categorizes them, and writes the analysis results
    to an output file.

    Args:
        input_file_path (str): The path to the file containing simulated scam messages.
        output_file_path (str): The path to the file where analysis results will be written.
    """
    analysis_results = []

    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile):
                original_message = line.strip() # Remove leading/trailing whitespace
                if not original_message: # Skip empty lines
                    continue

                # Preprocess the message
                preprocessed_message = preprocess_text(original_message)

                # Detect keywords
                found_keywords = detect_scam_keywords(preprocessed_message)

                # Categorize the scam
                scam_type, is_suspicious = categorize_scam(original_message, found_keywords)

                # Store results
                analysis_results.append({
                    "Original Message": original_message,
                    "Preprocessed Message": preprocessed_message,
                    "Detected Keywords": ", ".join(found_keywords) if found_keywords else "None",
                    "Scam Type": scam_type,
                    "Suspicious": "Yes" if is_suspicious else "No"
                })
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file_path}'")
        return
    except Exception as e:
        print(f"An error occurred while reading the input file: {e}")
        return

    # Write analysis results to the output file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write("--- BharatScan Analysis Results ---\n\n")
            if not analysis_results:
                outfile.write("No messages processed or no scam patterns detected.\n")
            else:
                for result in analysis_results:
                    outfile.write(f"Original Message: {result['Original Message']}\n")
                    outfile.write(f"Preprocessed: {result['Preprocessed Message']}\n")
                    outfile.write(f"Detected Keywords: {result['Detected Keywords']}\n")
                    outfile.write(f"Scam Type: {result['Scam Type']}\n")
                    outfile.write(f"Suspicious: {result['Suspicious']}\n")
                    outfile.write("-" * 50 + "\n\n") # Separator for readability
        print(f"Analysis complete. Results written to '{output_file_path}'")
    except Exception as e:
        print(f"An error occurred while writing to the output file: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    INPUT_FILE = "sample_scam_data.txt"
    OUTPUT_FILE = "analysis_results.txt"

    print(f"Starting 'BharatScan' analysis...")
    analyze_scam_data(INPUT_FILE, OUTPUT_FILE)
    print("Analysis finished. Check 'analysis_results.txt' for details.")
    print("\nTo run: ensure 'sample_scam_data.txt' and 'scam_patterns.py' are in the same directory.")
    print("Execute this script using: python main.py")
