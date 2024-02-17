document.querySelector('#upload img.inner').addEventListener('click', function() {
    document.querySelector('#file-upload').click();
});

document.addEventListener('DOMContentLoaded', function() {
    showLoadingOverlay();
    fetch('/loadmodel', {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Model loaded successfully');
        hideLoadingOverlay();
    })
    .catch(error => {
        console.error('Error loading model:', error);
    });
});

function handleFileUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
  
    reader.onload = function() {
      showLoadingOverlay();
      uploadFile(file);
    }

    reader.readAsDataURL(file);
  }
  
  function showLoadingOverlay() {
    document.querySelector('img.inner').classList.add('d-none');
    document.querySelector('.loading-overlay').classList.remove('d-none');
  }
  
  function hideLoadingOverlay() {
    document.querySelector('img.inner').classList.remove('d-none');
    document.querySelector('.loading-overlay').classList.add('d-none');
  }

  function showResults() {
    document.querySelector('#generation').classList.remove('d-none');
  }
  function hideResults() {
    document.querySelector('#generation').classList.add('d-none');
  }

  function downloadImage() {
    const link = document.createElement('a');
    link.href = document.querySelector('#generation-result').getAttribute('src');
    link.setAttribute(
        'download',
        `GeneratedRetina.png`,
    );
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  }
  
  function uploadFile(file) {
    hideResults();
    const formData = new FormData();
    formData.append('file', file);
  
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        let sourceImgURL = URL.createObjectURL(file);
        const input = document.querySelector('#generation-input');
        input.src = sourceImgURL;
        const imageUrl = URL.createObjectURL(blob);
        const result = document.querySelector('#generation-result');
        result.src = imageUrl;
        hideLoadingOverlay();
        showResults();
    })
    .catch(error => {
      console.error('Error:', error);
      hideLoadingOverlay();
    });
  }