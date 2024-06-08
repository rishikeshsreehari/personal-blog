import yaml
import svgwrite
import os
import plotly.graph_objs as go
import plotly.io as pio

# Load the books YAML file with UTF-8 encoding
with open("data/books.yaml", "r", encoding='utf-8') as f:
    books = yaml.safe_load(f)

# Initialize a dictionary to store the book count for each year
book_counts = {}

# Loop through each book and count the books read in each year
for book in books:
    year = book["date"].year
    if year in book_counts:
        book_counts[year] += 1
    else:
        book_counts[year] = 1

# Sort the book counts by year
book_counts = dict(sorted(book_counts.items()))

# SVG chart creation
width = 580
height = 230
chart_width = 580
chart_height = 200
chart_margin = 10
bar_color = "#0072B2"
max_value = max(book_counts.values())
bar_heights = {year: (count / float(max_value)) * chart_height for year, count in book_counts.items()}

if not os.path.exists("static/images"):
    os.makedirs("static/images")

dwg = svgwrite.Drawing("static/images/books_read_per_year.svg", size=(width, height))
chart_area = dwg.rect((chart_margin, chart_margin), (chart_width, chart_height), stroke="#1D1E20", fill="#1D1E20")
dwg.add(chart_area)

for i, (year, count) in enumerate(book_counts.items()):
    x = chart_margin + (i * (chart_width / len(book_counts)))
    y = chart_margin + chart_height - bar_heights[year]
    height = bar_heights[year]
    bar = dwg.rect((x, y), ((chart_width / len(book_counts)) - 10, height), fill=bar_color)
    dwg.add(bar)
    label_x = x + ((chart_width / len(book_counts)) - 10) / 2
    label_y = y - 5
    label = dwg.text(str(count) + ' books', insert=(label_x, label_y), fill="#FFFFFF", font_size="14px", font_family="sans-serif", text_anchor="middle", alignment_baseline="central")
    dwg.add(label)

for i, year in enumerate(book_counts.keys()):
    x = chart_margin + (i * (chart_width / len(book_counts))) + ((chart_width / len(book_counts)) / 2) - 10
    y = chart_margin + chart_height + 20
    label = dwg.text(year, insert=(x, y), fill="#BAC4C5", font_size="14px", font_family="sans-serif", text_anchor="middle")
    dwg.add(label)

dwg.save()

