// function datatables() {
//     return {
//         headings: [
//             { key: 'foodId', value: 'Food ID' },
//             { key: 'food_name', value: 'Food Name' },
//             { key: 'current_count', value: 'Current Count' },
//             { key: 'purchase_date', value: 'Purchase Date' },
//             { key: 'actual_expiry', value: 'Expiry Date' },
//             { key: 'days_remaining', value: 'Days Until Expiry' }
//         ],
//         items: [],
//         currentSort: '',
//         currentSortDir: 'asc',

//         init() {
//             const token = localStorage.getItem('token');
//             if (!token) {
//                 console.error("No Token Found, Please Login");
//                 this.showLoginModal = true;
//                 return;
//             }
//             fetch('http://127.0.0.1:5000/items', {
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'Access-Control-Allow-Origin': '*',
//                     'Authorization': `Bearer ${token}`
//                 }
//             })
//             .then(response => {
//                 if (!response.ok) {
//                 throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(data => {
//                 console.log('Data fetched:', data);
//                 const currentDate = new Date(); // Current date without time
//                     data.forEach(item => {
//                     const expiryDate = new Date(item.actual_expiry);
//                     const timeDifference = expiryDate.getTime() - currentDate.getTime();
//                     const daysRemaining = Math.ceil(timeDifference / (1000 * 3600 * 24));
//                     item.days_remaining = daysRemaining;
//                 });
//                 this.items = data;
//                 this.sort('days_remaining');
//             })
//             .catch(error => {
//                 console.error('There has been a problem with your fetch operation:', error);
//             });
//         },
//         sort(key) {
//             if (this.currentSort === key) {
//                 this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
//             } else {
//                 this.currentSortDir = 'asc';
//             }
//             this.currentSort = key;

//             this.items = this.items.sort((a, b) => {
//                 let aValue = a[key];
//                 let bValue = b[key];

//                 if (this.currentSortDir === 'asc') {
//                     return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
//                 } else {
//                     return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
//                 }
//             });
//         },
//         showLoginModal: false
//     }
// }

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
        currentSort: '',
        currentSortDir: 'asc',

        init() {
            this.showLoginModal = false;
            const token = localStorage.getItem('token');
            if (!token) {
                console.error("No Token Found, Please Login");
                this.showLoginModal = true;
                return;
            }
            fetch('http://127.0.0.1:5000/items', {
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authorization': `Bearer ${token}`
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
                this.sort('days_remaining');
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        },
        sort(key) {
            if (this.currentSort === key) {
                this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
            } else {
                this.currentSortDir = 'asc';
            }
            this.currentSort = key;

            this.items = this.items.sort((a, b) => {
                let aValue = a[key];
                let bValue = b[key];

                if (this.currentSortDir === 'asc') {
                    return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
                } else {
                    return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
                }
            });
        },
    }
}