import os
import sys
import pandas as pd

def create_file_list(directory):
    '''
    inputs: directory path where vcf files are located
    outputs: a list of all .vcf files within the specified directory
    '''
    print(f"Looking for VCF files in: {os.path.abspath(directory)}")
    
    file_list = []
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist!")
        return file_list
        
    for word in os.listdir(directory):
        if word.endswith('.vcf'):
            file_list.append(os.path.join(directory, word))
    
    print(f"Found {len(file_list)} VCF files")
    return file_list

def clean_entry(field):
    g = field.replace('\n', '')
    g = g.replace(';;', ';')
    g = g.replace(';', ' ')
    g = g.replace('=0D=0A=', '')
    return g

def read_vcf(file):
    '''
    inputs: file path with .vcf files
    outputs: a dictionary form of the .vcf file with standardized column names
    '''
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file, 'r', encoding=encoding) as f:
                dt = {
                    'Name Prefix': '', 'First Name': '', 'Middle Name': '', 'Last Name': '',
                    'Name Suffix': '', 'Phonetic First Name': '', 'Phonetic Middle Name': '',
                    'Phonetic Last Name': '', 'Nickname': '', 'File As': '',
                    'E-mail 1 - Label': 'Work', 'E-mail 1 - Value': '',
                    'Phone 1 - Label': '', 'Phone 1 - Value': '',
                    'Address 1 - Label': '', 'Address 1 - Country': '',
                    'Address 1 - Street': '', 'Address 1 - Extended Address': '',
                    'Address 1 - City': '', 'Address 1 - Region': '',
                    'Address 1 - Postal Code': '', 'Address 1 - PO Box': '',
                    'Organization Name': '', 'Organization Title': '',
                    'Organization Department': '', 'Birthday': '',
                    'Event 1 - Label': '', 'Event 1 - Value': '',
                    'Relation 1 - Label': '', 'Relation 1 - Value': '',
                    'Website 1 - Label': '', 'Website 1 - Value': '',
                    'Custom Field 1 - Label': '', 'Custom Field 1 - Value': '',
                    'Notes': '', 'Labels': ''
                }
                
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        if line in ['BEGIN:VCARD', 'END:VCARD']:
                            continue
                            
                        parts = line.split(':', 1)
                        field = parts[0].split(';')[0]
                        
                        if len(parts) == 2:
                            value = clean_entry(parts[1])
                            
                            # Map VCF fields to CSV columns
                            if field == 'N':
                                names = value.split(';')
                                if len(names) >= 1: dt['Last Name'] = names[0].strip()
                                if len(names) >= 2: dt['First Name'] = names[1].strip()
                                if len(names) >= 3: dt['Middle Name'] = names[2].strip()
                                if len(names) >= 4: dt['Name Prefix'] = names[3].strip()
                                if len(names) >= 5: dt['Name Suffix'] = names[4].strip()
                            elif field == 'FN':
                                dt['File As'] = value
                            elif field == 'EMAIL':
                                dt['E-mail 1 - Value'] = value
                            elif field == 'TEL':
                                dt['Phone 1 - Value'] = value
                                dt['Phone 1 - Label'] = 'Work'
                            elif field == 'ADR':
                                addr_parts = value.split(';')
                                if len(addr_parts) >= 1: dt['Address 1 - PO Box'] = addr_parts[0].strip()
                                if len(addr_parts) >= 2: dt['Address 1 - Extended Address'] = addr_parts[1].strip()
                                if len(addr_parts) >= 3: dt['Address 1 - Street'] = addr_parts[2].strip()
                                if len(addr_parts) >= 4: dt['Address 1 - City'] = addr_parts[3].strip()
                                if len(addr_parts) >= 5: dt['Address 1 - Region'] = addr_parts[4].strip()
                                if len(addr_parts) >= 6: dt['Address 1 - Postal Code'] = addr_parts[5].strip()
                                if len(addr_parts) >= 7: dt['Address 1 - Country'] = addr_parts[6].strip()
                            elif field == 'ORG':
                                org_parts = value.split(';')
                                if len(org_parts) >= 1: dt['Organization Name'] = org_parts[0].strip()
                                if len(org_parts) >= 2: dt['Organization Department'] = org_parts[1].strip()
                            elif field == 'TITLE':
                                dt['Organization Title'] = value
                            elif field == 'BDAY':
                                dt['Birthday'] = value
                            elif field == 'NOTE':
                                dt['Notes'] = value
                            elif field == 'NICKNAME':
                                dt['Nickname'] = value
                
                print(f"Successfully read: {os.path.basename(file)}")
                return dt
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {os.path.basename(file)}: {str(e)}")
            continue
    
    print(f"Failed to read {os.path.basename(file)}")
    return {}

def create_df(file_list):
    '''
    inputs: list of files to add to Dataframe
    outputs: dataframe of the vcf files
    '''
    if not file_list:
        print("No VCF files found!")
        return pd.DataFrame()
        
    d_list = []
    for item in file_list:
        contact_data = read_vcf(item)
        if contact_data:  # Only add non-empty dictionaries
            d_list.append(contact_data)
    
    if not d_list:
        print("No data could be extracted from VCF files!")
        return pd.DataFrame()
        
    db = pd.DataFrame(d_list)
    print(f"\nDataFrame created with shape: {db.shape}")
    
    # Ensure columns are in the correct order
    columns = ['Name Prefix', 'First Name', 'Middle Name', 'Last Name', 'Name Suffix',
              'Phonetic First Name', 'Phonetic Middle Name', 'Phonetic Last Name',
              'Nickname', 'File As', 'E-mail 1 - Label', 'E-mail 1 - Value',
              'Phone 1 - Label', 'Phone 1 - Value', 'Address 1 - Label',
              'Address 1 - Country', 'Address 1 - Street', 'Address 1 - Extended Address',
              'Address 1 - City', 'Address 1 - Region', 'Address 1 - Postal Code',
              'Address 1 - PO Box', 'Organization Name', 'Organization Title',
              'Organization Department', 'Birthday', 'Event 1 - Label', 'Event 1 - Value',
              'Relation 1 - Label', 'Relation 1 - Value', 'Website 1 - Label',
              'Website 1 - Value', 'Custom Field 1 - Label', 'Custom Field 1 - Value',
              'Notes', 'Labels']
    
    db = db[columns]
    return db

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <contacts_folder> <output_name>")
        print("Example: python main.py ./CONTACTS output")
        sys.exit(1)
        
    contacts_dir = sys.argv[1]
    output_name = sys.argv[2]
    
    print("\n=== Starting VCF to CSV Conversion ===\n")
    
    file_list = create_file_list(contacts_dir)
    if not file_list:
        print("No VCF files found in the specified directory!")
        sys.exit(1)
        
    df = create_df(file_list)
    
    if df.empty:
        print("\nNo data to save!")
        sys.exit(1)
    else:
        output_file = f"{output_name}.csv"
        df.to_csv(output_file, index=False)
        print(f"\nSuccessfully saved {len(df)} contacts to {output_file}")
        print(f"CSV file contains {len(df.columns)} columns: {df.columns.tolist()}")

if __name__ == "__main__":
    main()