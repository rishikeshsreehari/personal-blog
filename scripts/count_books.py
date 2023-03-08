import yaml
import svgwrite

import os



# Load the books YAML file
with open("data/books.yaml", "r") as f:
    books = yaml.safe_load(f)

# Initialize a dictionary to store the book count for each year
book_counts = {}

# Loop through each book and count the books read in each year
for book in books:
    rating = int(book["rating"])
    date_str = book["date"].strftime("%Y-%m-%d")
    year = book["date"].year
    month = book["date"].month
    if year in book_counts:
        book_counts[year] += 1
    else:
        book_counts[year] = 1

# Sort the book counts by year
book_counts = dict(sorted(book_counts.items()))

# Set the size of the SVG image
width = 600
height = 400

# Set the size and margin of the chart area
chart_width = 500
chart_height = 300
chart_margin = 50

# Set the color of the bars
bar_color = "#0072B2"

# Calculate the maximum value of the data
max_value = max(book_counts.values())

# Calculate the height of each bar
bar_heights = {year: (count / float(max_value)) * chart_height for year, count in book_counts.items()}

if not os.path.exists("static/images"):
    os.makedirs("static/images")

# Create the SVG drawing
dwg = svgwrite.Drawing("static/images/books_read_per_year.svg", size=(width, height))

# Create the chart area
chart_area = dwg.rect((chart_margin, chart_margin), (chart_width, chart_height), stroke="black", fill="white")
dwg.add(chart_area)

# Create the bars
for i, (year, count) in enumerate(book_counts.items()):
    x = chart_margin + (i * (chart_width / len(book_counts)))
    y = chart_margin + chart_height - bar_heights[year]
    height = bar_heights[year]
    bar = dwg.rect((x, y), ((chart_width / len(book_counts)) - 10, height), fill=bar_color)
    dwg.add(bar)

# Add the x-axis labels
for i, year in enumerate(book_counts.keys()):
    x = chart_margin + (i * (chart_width / len(book_counts))) + ((chart_width / len(book_counts)) / 2) - 10
    y = chart_margin + chart_height + 20
    label = dwg.text(year, insert=(x, y), fill="black", font_size="14px", font_family="sans-serif", text_anchor="middle")
    dwg.add(label)

# Add the y-axis label
label = dwg.text("Number of Books Read", insert=(chart_margin - 40, chart_margin + (chart_height / 2)), fill="black", font_size="14px", font_family="sans-serif", text_anchor="middle", transform="rotate(-90, {0}, {1})".format(chart_margin - 40, chart_margin + (chart_height / 2)))
dwg.add(label)

# Add the chart title
title = dwg.text("Books Read Per Year", insert=(width / 2, chart_margin - 10), fill="black", font_size="24px", font_family="sans-serif", text_anchor="middle")
dwg.add(title)

# Save the SVG image
dwg.save()
