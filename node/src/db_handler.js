const fs = require("fs");

function loadJsonFile(filePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        console.error("Error reading the file:", err);
        reject(err); // Reject the promise on error
      } else {
        try {
          const jsonObj = JSON.parse(data);
          resolve(jsonObj); // Resolve the promise with the JSON object
        } catch (parseError) {
          console.error("Error parsing JSON:", parseError);
          reject(parseError); // Reject the promise on parsing error
        }
      }
    });
  });
}

module.exports = { loadJsonFile };
