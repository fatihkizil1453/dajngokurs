// frontend/favorites.js
const favorites = {
    getItems() {
        const items = localStorage.getItem('favorites');
        return items ? JSON.parse(items) : [];
    },

    saveItems(items) {
        localStorage.setItem('favorites', JSON.stringify(items));
        this.updateNavbarCount();
    },

    addItem(product) {
        const items = this.getItems();
        const prodId = Number(product.id);

        // Check if already exists
        if (items.find(item => Number(item.id) === prodId)) {
            return false; // Already in favorites
        }

        items.push({
            id: prodId,
            name: product.name,
            price: product.price,
            seller: product.seller || '',
            image: product.image || '',
            addedAt: new Date().toISOString()
        });

        this.saveItems(items);
        return true;
    },

    removeItem(productId) {
        let items = this.getItems();
        const pId = Number(productId);
        items = items.filter(item => Number(item.id) !== pId);
        this.saveItems(items);
    },

    isInFavorites(productId) {
        const items = this.getItems();
        return items.some(item => Number(item.id) === Number(productId));
    },

    toggle(product) {
        if (this.isInFavorites(product.id)) {
            this.removeItem(product.id);
            return { added: false, message: 'Favorilerden çıkarıldı' };
        } else {
            this.addItem(product);
            return { added: true, message: 'Favorilere eklendi' };
        }
    },

    getCount() {
        return this.getItems().length;
    },

    updateNavbarCount() {
        const favBadge = document.getElementById('favoritesCount');
        if (favBadge) {
            const count = this.getCount();
            favBadge.textContent = count > 0 ? `(${count})` : '';
        }
    },

    showToast(message, isAdded) {
        // Remove existing toast if any
        const existingToast = document.getElementById('favToast');
        if (existingToast) existingToast.remove();

        const toast = document.createElement('div');
        toast.id = 'favToast';
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${isAdded ? '#10b981' : '#ef4444'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            z-index: 9999;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            animation: fadeInUp 0.3s ease;
        `;
        toast.innerHTML = `${isAdded ? '♥' : '♡'} ${message}`;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }
};

// Make it global
window.favorites = favorites;

// Initial update on page load
document.addEventListener('DOMContentLoaded', () => {
    favorites.updateNavbarCount();
});
