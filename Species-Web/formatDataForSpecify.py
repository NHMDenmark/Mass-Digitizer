import pandas as pd
import os
import re
import numpy as np
import shutil
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Directory paths should be defined in the .env file
base_folder_path = os.getenv("FOLDER_PATH")
base_archive_folder = os.getenv("ARCHIVE_FOLDER")
base_output_folder = os.getenv("OUTPUT_FOLDER")
base_log_file_path = os.getenv("LOG_FILE_PATH")

# In directory paths, {collection} is replaced with the collection name
# Change this to switch collections
collection = 'AU_Herbarium'
folder_path = base_folder_path.format(collection=collection)
archive_folder = base_archive_folder.format(collection=collection)
output_folder = base_output_folder.format(collection=collection)
log_file_path = base_log_file_path.format(collection=collection)

# Ensure the log file directory exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
# Ensure the archive folder exists
os.makedirs(archive_folder, exist_ok=True)

# Data to be extracted from gbif_match_json
keys_to_extract = [
    "key", "kingdom", "phylum", "order", "family", "genus", "species", "scientificName", "authorship", "taxonomicStatus",
    "acceptedKey", "accepted", "class"
]

# Extract taxonomy and author from gbif_match_json
def extract_json_data(row):
    extracted_data = {}
    try:
        # Loop through the keys you want to extract
        for key in keys_to_extract:
            # Use regex to find the key-value pair in the JSON-like string
            match = re.search(rf'"{key}":\s*("[^"]*"|\d+)', row['gbif_match_json'])
            
            if match:
                value = match.group(1)
                if value.startswith('"'):
                    extracted_data[key] = value.strip('"')  # Remove quotes for string values
                else:
                    # If it's a number (no quotes), store it as a string first
                    extracted_data[key] = value if not value.isdigit() else int(value)
            else:
                extracted_data[key] = None  # If key is not found, set to None
    except Exception as e:
        # Return None for all fields if there's an error
        extracted_data = {key: None for key in keys_to_extract}

    # Convert the dictionary to a pandas Series to match the structure of the df
    return pd.Series(extracted_data)

# Extract and remove genus from species column if species is not blank
def update_genus_and_species(row):
    if pd.notnull(row['species']):
        # Extract genus from the 'species' field
        row['genus'] = row['species'].split()[0] if row['species'].split()[0].istitle() else row['genus']
        # Remove genus from 'species' field if it's present
        row['species'] = ' '.join(row['species'].split()[1:])
    return row

# Process authorship, taxon key, and taxon key source at rank level
def process_taxonomic_fields(row):
    if pd.isnull(row['species']):
        row['genus_author'] = row['authorship']
        row['genus_taxon_key'] = row['key']
        row['genus_taxon_key_source'] = 'GBIF'
    elif "var." in row['scientificName']:
        row['variety_author'] = row['authorship']
        row['variety_taxon_key'] = row['key']
        row['variety_taxon_key_source'] = 'GBIF'
    elif "subsp." in row['scientificName']:
        row['subspecies_author'] = row['authorship']
        row['subspecies_taxon_key'] = row['key']
        row['subspecies_taxon_key_source'] = 'GBIF'
    else:
        row['species_author'] = row['authorship']
        row['species_taxon_key'] = row['key']
        row['species_taxon_key_source'] = 'GBIF'
    
    return row

# Extract subspecies if the string "subsp." is detected
def extract_subspecies(scientific_name):
    match = re.search(r'\bsubsp\.\s+([a-z\s]*x\s[a-z\s]*)', scientific_name)
    if match:
        return match.group(1).strip()
    else:
        match = re.search(r'\bsubsp\.\s+(\S+)', scientific_name)
        if match:
            return match.group(1).strip()
    return None

# Create fields 'ishybrid' at rank level (either species or subspecies)
# Note that this code does not support cross-rank hybrids at this time
def assign_ishybrid_fields(row):
    row['ishybrid_species'] = True if pd.notnull(row['species']) and ' x ' in row['species'] else None
    row['ishybrid_subspecies'] = True if pd.notnull(row['subspecies']) and ' x ' in row['subspecies'] else None
    return row

