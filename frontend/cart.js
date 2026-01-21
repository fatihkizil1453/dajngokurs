// frontend/cart.js
const cart = {
    getItems() {
        const items = localStorage.getItem('cart');
        return items ? JSON.parse(items) : [];
    },

    saveItems(items) {
        localStorage.setItem('cart', JSON.stringify(items));
        this.updateNavbarCount();
    },

    addItem(product) {
        // Check stock availability first
        if (product.stock_quantity !== undefined && product.stock_quantity <= 0) {
            this.showStockWarning('Bu ürün şu anda stokta bulunmamaktadır.');
            return;
        }

        const items = this.getItems();
        // Normalize IDs to handle string/number comparison and undefined variantId
        const prodId = Number(product.id);
        const vId = product.variantId ? Number(product.variantId) : 0;

        const existingItem = items.find(item => Number(item.id) === prodId && (item.variantId ? Number(item.variantId) : 0) === vId);

        const qtyToAdd = product.quantity ? parseInt(product.quantity) : 1;

        // Check if adding this quantity would exceed stock
        if (product.stock_quantity !== undefined) {
            const currentQty = existingItem ? existingItem.quantity : 0;
            const totalQty = currentQty + qtyToAdd;

            if (totalQty > product.stock_quantity) {
                const available = product.stock_quantity - currentQty;
                if (available <= 0) {
                    this.showStockWarning('Bu ürün için maksimum stok miktarına ulaştınız.');
                } else {
                    this.showStockWarning(`Stokta sadece ${available} adet bulunmaktadır.`);
                }
                return;
            }
        }

        if (existingItem) {
            existingItem.quantity += qtyToAdd;
            // Update image if it was missing or provided
            if (product.image) {
                existingItem.image = product.image;
            }
            // Update stock quantity for future checks
            if (product.stock_quantity !== undefined) {
                existingItem.stock_quantity = product.stock_quantity;
            }
        } else {
            items.push({
                ...product,
                id: prodId,
                variantId: vId,
                quantity: qtyToAdd,
                image: product.image || ''
            });
        }

        this.saveItems(items);
        this.showSuccessMessage(`${product.name} sepete eklendi!`);
    },

    showStockWarning(message) {
        // Create a styled warning toast
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: #fef2f2;
            color: #991b1b;
            padding: 16px 24px;
            border-radius: 8px;
            border-left: 4px solid #dc2626;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            font-family: Inter, sans-serif;
            font-size: 14px;
            font-weight: 500;
            max-width: 350px;
            animation: slideIn 0.3s ease-out;
        `;
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 24px;">⚠️</span>
                <div>
                    <div style="font-weight: 600; margin-bottom: 4px;">Stok Yetersiz</div>
                    <div style="font-weight: 400; opacity: 0.9;">${message}</div>
                </div>
            </div>
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },

    showSuccessMessage(message) {
        // Create a styled success toast
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: #f0fdf4;
            color: #166534;
            padding: 16px 24px;
            border-radius: 8px;
            border-left: 4px solid #16a34a;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            font-family: Inter, sans-serif;
            font-size: 14px;
            font-weight: 500;
            max-width: 350px;
            animation: slideIn 0.3s ease-out;
        `;
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 24px;">✓</span>
                <div style="font-weight: 500;">${message}</div>
            </div>
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    removeItem(productId, variantId) {
        let items = this.getItems();
        const pId = Number(productId);
        const vId = Number(variantId) || 0;

        items = items.filter(item => !(Number(item.id) === pId && (Number(item.variantId) || 0) === vId));
        this.saveItems(items);
        this.renderCart();
    },

    updateQuantity(productId, variantId, quantity) {
        const items = this.getItems();
        const pId = Number(productId);
        const vId = Number(variantId) || 0;

        const item = items.find(item => Number(item.id) === pId && (Number(item.variantId) || 0) === vId);
        if (item) {
            item.quantity = parseInt(quantity) || 1;
            if (item.quantity <= 0) {
                this.removeItem(productId, variantId);
            } else {
                this.saveItems(items);
                this.renderCart();
            }
        }
    },

    getCount() {
        const items = this.getItems();
        return items.reduce((total, item) => total + item.quantity, 0);
    },

    getTotal() {
        const items = this.getItems();
        return items.reduce((total, item) => total + (item.price * item.quantity), 0);
    },

    clear() {
        localStorage.removeItem('cart');
        this.updateNavbarCount();
    },

    updateNavbarCount() {
        const cartBadge = document.querySelector('.nav-item.btn-primary');
        if (cartBadge) {
            cartBadge.textContent = `Sepet (${this.getCount()})`;
        }
    },

    renderCart() {
        const cartContainer = document.getElementById('cartItemsContainer');
        const summaryContainer = document.getElementById('cartSummaryContainer');

        if (!cartContainer || !summaryContainer) return;

        const items = this.getItems();
        const count = this.getCount();

        // Update Header
        const header = cartContainer.querySelector('h1');
        if (header) header.textContent = `Sepet (${count} Ürün)`;

        // Remove old items/loading messages
        const childNodes = Array.from(cartContainer.children);
        childNodes.forEach(node => {
            if (node.tagName !== 'H1') {
                node.remove();
            }
        });

        if (items.length === 0) {
            const emptyMsg = document.createElement('div');
            emptyMsg.className = 'bg-white rounded shadow-sm border p-8 text-center';
            emptyMsg.innerHTML = `
                <div class="text-muted mb-4">Sepetiniz şu an boş.</div>
                <a href="products.html" class="btn btn-primary">Alışverişe Başla</a>
            `;
            cartContainer.appendChild(emptyMsg);

            summaryContainer.innerHTML = `
                <h2 class="font-bold text-lg mb-4">Sipariş Özeti</h2>
                <div class="text-muted text-sm">Sepetinizde ürün bulunmamaktadır.</div>
            `;
            return;
        }

        // Group items by seller
        const sellers = {};
        items.forEach(item => {
            const sName = item.seller || 'Bilinmeyen Satıcı';
            if (!sellers[sName]) sellers[sName] = [];
            sellers[sName].push(item);
        });

        for (const [sellerName, sellerItems] of Object.entries(sellers)) {
            const sellerGroup = document.createElement('div');
            sellerGroup.className = 'bg-white rounded shadow-sm border p-4 mb-4';

            let itemsHtml = `
                <div class="font-semibold border-b pb-2 mb-2 flex justify-between">
                    <span>Satıcı: ${sellerName}</span>
                    <span class="text-sm text-success">Kargo Bedava</span>
                </div>
            `;

            sellerItems.forEach(item => {
                const imgHtml = item.image
                    ? `<img src="${item.image}" style="width: 100%; height: 100%; object-fit: contain; padding: 4px;">`
                    : 'Görsel Yok';

                itemsHtml += `
                    <div class="flex gap-4 mb-4 pb-4 border-b last:border-0">
                        <div style="width: 80px; height: 80px; background: white; border: 1px solid #eee; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; text-align: center; color: #999; overflow: hidden;">${imgHtml}</div>
                        <div class="flex-1">
                            <h3 class="font-semibold">${item.name}</h3>
                            <div class="text-sm text-muted">Varyant: ${item.variantName || 'Standart'}</div>
                            <div class="mt-2 flex justify-between items-center">
                                <input type="number" value="${item.quantity}" min="1" class="form-control" style="width: 60px;" 
                                    onchange="cart.updateQuantity(${item.id}, ${item.variantId}, this.value)">
                                <span class="font-bold">${(item.price * item.quantity).toLocaleString('tr-TR')} TL</span>
                            </div>
                            <button class="text-sm text-danger mt-1 hover:underline" onclick="cart.removeItem(${item.id}, ${item.variantId})">Sil</button>
                        </div>
                    </div>
                `;
            });

            sellerGroup.innerHTML = itemsHtml;
            cartContainer.appendChild(sellerGroup);
        }

        // Update Summary
        const total = this.getTotal();
        summaryContainer.innerHTML = `
            <h2 class="font-bold text-lg mb-4">Sipariş Özeti</h2>
            <div class="flex justify-between mb-2">
                <span class="text-muted">Ara Toplam</span>
                <span>${total.toLocaleString('tr-TR')} TL</span>
            </div>
            <div class="flex justify-between mb-2">
                <span class="text-muted">Kargo</span>
                <span class="text-success">Ücretsiz</span>
            </div>
            <div class="flex justify-between mb-4 border-t pt-2 font-bold text-lg">
                <span>Toplam</span>
                <span class="text-primary">${total.toLocaleString('tr-TR')} TL</span>
            </div>
            <a href="checkout.html" class="btn btn-primary btn-block mb-2">Alışverişi Tamamla</a>
            <a href="products.html" class="btn btn-secondary btn-block">Alışverişe Devam Et</a>
        `;
    }
};

// Make it global
window.cart = cart;

// Initial update
document.addEventListener('DOMContentLoaded', () => {
    cart.updateNavbarCount();
    // Use container check instead of URL path check
    if (document.getElementById('cartItemsContainer')) {
        cart.renderCart();
    }
});
