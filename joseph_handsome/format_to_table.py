def csv_to_html_table(csv_lines):
    # Split the first line to get headers
    headers = csv_lines[0].split(',')
    
    # Start the HTML table
    html = '<table>\n'
    
    # Create the table header
    html += '  <thead>\n    <tr>\n'
    for header in headers:
        html += f'      <th>{header.strip()}</th>\n'
    html += '    </tr>\n  </thead>\n'
    
    # Create the table body
    html += '  <tbody>\n'
    for line in csv_lines[1:]:
        values = line.split(',')
        html += '    <tr>\n'
        for value in values:
            html += f'      <td>{value.strip()}</td>\n'
        html += '    </tr>\n'
    html += '  </tbody>\n</table>'
    
    return html

# Example usage:
csv_data = [
    "name, age, height (in feet)",
    "joe, 18, 5.8",
    "ella, 16, 3.3"
]

html_table = csv_to_html_table(csv_data)
print(html_table)
