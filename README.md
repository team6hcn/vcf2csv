# VCF to CSV Converter

A Python script that converts VCF (vCard) contact files to a CSV format compatible with common contact management systems.

## Description

This script takes a directory containing VCF files and converts them into a single CSV file with standardized columns. It's particularly useful for:
- Migrating contacts between different systems
- Creating backups of contact lists
- Converting Outlook/vCard contacts to spreadsheet format

## Features

- Handles multiple VCF files in a directory
- Supports different character encodings (UTF-8, Latin-1, ISO-8859-1, CP1252)
- Extracts common contact fields:
  - Names (First, Middle, Last, Prefix, Suffix)
  - Email addresses
  - Phone numbers
  - Addresses
  - Organization details
  - And more...
- Outputs a standardized CSV format

## Requirements

- Python 3.x
- pandas
- vobject

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with the directory path and output filename as arguments:
```bash
python main.py <directory_path> <output_filename>
```

Example:
```bash
python main.py ./contacts.vcf contacts.csv
```

This will create a CSV file named `contacts.csv` in the current directory.

This will:
1. Read all .vcf files from the CONTACTS directory
2. Convert them to CSV format
3. Save the result as "output.csv"

## Output Format

The CSV file includes the following columns:
- Name (Prefix, First, Middle, Last, Suffix)
- Email
- Phone
- Address (Street, City, Region, Postal Code, Country)
- Organization (Name, Title, Department)
- And other standard contact fields

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Team 6 HCN

## Acknowledgments

- Thanks to all contributors


