import yaml
import matplotlib.pyplot as plt


def main():
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

    # Create a bar chart of the book counts
    fig, ax = plt.subplots()
    ax.bar(book_counts.keys(), book_counts.values())
    ax.set_title("Books Read Per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Books Read")
    fig.savefig("static/images/books_read_per_year.png")

    print("Python script executed successfully")
    print("Running count_books.py script...")


if __name__ == "__main__":
    main()
