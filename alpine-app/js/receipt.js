function groceryManager() {
    return {
        imageFile: null,
        showForm: false,
        loading: false,
        items: [],

        init() {
            const token = localStorage.getItem('token');
            if (!token) {
                console.error("No Token Found, Please Login");
                window.location.href = urls.login;
                return;
            }
        },

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
                const token = localStorage.getItem('token');
                if (!token) {
                    console.error("No Token Found, Please Login");
                    alert("Not Logged In");
                    return;
                }
                const BASE_URL = window.location.origin;
                let response = await fetch(`${BASE_URL}/upload`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
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
                const token = localStorage.getItem('token');
                if (!token) {
                    console.error("No Token Found, Please Login");
                    alert("Not Logged In");
                    return;
                }
                const BASE_URL = window.location.origin;
                let response = await fetch(`${BASE_URL}/updatedb`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
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