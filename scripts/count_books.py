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
width = 580
height = 230

# Set the size and margin of the chart area
chart_width = 580
chart_height = 200
chart_margin = 10

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
chart_area = dwg.rect((chart_margin, chart_margin), (chart_width, chart_height), stroke="#1D1E20", fill="#1D1E20")
dwg.add(chart_area)

# Create the bars
for i, (year, count) in enumerate(book_counts.items()):
    x = chart_margin + (i * (chart_width / len(book_counts)))
    y = chart_margin + chart_height - bar_heights[year]
    height = bar_heights[year]
    bar = dwg.rect((x, y), ((chart_width / len(book_counts)) - 10, height), fill=bar_color)
    dwg.add(bar)
    label_x = x + ((chart_width / len(book_counts)) - 10) / 2
    label_y = y - 5
    label = dwg.text(str(count) + ' books', insert=(x + ((chart_width / len(book_counts)) - 10) / 2, y + height / 2), fill="#FFFFFF", font_size="14px", font_family="sans-serif", text_anchor="middle", alignment_baseline="central")
    dwg.add(label)

# Add the x-axis labels
for i, year in enumerate(book_counts.keys()):
    x = chart_margin + (i * (chart_width / len(book_counts))) + ((chart_width / len(book_counts)) / 2) - 10
    y = chart_margin + chart_height + 20
    label = dwg.text(year, insert=(x, y), fill="#BAC4C5", font_size="14px", font_family="sans-serif", text_anchor="middle")
    dwg.add(label)

# Add the y-axis label
#label = dwg.text("Number of Books Read", insert=(chart_margin - 40, chart_margin + (chart_height / 2)), fill="#FFFFFF", font_size="14px", font_family="sans-serif", text_anchor="middle", transform="rotate(-90, {0}, {1})".format(chart_margin - 40, chart_margin + (chart_height / 2)))
#dwg.add(label)

# Add the chart title
#title = dwg.text("Books Read Per Year", insert=(width / 2, chart_margin - 10), fill="black", font_size="24px", font_family="sans-serif", text_anchor="middle")
#dwg.add(title)

# Save the SVG image
dwg.save()

import plotly.graph_objs as go
import plotly.io as pio
import numpy as np

fig = go.Figure(
    layout=go.Layout(
        title="Random Graph Title",
        xaxis=dict(title="X-axis"),
        yaxis=dict(title="Y-axis")
    )
)

# Export the graph as a PNG file
pio.write_image(fig, 'static/images/random_graph.png', width=800, height=600)



