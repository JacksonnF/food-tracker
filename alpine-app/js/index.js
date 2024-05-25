function datatables() {
    return {
    headings: [
        { key: 'foodId', value: 'Food ID' },
        { key: 'food_name', value: 'Food Name' },
        { key: 'current_count', value: 'Current Count' },
        { key: 'purchase_date', value: 'Purchase Date' },
        { key: 'actual_expiry', value: 'Expiry Date' },
        { key: 'days_remaining', value: 'Days Until Expiry' }
    ],
    items: [],

    init() {
        // Fetch the data when the component is initialized
        fetch('http://127.0.0.1:5000/items', {
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched:', data);
            const currentDate = new Date(); // Current date without time
                data.forEach(item => {
                const expiryDate = new Date(item.actual_expiry);
                const timeDifference = expiryDate.getTime() - currentDate.getTime();
                const daysRemaining = Math.ceil(timeDifference / (1000 * 3600 * 24));
                item.days_remaining = daysRemaining;
            });
            this.items = data;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    }
    }
}