# Pull accepted name and author if this taxon is a synonym
def parse_accepted_data(row):
    accepted = row.get('accepted')
    
    if not isinstance(accepted, str) or not accepted.strip():
        # If 'accepted' is empty or not a valid string, return None for all fields
        row['accepted_genus'] = None
        row['accepted_species'] = None
        row['accepted_subspecies'] = None
        row['accepted_variety'] = None
        return row

    # Split the accepted name into words
    parts = accepted.split()

    # The first word (capitalized) is always the genus
    row['accepted_genus'] = parts[0] if parts[0][0].isupper() else None

    # Create species, subspecies, and variety columns
    row['accepted_species'] = None
    row['accepted_subspecies'] = None
    row['accepted_variety'] = None

    # Parse the rest of the string
    species_parts = []
    subspecies_parts = []
    variety_parts = []

    i = 1
    while i < len(parts):
        if parts[i] == 'subsp.':
            # Parse subspecies starting from the next word
            i += 1
            while i < len(parts) and parts[i] != 'var.':
                subspecies_parts.append(parts[i])
                i += 1
        elif parts[i] == 'var.':
            # Parse variety starting from the next word
            i += 1
            while i < len(parts):
                variety_parts.append(parts[i])
                i += 1
        elif parts[i][0].islower():
            # Add to species if it's lowercase and not part of subspecies or variety
            species_parts.append(parts[i])
            i += 1
        else:
            i += 1  # Skip unexpected tokens

    # Assign parsed values to correct taxonomic rank
    row['accepted_species'] = ' '.join(species_parts) if species_parts else None
    row['accepted_subspecies'] = ' '.join(subspecies_parts) if subspecies_parts else None
    row['accepted_variety'] = ' '.join(variety_parts) if variety_parts else None

    return row

# Extract and assign accepted author, taxonkey, and taxon key source at rank level
def assign_accepted_fields(row):
    # Extract accepted_author from the 'accepted' field
    if pd.notnull(row['accepted']):
        # Split the accepted field into parts
        accepted_parts = row['accepted'].rsplit(' ', 1)
        
        # Check if the last part is in parentheses
        if len(accepted_parts) > 1 and accepted_parts[-1].startswith('(') and accepted_parts[-1].endswith(')'):
            row['accepted_author'] = accepted_parts[-1]
        elif len(accepted_parts) > 1:
            row['accepted_author'] = accepted_parts[-1]
        else:
            row['accepted_author'] = None
    else:
        row['accepted_author'] = None

    # Assign accepted_author, accepted_key, and accepted_key_source to the appropriate rank
    if pd.isnull(row['accepted_species']):
        row['accepted_genus_author'] = row['accepted_author']
        row['accepted_genus_taxon_key'] = row['acceptedKey']
        row['accepted_genus_taxon_key_source'] = 'GBIF'
    elif pd.isnull(row['accepted_subspecies']):
        row['accepted_species_author'] = row['accepted_author']
        row['accepted_species_taxon_key'] = row['acceptedKey']
        row['accepted_species_taxon_key_source'] = 'GBIF'
    elif pd.isnull(row['accepted_variety']):
        row['accepted_subspecies_author'] = row['accepted_author']
        row['accepted_subspecies_taxon_key'] = row['acceptedKey']
        row['accepted_subspecies_taxon_key_source'] = 'GBIF'
    else:
        row['accepted_variety_author'] = row['accepted_author']
        row['accepted_variety_taxon_key'] = row['acceptedKey']
        row['accepted_variety_taxon_key_source'] = 'GBIF'

    return row

