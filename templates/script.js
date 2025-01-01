document.getElementById('dropZone').addEventListener('click', () => {
    document.getElementById('fileInput').click();
});

document.getElementById('urlSubmit').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value.trim();
    if (url) {
        document.getElementById('hiddenUrlInput').value = url;
        document.getElementById('uploadForm').submit();
    } else {
        alert('Please enter a valid URL.');
    }
});
