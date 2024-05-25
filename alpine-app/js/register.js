function registerForm() {
    return {
        username: '',
        email: '',
        password: '',
        errorMessage: '',

        submitForm() {
            fetch('http://127.0.0.1:5000/register', {
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
                window.location.href = 'login.html';
            })
            .catch(error => {
                this.errorMessage = 'Registration failed. Please check your details and try again.';
            });
        }
    }
}