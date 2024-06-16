document.addEventListener('DOMContentLoaded', () => {
    const initialDisplayCount = 20;
    let displayedCount = initialDisplayCount;
    const books = document.querySelectorAll('.book');
    const showMoreButton = document.getElementById('show-more');
  
    // Hide all books initially
    books.forEach((book, index) => {
      if (index >= initialDisplayCount) {
        book.style.display = 'none';
      }
    });
  
    // Show more books on button click
    window.showMoreBooks = function () {
      const nextCount = displayedCount + initialDisplayCount;
      books.forEach((book, index) => {
        if (index < nextCount) {
          book.style.display = 'block';
        }
      });
      displayedCount = nextCount;
  
      // Hide the button if all books are displayed
      if (displayedCount >= books.length) {
        showMoreButton.style.display = 'none';
      }
    };
  });
  