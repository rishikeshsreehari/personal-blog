// Get the table element
var table = document.querySelector('.sortable');

// Initialize SortableJS on the table
var sortable = new Sortable(table, {
  // Define the sorting behavior for the "Rating" column
  sort: true,
  onSort: function (evt) {
    // Get the index of the "Rating" column
    var ratingIndex = Array.prototype.indexOf.call(table.tHead.rows[0].cells, evt.detail.handle);

    // Sort the rows based on the rating column
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    rows.sort(function (a, b) {
      var aRating = a.cells[ratingIndex].innerText;
      var bRating = b.cells[ratingIndex].innerText;
      if (aRating > bRating) return -1;
      if (aRating < bRating) return 1;
      return 0;
    });

    // Reorder the rows in the table
    for (var i = 0; i < rows.length; i++) {
      table.tBodies[0].appendChild(rows[i]);
    }
  }
});
