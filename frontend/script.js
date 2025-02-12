function uploadPodcast() {
    let fileInput = document.getElementById('podcastUpload');
    if (fileInput.files.length === 0) {
        alert('Please upload a podcast file!');
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("podcast", file);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert("Podcast uploaded successfully! AI is generating the summary...");
        displaySummary(data);
    })
    .catch(error => console.error('Error:', error));
}

function displaySummary(data) {
    let resultsContainer = document.getElementById('results-container');
    let newSummary = document.createElement('div');
    newSummary.classList.add('result');
    newSummary.innerHTML = `<strong>${data.title}</strong><br>${data.summary}`;
    resultsContainer.appendChild(newSummary);
}

function searchSummaries() {
    let query = document.getElementById('searchInput').value.toLowerCase();
    let summaries = document.getElementsByClassName('result');

    for (let summary of summaries) {
        if (summary.innerHTML.toLowerCase().includes(query)) {
            summary.style.display = "block";
        } else {
            summary.style.display = "none";
        }
    }
}
