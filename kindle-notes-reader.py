import re
import os

def process_highlights(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    # Split the input text on the delimiter
    highlights = text.strip().split("==========")

    # Define a dictionary to store quotes by book title
    book_quotes = {}

    # Regex to extract page number and date
    page_date_pattern = re.compile(r"page (\d+).*?Added on (.*)")

    for highlight in highlights:
        if highlight.strip():  # Check if highlight is not empty
            lines = highlight.strip().split('\n')

            # Extract the title and author from the first line
            title_author_line = lines[0].strip()
            title_author_parts = title_author_line.split(' (')
            title = title_author_parts[0].strip()
            author = title_author_parts[1].strip(')') if len(title_author_parts) > 1 else "Unknown Author"

            # Extract page number and date
            page_date_match = page_date_pattern.search(highlight)
            if page_date_match:
                page = page_date_match.group(1).strip()
                date = page_date_match.group(2).strip()

                # Extract the quote
                quote_parts = lines[3:]  # Skip the metadata lines
                quote = ' '.join(part.strip() for part in quote_parts if part.strip())

                # Format the quote with page number and date
                formatted_quote = "Page {} | Added on {}\n{}".format(page, date, quote)

                # Construct the title-author key
                title_author_key = "{} ({})".format(title, author)

                # Add the formatted quote to the dictionary under the appropriate title-author key
                if title_author_key in book_quotes:
                    book_quotes[title_author_key].append(formatted_quote)
                else:
                    book_quotes[title_author_key] = [formatted_quote]

    # Save quotes to files by book title-author key
    if not os.path.exists('output'):
        os.makedirs('output')

    for title_author_key in sorted(book_quotes):
        file_name = "{}.txt".format(title_author_key.replace('/', '_').replace('\\', '_').replace(':', '_'))
        file_path = os.path.join('output', file_name)
        with open(file_path, 'w') as file:
            for quote in book_quotes[title_author_key]:
                file.write(quote + "\n\n")
        print("Quotes for '{}' have been saved to '{}'".format(title_author_key, file_path))

# Path to the input file
file_path = 'My Clippings.txt'

# Call the function with the file path
process_highlights(file_path)
