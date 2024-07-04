//Add this code in Google Sheet App Script
//You have to add a trigger to run this code everyday or at intervals as required using the convertSheetToJson() function



function convertSheetToJson() {
  // Get the active sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Dashboard");
  
  // Get the data range
  var range = sheet.getDataRange();
  
  // Get the data values
  var values = range.getValues();
  
  // Get the headers
  var headers = values[0];
  
  // Initialize an empty array to store the JSON data
  var jsonData = [];
  
  // Loop through the rows of data and create JSON objects
  for (var i = 1; i < values.length; i++) {
    var obj = {};
    for (var j = 0; j < headers.length; j++) {
      obj[headers[j]] = values[i][j];
    }
    jsonData.push(obj);
  }

  // Add Updated item with current datetime value
  jsonData.push({Updated: new Date().toLocaleString()});
  
  // Convert the JSON data to a string
  var jsonString = JSON.stringify(jsonData, null, 2);
  
  // Get the folder where the JSON file will be stored
  var folder = DriveApp.getFolderById("YOUR_FOLDER_ID");
  
  // Check if the file already exists in the folder
  var files = folder.getFilesByName("my_data.json");
  if (files.hasNext()) {
    var file = files.next();
    // Delete the existing file
    file.setTrashed(true);
  }

  // Create the JSON file with the data
  folder.createFile("my_data.json", jsonString, 'application/json');

  // Update the JSON file on GitHub
  var token = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN";
  var repoOwner = "YOUR_GITHUB_USERNAME";
  var repoName = "YOUR_REPO_NAME";
  var filePath = "path/to/your/file.json";
  var commitMessage = "Automated daily update of my_data.json";
  updateGitHub(token, repoOwner, repoName, filePath, commitMessage, jsonString);
}

function updateGitHub(token, repoOwner, repoName, filePath, commitMessage, fileContent) {
  var url = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${filePath}`;
  var headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/vnd.github.v3+json"
  };

  // Get the current file's SHA
  var getResponse = UrlFetchApp.fetch(url, {
    "method": "GET",
    "headers": headers
  });
  var fileInfo = JSON.parse(getResponse.getContentText());
  var sha = fileInfo.sha;

  // Prepare the update payload
  var payload = {
    "message": commitMessage,
    "content": Utilities.base64Encode(fileContent),
    "sha": sha,
    "committer": {
      "name": "AutomationBot",
      "email": "bot@example.com"
    }
  };

  // Update the file
  var updateResponse = UrlFetchApp.fetch(url, {
    "method": "PUT",
    "headers": headers,
    "payload": JSON.stringify(payload)
  });

  var result = JSON.parse(updateResponse.getContentText());
  if (updateResponse.getResponseCode() != 200) {
    throw new Error("Error updating GitHub file: " + result.message);
  }
}