def create_synonyms(df, output_folder, filename):
    # Filter rows where taxonomicStatus contains 'SYNONYM'
    synonym_rows = df[df['taxonomicStatus'].str.contains('SYNONYM', na=False)]

    # Apply parsing logic for synonyms to the synonyms df
    synonym_rows = synonym_rows.apply(parse_accepted_data, axis=1)

    # Ensure 'accepted_' columns exist
    accepted_columns = [
        'accepted_genus_author', 'accepted_genus_taxon_key', 'accepted_genus_taxon_key_source',
        'accepted_species_author', 'accepted_species_taxon_key', 'accepted_species_taxon_key_source',
        'accepted_subspecies_author', 'accepted_subspecies_taxon_key', 'accepted_subspecies_taxon_key_source', 
        'accepted_variety_author', 'accepted_variety_taxon_key', 'accepted_variety_taxon_key_source'
    ]

    for col in accepted_columns:
        if col not in synonym_rows.columns:
            synonym_rows[col] = None

    # Assign author and key to synonyms
    synonym_rows = synonym_rows.apply(assign_accepted_fields, axis=1)

    # Specify columns to include in the separate synonyms CSV
    columns_to_include = [
        'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'genus_author', 'genus_taxon_key', 'genus_taxon_key_source',
        'species', 'species_author', 'species_taxon_key', 'species_taxon_key_source', 'ishybrid_species',
        'subspecies', 'subspecies_author', 'subspecies_taxon_key', 'subspecies_taxon_key_source', 'ishybrid_subspecies',
        'variety', 'variety_author', 'variety_taxon_key', 'variety_taxon_key_source',
        'accepted_genus', 'accepted_genus_author', 'accepted_genus_taxon_key', 'accepted_genus_taxon_key_source',
        'accepted_species', 'accepted_species_author', 'accepted_species_taxon_key', 'accepted_species_taxon_key_source',
        'accepted_subspecies', 'accepted_subspecies_author', 'accepted_subspecies_taxon_key',
        'accepted_subspecies_taxon_key_source', 'accepted_variety',
        'accepted_variety_author', 'accepted_variety_taxon_key', 'accepted_variety_taxon_key_source'
    ]

    # Only include column if it exists in the above list and the synonym_rows list
    columns_to_include = [col for col in columns_to_include if col in synonym_rows.columns]
    synonym_rows = synonym_rows[columns_to_include]

    # Rename columns to match Sp7ApiToolbox formatting requirements
    synonym_rows.rename(columns={'kingdom': 'Kingdom', 'phylum': 'Phylum', 'class': 'Class', 'order': 'Order', 'family': 'Family',
                                 'genus': 'Genus', 'genus_author': 'GenusAuthor', 'species': 'Species', 'species_author': 'SpeciesAuthor',
                                 'subspecies': 'Subspecies', 'subspecies_author': 'SubspeciesAuthor', 'accepted_genus': 'AcceptedGenus', 
                                 'accepted_genus_author': 'AcceptedGenusAuthor', 'accepted_species': 'AcceptedSpecies', 
                                 'accepted_species_author': 'AcceptedSpeciesAuthor', 'accepted_subspecies': 'AcceptedSubspecies',
                                 'accepted_subspecies_author': 'AcceptedSubspeciesAuthor'}, inplace=True)

    # Add the isAccepted column to the synonym rows
    synonym_rows['isAccepted'] = True
    
    # Create the filename for the synonyms CSV
    synonyms_filename = updated_filename.replace('_processed.tsv', '_synonymsToImport.csv')

    # Convert all numeric columns to integers in the synonyms df
    numeric_columns_synonymns = synonym_rows.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns_synonymns:
        synonym_rows[col] = pd.to_numeric(synonym_rows[col], errors='coerce').fillna(pd.NA).astype(pd.Int64Dtype())

    # Save the synonym rows to a CSV
    output_file_path_synonyms = os.path.join(output_folder, synonyms_filename)
    synonym_rows.to_csv(output_file_path_synonyms, index=False)

def format_digitiser(df):
    # Split the digitiser field based on underscores
    df['digitiser'] = df['digitiser'].fillna('').astype(str)

    for idx, row in df.iterrows():
        name_parts = row['digitiser'].split('_')
        
        if len(name_parts) == 2:
            # If there are two parts, first part is the first name, second part is the last name
            df.at[idx, 'cataloger_firstname'] = name_parts[0]
            df.at[idx, 'cataloger_lastname'] = name_parts[1]
        elif len(name_parts) > 2:
            # If there are more than two parts, first part is the first name, last part is the last name, everything else is the middle name
            df.at[idx, 'cataloger_firstname'] = name_parts[0]
            df.at[idx, 'cataloger_lastname'] = name_parts[-1]
            df.at[idx, 'cataloger_middle'] = '_'.join(name_parts[1:-1])  # Join middle parts if there are any
        else:
            # If the 'digitiser' is empty or does not contain an underscore
            df.at[idx, 'cataloger_firstname'] = 'Birgitte'
            df.at[idx, 'cataloger_lastname'] = 'Bergmann'

    # Add Birgitte to any empty catloger fields
    df['cataloger_firstname'] = df['cataloger_firstname'].fillna('')
    df['cataloger_lastname'] = df['cataloger_lastname'].fillna('')

    df.loc[
        (df['cataloger_firstname'] == '') & (df['cataloger_lastname'] == ''), 
        ['cataloger_firstname', 'cataloger_lastname']
    ] = ['Birgitte', 'Bergmann']

    return df

