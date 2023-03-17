
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
  var folder = DriveApp.getFolderById("FOLDER_ID"); // Replace "FOLDER_ID" with the ID of the folder
  
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
  var fileId = "FILE_ID";
  var token = "TOKEN"; 
  var repoName = "rishikeshsreehari/personal-blog"; //Repository Name
  var filePath = "data/my_data.json"; //Path to your JSON file
  var commitMessage = "Automated daily updation of my_data.json"; // Commit message to be displayed on GitHub
  updateGitHub(fileId, token, repoName, filePath, commitMessage, jsonString);

  function updateGitHub(fileId, token, repoName, filePath, commitMessage, fileContent) {
    var url = "https://api.github.com/repos/" + repoName + "/contents/" + filePath;
    var sha = getFileSha(url, token);
  
    var params = {
      method: "PUT",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json"
      },
     payload: JSON.stringify({
    message: commitMessage,
    content: Utilities.base64Encode(fileContent),
    sha: sha,
    })
  
    };
    var response = UrlFetchApp.fetch(url, params);
    var result = JSON.parse(response.getContentText());
    if (result.message == "Bad credentials") {
      throw new Error("Invalid GitHub token");
    } else if (response.getResponseCode() != 200) {
      throw new Error("Error updating GitHub file: " + result.message);
    }
    
    function getFileSha(url, token) {
      var params = {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json"
        }
      };
      var response = UrlFetchApp.fetch(url, params);
      var result = JSON.parse(response.getContentText());
      return result.sha;
    }
    
  }

}





















