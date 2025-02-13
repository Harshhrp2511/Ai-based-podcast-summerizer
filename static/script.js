document.getElementById("uploadBtn").addEventListener("click", uploadPodcast);
document.getElementById("searchBtn").addEventListener("click", searchPodcast);

function uploadPodcast() {
    let fileInput = document.getElementById("uploadInput");
    let file = fileInput.files[0];
    
    if (!file) {
        alert("Please select a file to upload!");
        return;
    }

    let formData = new FormData();
    formData.append("podcast", file);

    fetch("/upload", { method: "POST", body: formData })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("uploadStatus").innerText = "Error: " + data.error;
        } else {
            document.getElementById("uploadStatus").innerText = 
                "Uploaded: " + data.title + "\nSummary: " + data.summary;
        }
    })
    .catch(error => console.error("Error:", error));
}

function searchPodcast() {
    let query = document.getElementById("searchInput").value;
    if (!query) {
        alert("Enter a search term!");
        return;
    }

    fetch("/search?query=" + encodeURIComponent(query))
    .then(response => response.json())
    .then(data => {
        let resultsList = document.getElementById("results");
        resultsList.innerHTML = "";

        if (data.length === 0) {
            resultsList.innerHTML = "<li>No results found</li>";
        } else {
            data.forEach(item => {
                let listItem = document.createElement("li");
                listItem.innerText = item.title + " - " + item.summary;
                resultsList.appendChild(listItem);
            });
        }
    })
    .catch(error => console.error("Error:", error));
}
