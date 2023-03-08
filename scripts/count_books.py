import yaml
import matplotlib.pyplot as plt
matplotlib.use('Agg')



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

    # Generate a bar plot of the book counts
    plt.bar(book_counts.keys(), book_counts.values())
    plt.title("Books Read Per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Books Read")
    plt.savefig("static/images/books_read_per_year.png")

    print("Python script executed successfully")
    print("Running count_books.py script...")


if __name__ == "__main__":
    main()