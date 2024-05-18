function app() {
    return {
        items: [],
        fetchItems() {
            console.log('Button clicked!');
            fetch('http://127.0.0.1:5000/items')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Data fetched:', data);
                    this.items = data;
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
        }
    };
}

