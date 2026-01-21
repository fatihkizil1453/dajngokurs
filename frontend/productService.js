// frontend/productService.js
const productService = {
    getProducts() {
        const stored = localStorage.getItem('products');
        if (!stored) {
            localStorage.setItem('products', JSON.stringify([]));
            return [];
        }
        return JSON.parse(stored);
    },

    saveProducts(products) {
        localStorage.setItem('products', JSON.stringify(products));
    },

    addProduct(product) {
        const products = this.getProducts();
        product.id = products.length > 0 ? Math.max(...products.map(p => p.id)) + 1 : 1;
        product.rating = 0;
        product.reviews = 0;
        products.push(product);
        this.saveProducts(products);
        return product;
    },

    updateProduct(id, updatedData) {
        const products = this.getProducts();
        const index = products.findIndex(p => p.id === Number(id));
        if (index !== -1) {
            products[index] = { ...products[index], ...updatedData };
            this.saveProducts(products);
            return products[index];
        }
        return null;
    },

    deleteProduct(id) {
        let products = this.getProducts();
        products = products.filter(p => p.id !== Number(id));
        this.saveProducts(products);
    },

    getProductById(id) {
        return this.getProducts().find(p => p.id === Number(id));
    },

    getSellerProducts(sellerName) {
        return this.getProducts().filter(p => p.seller === sellerName);
    },

    getProductsByCategory(category) {
        return this.getProducts().filter(p => p.category.toLowerCase() === category.toLowerCase());
    }
};

window.productService = productService;

// One-time cleanup to remove specific example products if they exist in storage
(function cleanupExamples() {
    const products = productService.getProducts();
    const toRemove = [
        'Kablosuz Kulaklık', 'Akıllı Saat Seri 7', 'Koşu Ayakkabısı', 'Mekanik Klavye',
        'Laptop Pro X', 'Akıllı Telefon 13', '4K Monitör', 'Bluetooth Hoparlör',
        'Oyuncu Faresi', 'USB-C Hub'
    ];
    const filtered = products.filter(p => !toRemove.includes(p.name));

    if (products.length !== filtered.length) {
        productService.saveProducts(filtered);
    }
})();
