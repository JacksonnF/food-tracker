function registerForm() {
    return {
        username: '',
        email: '',
        password: '',
        errorMessage: '',

        submitForm() {
            const BASE_URL = window.location.origin;
            fetch(`${BASE_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    email: this.email,
                    password: this.password
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Registration failed');
                }
                return response.json();
            })
            .then(data => {
                window.location.href = urls.login;
            })
            .catch(error => {
                this.errorMessage = 'Registration failed. Please check your details and try again.';
            });
        }
    }
}