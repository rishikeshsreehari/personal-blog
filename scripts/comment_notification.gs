
//Use this code in Google App Script to get notifications on email. Trigger needs to be set!

function checkForNewComments() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();
  const lastCheck = PropertiesService.getScriptProperties().getProperty('lastCheckedRow');

  if (lastRow > lastCheck) {
    // New comments have been added
    sendNotification(lastRow - lastCheck); // Send notification for new comments
    PropertiesService.getScriptProperties().setProperty('lastCheckedRow', lastRow);
  }
}

function sendNotification(newCommentsCount) {
  // Send an email notification or any other type of notification
  const email = 'EMAIL'; // Replace with your email
  const subject = 'New Comment on Blog';
  const body = `${newCommentsCount} new comments have been added. Check and approve:URL`;
  MailApp.sendEmail(email, subject, body);
}