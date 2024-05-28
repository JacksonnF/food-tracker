function logout() {
    localStorage.removeItem('token');

    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Logged out successfully") {
            window.location.href = '/login-page';
        }
    })
    .catch(error => console.error('Error logging out:', error));
}
