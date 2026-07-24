function getCsrfToken() {
    var cookie = document.cookie.split(';').find(function (c) {
        return c.trim().startsWith('csrftoken=');
    });
    return cookie ? cookie.trim().split('=')[1] : '';
}

document.addEventListener('DOMContentLoaded', function () {
    var textarea = document.getElementById('id_content');
    if (!textarea) return;

    var easyMDE = new EasyMDE({
        element: textarea,
        spellChecker: false,
        autosave: {
            enabled: true,
            uniqueId: 'post_content_autosave',
            delay: 2000,
        },
        toolbar: [
            'bold', 'italic', 'heading', '|',
            'quote', 'unordered-list', 'ordered-list', '|',
            'link', 'upload-image', 'table', '|',
            'code', 'horizontal-rule', '|',
            'preview', 'side-by-side', 'fullscreen', '|',
            'guide'
        ],
        uploadImage: true,
        imageUploadFunction: function (file, onSuccess, onError) {
            var allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
            if (!allowed.includes(file.type)) {
                onError('Tipo no permitido. Usa JPG, PNG, GIF o WebP.');
                return;
            }
            if (file.size > 5 * 1024 * 1024) {
                onError('La imagen no puede superar los 5 MB.');
                return;
            }

            var formData = new FormData();
            formData.append('image', file);

            fetch('/upload-imagen/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData,
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.url) {
                        onSuccess(data.url);
                    } else {
                        onError(data.error || 'Error al subir la imagen.');
                    }
                })
                .catch(function () {
                    onError('Error de red al subir la imagen.');
                });
        },
        imageTexts: {
            sbInit: 'Adjunta imágenes arrastrando o haciendo clic aquí.',
            sbOnDragEnter: 'Suelta la imagen para subirla.',
            sbOnDrop: 'Subiendo imagen #images_names#...',
            sbProgress: 'Subiendo #file_name#: #progress#%',
            sbOnUploaded: '¡Imagen subida!',
        },
        errorMessages: {
            noFileGiven: 'Debes seleccionar una imagen.',
            typeNotAllowed: 'Tipo de archivo no permitido.',
            fileTooLarge: 'La imagen supera los 5 MB.',
            importError: 'Error al importar la imagen: #error_message#',
        },
        renderingConfig: {
            singleLineBreaks: false,
            codeSyntaxHighlighting: true,
        },
        previewRender: function (plainText, preview) {
            setTimeout(function () {
                if (window.MathJax && MathJax.typesetPromise) {
                    MathJax.typesetPromise([preview]);
                }
            }, 100);
            return this.parent.markdown(plainText);
        },
        minHeight: '400px',
        sideBySideFullscreen: false,
    });
});