# Loop through each CSV file in the specified folder_path
for filename in os.listdir(folder_path):
    # Check if the file is a CSV file
    if filename.endswith('.csv'):
        # Read the CSV file with semicolon delimiter
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, delimiter=';')
        
        # Modify the filename to replace 'checked' or 'checked_corrected' with 'processed.tsv'
        updated_filename = re.sub(r'checked(_corrected)?\.csv$', 'processed.tsv', filename)

        # Extract keys from gbif_match_json and convert floats to ints
        df[keys_to_extract] = df.apply(extract_json_data, axis=1)
        # Use 'Int64' dtype to allow for None (null) values
        df['key'] = pd.to_numeric(df['key'], errors='coerce').fillna(pd.NA).astype('Int64') 

        # Add a column with the updated filename
        df['datafile_remark'] = updated_filename
        # Add other pre-filled columns with specified values
        df['projectnumber'] = 'DaSSCo'
        df['publish'] = True
        df['storedunder'] = True
        df['preptypename'] = 'Sheet'
        df['count'] = 1
        df['datafile_source'] = 'DaSSCo data file'
        df['cataloger_firstname'] = None
        df['cataloger_middle'] = None
        df['cataloger_lastname'] = None

        # Convert the 'date_asset_taken' column to datetime and extract the date in 'YYYY-MM-DD' format
        # Assign this value to catalogeddate and datafile_date
        df['catalogeddate'] = pd.to_datetime(df['date_asset_taken']).dt.date.astype(str)
        df['datafile_date'] = df['catalogeddate']

        # Convert the value in digitiser to cataloger first, middle, and last names 
        df = format_digitiser(df)

        # Update the genus and species fields
        df = df.apply(update_genus_and_species, axis=1)
        
        # Replace values in 'authorship' column with NaN if they contain no letters
        df['authorship'] = df['authorship'].apply(
            lambda x: np.nan if isinstance(x, str) and not any(char.isalpha() for char in x) else x
            )
        
        # Move the author & taxon key info to the correct columns
        df = df.apply(process_taxonomic_fields, axis=1)

        # Change any float values to ints in the taxon key fields
        columns_to_check = ['genus_taxon_key', 'species_taxon_key', 'subspecies_taxon_key', 'variety_taxon_key']
        for column in columns_to_check:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce').fillna(pd.NA).astype('Int64')

        # If scientificName contains "var.", copy the word after "var." to new column "variety"
        df['variety'] = df['scientificName'].str.extract(r'\bvar\.\s+(\w+)')

        # If scientificName contains "subsp.", copy the words after "subsp." to new column "subspecies"
        df['subspecies'] = df['scientificName'].apply(extract_subspecies)

        # Add 'ishybrid' column based on whether ' x ' is in the 'species' or 'subspecies' column
        df = df.apply(assign_ishybrid_fields, axis=1)

        # Rename barcode and area columns
        df.rename(columns={'barcode': 'catalognumber', 'area': 'broadgeographicalregion'}, inplace=True)
        df['locality'] = df['broadgeographicalregion']

        create_synonyms(df, output_folder, filename)

        # Desired column order
        desired_columns = [
            'catalognumber', 'catalogeddate', 'cataloger_firstname', 'cataloger_middle', 'cataloger_lastname',
            'projectnumber', 'publish', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'genus_author', 'genus_taxon_key', 'genus_taxon_key_source',
            'species', 'species_author', 'species_taxon_key', 'species_taxon_key_source', 'ishybrid_species',
            'subspecies', 'subspecies_author', 'subspecies_taxon_key', 'subspecies_taxon_key_source', 'ishybrid_subspecies',
            'variety', 'variety_author', 'variety_taxon_key', 'variety_taxon_key_source', 'storedunder', 'locality', 
            'broadgeographicalregion', 'preptypename', 'count'
        ]

        # Ensure all columns in `desired_columns` exist in the DataFrame
        for column in desired_columns:
            if column not in df.columns:
                df[column] = pd.NA

        # Reorder the columns and drop any that are not needed for import to Specify
        df = df[desired_columns]
        df = df[[col for col in desired_columns if col in df.columns]]

        # Convert all numeric columns to integers
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(pd.NA).astype(pd.Int64Dtype())
        
        # Write the df to a new CSV file in the output folder with the updated filename
        output_file_path = os.path.join(output_folder, updated_filename)
        df.to_csv(output_file_path, index=False)
        
        processed_file_path = os.path.join(archive_folder, filename)
        print(f"Moving file to: {processed_file_path}")
        shutil.move(file_path, processed_file_path)

        # Log the processing
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{timestamp} - {filename} processed and moved to {archive_folder}\n")
            log_file.write(f"{timestamp} - {updated_filename} ready for import to Specify\n")