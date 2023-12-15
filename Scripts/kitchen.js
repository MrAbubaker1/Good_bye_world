function previewImage(event) {
    var reader = new FileReader();
    var imagePreview = document.getElementById('imagePreview');
    var imageCancel = document.getElementById('cancel');

    reader.onload = function () {
        imagePreview.src = reader.result;
    imagePreview.style.display = 'block'; // Display the image after a file is selected
    imageCancel.style.display = 'block' ;
    };

    reader.readAsDataURL(event.target.files[0]);
}

function cancelPreview() {
    var uploadInput = document.getElementById('uploadInput');
    var imagePreview = document.getElementById('imagePreview');
    var imageCancel = document.getElementById('cancel');

    uploadInput.value = ''; // Clear the file input
    imagePreview.style.display = 'none'; // Hide the image
    imageCancel.style.display = 'none' ;
}