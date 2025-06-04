    const BASE_URL = 'http://localhost:5000';

    // Show/hide sections
    function showSection(sectionId) {
      document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
      });
      document.getElementById(sectionId).classList.remove('hidden');
    }

    // Display message
    function showMessage(text, isError = false) {
      const messageDiv = document.getElementById('message');
      messageDiv.textContent = text;
      messageDiv.className = `message ${isError ? 'error' : 'success'}`;
      messageDiv.style.display = 'block';
      setTimeout(() => { messageDiv.style.display = 'none'; }, 3000);
    }

    // Fetch and display inventory
    async function fetchInventory() {
      try {
        const response = await fetch(`${BASE_URL}/inventory`);
        const products = await response.json();
        const tbody = document.getElementById('inventory-body');
        tbody.innerHTML = '';
        products.forEach(product => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${product.product_id}</td>
            <td>${product.name}</td>
            <td>${product.quantity}</td>
            <td><button class="delete-btn" onclick="deleteProduct(${product.product_id})">Delete</button></td>
          `;
          tbody.appendChild(row);
        });
      } catch (error) {
        showMessage('Error fetching inventory', true);
      }
    }

    // Fetch and display orders
    async function fetchOrders() {
      try {
        const response = await fetch(`${BASE_URL}/orders`);
        const orders = await response.json();
        const list = document.getElementById('orders-list');
        list.innerHTML = '';
        orders.forEach(order => {
          const li = document.createElement('li');
          li.textContent = `Order ID: ${order}`;
          list.appendChild(li);
        });
      } catch (error) {
        showMessage('Error fetching orders', true);
      }
    }

    // Add product manually
    async function addProduct() {
      const productId = document.getElementById('product-id').value;
      const name = document.getElementById('product-name').value;
      const quantity = document.getElementById('quantity').value;
      if (!productId || !name || !quantity) {
        showMessage('Please fill all product fields', true);
        return;
      }
      try {
        const response = await fetch(`${BASE_URL}/inventory`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product_id: parseInt(productId), name, quantity: parseInt(quantity) })
        });
        const data = await response.json();
        showMessage(data.message, response.status >= 400);
        fetchInventory();
        document.getElementById('product-id').value = '';
        document.getElementById('product-name').value = '';
        document.getElementById('quantity').value = '';
      } catch (error) {
        showMessage('Error adding product', true);
      }
    }

    // Bulk product upload
    async function uploadBulkProducts() {
      const fileInput = document.getElementById('bulk-file');
      const file = fileInput.files[0];
      if (!file) {
        showMessage('Please select a CSV or TXT file', true);
        return;
      }
      if (!file.name.endsWith('.csv') && !file.name.endsWith('.txt')) {
        showMessage('File must be a CSV or TXT', true);
        return;
      }
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await fetch(`${BASE_URL}/inventory/bulk`, {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        showMessage(data.message, response.status >= 400);
        fetchInventory();
        fileInput.value = '';
      } catch (error) {
        showMessage('Error uploading products', true);
      }
    }

    // Delete product
    async function deleteProduct(productId) {
      try {
        const response = await fetch(`${BASE_URL}/inventory/${productId}`, { method: 'DELETE' });
        const data = await response.json();
        showMessage(data.message, response.status >= 400);
        fetchInventory();
      } catch (error) {
        showMessage('Error deleting product', true);
      }
    }

    // Add order
    async function addOrder() {
      const orderId = document.getElementById('order-id').value;
      if (!orderId) {
        showMessage('Please enter an order ID', true);
        return;
      }
      try {
        const response = await fetch(`${BASE_URL}/orders`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ order_id: parseInt(orderId) })
        });
        const data = await response.json();
        showMessage(data.message, response.status >= 400);
        fetchOrders();
        document.getElementById('order-id').value = '';
      } catch (error) {
        showMessage('Error adding order', true);
      }
    }

    // Process order
    async function processOrder() {
      try {
        const response = await fetch(`${BASE_URL}/orders/process`, { method: 'POST' });
        const data = await response.json();
        showMessage(data.message);
        fetchOrders();
      } catch (error) {
        showMessage('Error processing order', true);
      }
    }

    // Search product
    async function searchProduct() {
      const searchId = document.getElementById('search-id').value;
      if (!searchId) {
        showMessage('Please enter a product ID', true);
        return;
      }
      try {
        const response = await fetch(`${BASE_URL}/inventory/search/${searchId}`);
        const data = await response.json();
        if (response.status === 200 && data.product_id) {
          showMessage(`Found: ${data.name} (ID: ${data.product_id}, Quantity: ${data.quantity})`);
        } else {
          showMessage(data.message, true);
        }
        document.getElementById('search-id').value = '';
      } catch (error) {
        showMessage('Error searching product', true);
      }
    }

    // Sort inventory
    async function sortInventory() {
      try {
        const response = await fetch(`${BASE_URL}/inventory/sort`, { method: 'POST' });
        const data = await response.json();
        showMessage(data.message);
        fetchInventory();
      } catch (error) {
        showMessage('Error sorting inventory', true);
      }
    }

    // Initial fetch and show inventory
    fetchInventory();
    fetchOrders();
    showSection('inventory');