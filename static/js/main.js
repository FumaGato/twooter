function showFileName(input) {
    const fileNameSpan = document.getElementById('fileName');
    const clearButton = document.getElementById('clearButtonLabel');
    if (input.files && input.files.length > 0) {
        fileNameSpan.textContent = input.files[0].name;
        clearButton.textContent = 'Clear';
    } else {
        fileNameSpan.textContent = '';
        clearButton.textContent = '';
    }
}

function clearSelection() {
    const fileInput = document.getElementById('image');
    const fileNameSpan = document.getElementById('fileName');
    const clearButton = document.getElementById('clearButtonLabel');
    fileInput.value = '';
    fileNameSpan.textContent = '';
    clearButton.textContent = '';
}

function resizeImg(img) {
    if (img.style.width == '50%') {
        img.style.width = '100%';
    } else {
        img.style.width = '50%';
    }
}

function deleteTwoot(id) {
    fetch(`delete/${id}`, {
        method: 'DELETE'
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const row = document.getElementById(`twoot${id}`)
                row.remove()
            }
        })
}