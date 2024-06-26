function loginForm() {
    return {
        username: '',
        password: '',
        errorMessage: '',

        submitForm() {
            const BASE_URL = window.location.origin;
            fetch(`${BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password
                })
            })
            .then(response => {
                console.log(response);
                if (!response.ok) {
                    throw new Error('Invalid credentials');
                }
                return response.json();
            })
            .then(data => {
                if (data.token) {
                    localStorage.setItem('token', data.token);
                    window.location.href = urls.index;
                } else {
                    throw new Error('No Token in Response');
                }
            })
            .catch(error => {
                this.errorMessage = 'Login failed. Please check your username and password.';
            });
        },

        redirectToRegister() {
            window.location.href = urls.register;
        }
    }
}