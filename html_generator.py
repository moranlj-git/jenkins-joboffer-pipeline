import csv
import os

def generate_html_table(csv_filepath, html_filepath):
    """Generates an HTML table from a CSV file."""

    try:
        with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            rows = list(reader) # Read all rows into a list

        with open(html_filepath, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write('<!DOCTYPE html>')
            htmlfile.write('<html lang="en">')
            htmlfile.write('<head>')
            htmlfile.write('    <meta charset="UTF8">')
            htmlfile.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
            htmlfile.write('    <title>Job Listings</title>')
            # Minimal CSS for responsive table
            htmlfile.write('    <style>')
            htmlfile.write('        table {')
            htmlfile.write('            border-collapse: collapse;')
            htmlfile.write('            width: 100%;')
            htmlfile.write('        }')
            htmlfile.write('        th, td {')
            htmlfile.write('            border: 1px solid black;')
            htmlfile.write('            padding: 8px;')
            htmlfile.write('            text-align: left;')
            htmlfile.write('        }')
            htmlfile.write('        th {')
            htmlfile.write('            background-color: #f2f2f2;')
            htmlfile.write('        }')
            htmlfile.write('        /* Responsive table */')
            htmlfile.write('        @media screen and (max-width: 600px) {')
            htmlfile.write('            table, thead, tbody, th, td, tr {')
            htmlfile.write('                display: block;')
            htmlfile.write('            }')
            htmlfile.write('            thead tr {')
            htmlfile.write('                position: absolute;')
            htmlfile.write('                top: -9999px;')
            htmlfile.write('                left: -9999px;')
            htmlfile.write('            }')
            htmlfile.write('            tr {')
            htmlfile.write('                border: 1px solid black;')
            htmlfile.write('            }')
            htmlfile.write('            td {')
            htmlfile.write('                border: none;')
            htmlfile.write('                border-bottom: 1px solid black;')
            htmlfile.write('                position: relative;')
            htmlfile.write('                padding-left: 50%;')
            htmlfile.write('            }')
            htmlfile.write('            td:before {')
            htmlfile.write('                position: absolute;')
            htmlfile.write('                top: 6px;')
            htmlfile.write('                left: 6px;')
            htmlfile.write('                width: 45%;')
            htmlfile.write('                padding-right: 10px;')
            htmlfile.write('                white-space: nowrap;')
            htmlfile.write('                content: attr(data-label);')
            htmlfile.write('                text-align: left;')
            htmlfile.write('                font-weight: bold;')
            htmlfile.write('            }')
            htmlfile.write('        }')
            htmlfile.write('    </style>')
            htmlfile.write('</head>')
            htmlfile.write('<body>')
            htmlfile.write('    <h1>Job Listings</h1>')
            htmlfile.write('    <table>')
            htmlfile.write('        <thead>')
            htmlfile.write('            <tr>')
            for field in fieldnames:                htmlfile.write(f'                <th>{field}</th>')
            htmlfile.write('            </tr>')
            htmlfile.write('        </thead>')
            htmlfile.write('        <tbody>')
            for row in rows:
                htmlfile.write('            <tr>')
                for field in fieldnames:
                    value = row[field]
                    if field == 'Lien':
                        htmlfile.write(f'                <td data-label="{field}"><a href="{value}">{value}</a></td>')
                    else:
                        htmlfile.write(f'                <td data-label="{field}">{value}</td>')
                htmlfile.write('            </tr>')
            htmlfile.write('        </tbody>')
            htmlfile.write('    </table>')
            htmlfile.write('</body>')
            htmlfile.write('</html>')

    except FileNotFoundError:
        print(f"Error: The file {csv_filepath} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    csv_file = 'data/jobs.csv'
    html_file = 'public/index.html'

    # Create the 'public' directory if it doesn't exist
    if not os.path.exists('public'):
        os.makedirs('public')

    generate_html_table(csv_file, html_file)
    print(f"HTML table generated successfully at {html_file}")
