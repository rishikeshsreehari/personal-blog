document.addEventListener('DOMContentLoaded', function() {
  const initialDisplayCount = INITIAL_DISPLAY_COUNT;
  let displayedCount = initialDisplayCount;
  const books = document.querySelectorAll('.book');
  const showMoreButton = document.getElementById('show-more');
  
  // Hide all books initially
  books.forEach(function(book, index) {
    if (index >= initialDisplayCount) {
      book.style.display = 'none';
    }
  });

  // Define the function to show more books
  window.showMoreBooks = function() {
    const nextCount = displayedCount + initialDisplayCount;
    books.forEach(function(book, index) {
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
