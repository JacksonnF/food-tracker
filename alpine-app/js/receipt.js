function groceryManager() {
    return {
        imageFile: null,
        showForm: false,
        loading: false,
        items: [],

        handleFileChange(event) {
            this.imageFile = event.target.files[0];
        },

        async uploadReceipt() {
            if (!this.imageFile) {
                alert("Please select an image file first.");
                return;
            }

            this.loading = true;

            let formData = new FormData();
            formData.append('receipt', this.imageFile);

            try {
                let response = await fetch('http://127.0.0.1:5000/upload', {
                    method: 'POST',
                    body: formData
                });
                let jsonResponse = await response.json();
                this.loading = false;
                if (response.ok) {
                    console.log(jsonResponse);
                    this.items = jsonResponse;
                    alert("Receipt uploaded successfully!");
                } else {
                    alert("Receipt upload failed.");
                }
            } catch (error) {
                this.loading = false;
                alert("An error occurred while uploading the receipt.");
            }
        },

        removeItem(index) {
            this.items.splice(index, 1);
        },

        async submitUpdatedItems() {
            try {
                let response = await fetch('http://127.0.0.1:5000/updatedb', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.items)
                });
                if (response.ok) {
                    alert("Items updated successfully!");
                } else {
                    alert("Failed to update items.");
                }
            } catch (error) {
                alert("An error occurred while updating items.");
            }
        }
    }
}