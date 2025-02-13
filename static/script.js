function uploadPodcast() {
    let fileInput = document.getElementById("uploadInput");
    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("podcast", file);

    fetch("/upload", { method: "POST", body: formData })
    .then(response => response.json())
    .then(data => {
        document.getElementById("uploadStatus").innerText = 
            "Uploaded: " + data.title + "\nSummary: " + data.summary;
    })
    .catch(error => console.error("Error:", error));
}

function searchPodcast() {
    let query = document.getElementById("searchInput").value;

    fetch("/search?query=" + query)
    .then(response => response.json())
    .then(data => {
        let resultsList = document.getElementById("results");
        resultsList.innerHTML = "";

        data.forEach(item => {
            let listItem = document.createElement("li");
            listItem.innerText = item.title + " - " + item.summary;
            resultsList.appendChild(listItem);
        });
    })
    .catch(error => console.error("Error:", error));
}
