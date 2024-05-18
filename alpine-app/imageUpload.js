function imageUpload() {
    return {
        imageFile: null,
        uploading: false,
        uploadSuccess: false,

        handleFileChange(event) {
            this.imageFile = event.target.files[0];
        },

        async uploadImage() {
            if (!this.imageFile) {
                alert("Please select an image file first.");
                return;
            }

            this.uploading = true;
            this.uploadSuccess = false;

            let formData = new FormData();
            formData.append('image', this.imageFile);

            try {
                let response = await fetch('http://127.0.0.1:5000/upload', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    this.uploadSuccess = true;
                } else {
                    alert("Image upload failed.");
                }
            } catch (error) {
                alert("An error occurred while uploading the image.");
            } finally {
                this.uploading = false;
            }
        }
    }
}