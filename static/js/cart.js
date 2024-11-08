// Cart functionality
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function updateCart() {
    const cartCount = document.getElementById('cart-count');
    const cartPreview = document.getElementById('cart-preview');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    cartCount.textContent = totalItems;
    
    // Update cart preview
    if (cartPreview) {
        cartPreview.innerHTML = '';
        let total = 0;
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            const itemElement = document.createElement('div');
            itemElement.className = 'cart-item d-flex justify-content-between align-items-center p-2';
            itemElement.innerHTML = `
                <span>${item.name} x ${item.quantity}</span>
                <span>$${itemTotal.toFixed(2)}</span>
            `;
            cartPreview.appendChild(itemElement);
        });
        
        if (cart.length > 0) {
            const totalElement = document.createElement('div');
            totalElement.className = 'cart-total d-flex justify-content-between align-items-center p-2 border-top';
            totalElement.innerHTML = `
                <strong>Total:</strong>
                <strong>$${total.toFixed(2)}</strong>
            `;
            cartPreview.appendChild(totalElement);
        } else {
            cartPreview.innerHTML = '<p class="text-center m-3">Your cart is empty</p>';
        }
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(id, name, price) {
    const quantityInput = document.querySelector(`input[data-item-id="${id}"]`);
    const quantity = parseInt(quantityInput.value);
    
    if (quantity < 1) return;
    
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ id, name, price, quantity });
    }
    
    quantityInput.value = 1;
    updateCart();
    
    // Show feedback animation
    const addButton = document.querySelector(`button[data-item-id="${id}"]`);
    addButton.classList.add('btn-success');
    setTimeout(() => addButton.classList.remove('btn-success'), 500);
}

// Initialize cart on page load
document.addEventListener('DOMContentLoaded', updateCart);
