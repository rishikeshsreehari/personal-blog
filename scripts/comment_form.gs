
//Add this code in Google Sheet App Script to collect comments to sheet.


var sheetName = 'Sheet1';
var scriptProp = PropertiesService.getScriptProperties();

function intialSetup() {
  var activeSpreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  scriptProp.setProperty('key', activeSpreadsheet.getId());
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  try {
    // Check the honeypot field
    var honeypotValue = e.parameter['honeypot'];
    if (honeypotValue && honeypotValue !== '') {
      // The honeypot field is filled; treat it as spam
      return ContentService
        .createTextOutput('Error: Spam submission detected.')
        .setMimeType(ContentService.MimeType.TEXT);
    }

    var doc = SpreadsheetApp.openById(scriptProp.getProperty('key'));
    var sheet = doc.getSheetByName(sheetName);
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    var nextRow = sheet.getLastRow() + 1;
    var newRow = headers.map(function (header) {
      return header === 'timestamp' ? new Date() : e.parameter[header];
    });
    sheet.getRange(nextRow, 1, 1, newRow.length).setValues([newRow]);

    // Return a simple text success message
    return ContentService
      .createTextOutput('Thank you for your comment! After moderation, the comment will appear on the website. Feel free to return to the content by clicking the back button.')
      .setMimeType(ContentService.MimeType.TEXT);
  } catch (e) {
    // Return an error message
    return ContentService
      .createTextOutput('Error submitting comment: ' + e)
      .setMimeType(ContentService.MimeType.TEXT);
  } finally {
    lock.releaseLock();
  }
}
