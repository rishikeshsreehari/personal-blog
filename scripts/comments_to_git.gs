
//Use this code in Google App Script to push the code to git as a .json

function pushDataToGitHub() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const rows = sheet.getDataRange().getValues();
  rows.shift(); // Assuming the first row is headers

  // Define the formatDate function within pushDataToGitHub
  function formatDate(date) {
    // Format the date as desired, e.g., "YYYY-MM-DD"
    return Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd");
  }

  // Organizing data by URL
  let dataByUrl = {};
  rows.forEach(row => {
    let [timestamp, url, name, , message] = row;
    url = url.replace(/^\/*|\/*$/g, ''); // Remove leading and trailing slashes
    if (!dataByUrl[url]) {
      dataByUrl[url] = [];
    }
    dataByUrl[url].push({
      "Name": name,
      "Date": formatDate(timestamp),
      "Comment": message
    });
  });

  // Create an object to hold all the JSON data
  let allData = {};

  // Iterate over each URL and add data to the allData object
  for (let url in dataByUrl) {
    allData[url] = dataByUrl[url];
  }

  // Convert the allData object to JSON
  const fileName = `FILE_NAME.json`;
  const fileContent = JSON.stringify(allData, null, 4); // JSON with indentation
  pushToFileInGitHub(fileName, fileContent);
}

function pushToFileInGitHub(fileName, content) {
  const token = 'YOUR_TOKEN'; // Replace with your GitHub personal access token
  const repoOwner = 'USER_NAME'; // Replace with the GitHub user or organization name
  const repoName = 'REPO_NAME'; // Replace with the repository name
  const path = `data/${fileName}`; // Path within the repository
  const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${path}`;

  const fileData = {
    "message": `Updated ${fileName}`,
    "content": Utilities.base64Encode(content)
  };

  // Check if the file exists
  const headers = {
    "Authorization": `token ${token}`,
    "Accept": "application/vnd.github.v3+json"
  };

  const options = {
    "method": "get",
    "headers": headers,
    "muteHttpExceptions": true
  };

  const response = UrlFetchApp.fetch(apiUrl, options);
  if (response.getResponseCode() == 200) {
    // If file exists, get its SHA to update
    const fileSha = JSON.parse(response.getContentText()).sha;
    fileData.sha = fileSha;
  }

  // Push content to GitHub
  options.method = 'put';
  options.payload = JSON.stringify(fileData);

  try {
    UrlFetchApp.fetch(apiUrl, options);
    Logger.log(`Updated file: ${fileName}`);
  } catch (error) {
    Logger.log(`Error updating file: ${fileName}, ${error}`);
  }
}