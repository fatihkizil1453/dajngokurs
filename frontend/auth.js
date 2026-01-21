// frontend/auth.js
const API_BASE_URL = '/api/auth';

const auth = {
    async login(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,       // Backend expects 'email' as primary key
                    username: email     // But we send both to be safe
                    , password
                }),
            });

            if (response.ok) {
                const user = await response.json();
                localStorage.setItem('user', JSON.stringify(user));
                return { success: true };
            }
            const errorData = await response.json();
            console.error('Login failed:', errorData);
            return { success: false, error: errorData };
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: 'Network error or server down' };
        }
    },

    async register(data) {
        try {
            const response = await fetch(`${API_BASE_URL}/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Register failed:', errorData);
                return { success: false, error: errorData };
            }

            return { success: true };
        } catch (error) {
            console.error('Register error:', error);
            return { success: false, error: 'Network error or server down' };
        }
    },

    logout() {
        localStorage.removeItem('user');
        // Optionally call the logout API to clear the session cookie
        fetch(`${API_BASE_URL}/logout/`, { method: 'POST' }).catch(() => { });
        window.location.href = 'index.html';
    },

    getUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    saveUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    async updateProfile(updatedData) {
        const user = this.getUser();
        if (!user) return { success: false, error: 'User not logged in' };

        // In a real app, this would be a fetch call to the backend
        // For this demo, we'll update the local storage directly
        const updatedUser = { ...user, ...updatedData };
        this.saveUser(updatedUser);

        // Refresh UI
        this.updateNavbar();
        return { success: true };
    },

    isLoggedIn() {
        return !!this.getUser();
    },

    updateNavbar() {
        const navActions = document.querySelector('.nav-actions');
        if (!navActions) return;

        const user = this.getUser();
        const isHomePage = document.body.getAttribute('data-page') === 'home';

        if (user) {
            // User is logged in
            const isSeller = user.role === 'SELLER';
            let html = `
                ${isSeller ? '<a href="../seller/seller-dashboard.html" class="text-sm font-semibold text-muted">MarketPlus\'ta Satış Yap</a>' : ''}
                <a href="profile.html" class="nav-item">Hesabım (${user.first_name})</a>
                <a href="favorites.html" class="nav-item">Favorilerim <span id="favoritesCount">${typeof favorites !== 'undefined' && favorites.getCount() > 0 ? '(' + favorites.getCount() + ')' : ''}</span></a>
                <a href="orders.html" class="nav-item">Siparişlerim</a>
                <a href="#" id="logoutBtn" class="nav-item">Çıkış Yap</a>
                ${user.role === 'BUYER' ? `<a href="cart.html" class="nav-item btn btn-primary btn-sm">Sepet (${typeof cart !== 'undefined' ? cart.getCount() : 0})</a>` : ''}
            `;
            navActions.innerHTML = html;

            const logoutBtn = document.getElementById('logoutBtn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    auth.logout();
                });
            }
        } else {
            // User is not logged in
            if (isHomePage) {
                // Clean homepage for guests
                let html = `
                    <a href="login.html" class="nav-item">Giriş Yap</a>
                    <a href="register.html" class="nav-item">Kayıt Ol</a>
                `;
                navActions.innerHTML = html;
            } else {
                // Show full options on other pages for guests
                let html = `
                    <a href="../seller/seller-dashboard.html" class="text-sm font-semibold text-muted">MarketPlus'ta Satış Yap</a>
                    <a href="login.html" class="nav-item">Giriş Yap</a>
                    <a href="register.html" class="nav-item">Kayıt Ol</a>
                    <a href="cart.html" class="nav-item btn btn-primary btn-sm">Sepet (${typeof cart !== 'undefined' ? cart.getCount() : 0})</a>
                `;
                navActions.innerHTML = html;
            }
        }
    }
};

// Auto-update navbar and sidebars on page load
document.addEventListener('DOMContentLoaded', () => {
    auth.updateNavbar();

    // Also update any profile sidebars if they exist on the page
    const user = auth.getUser();
    if (user) {
        const sidebarName = document.querySelector('.sidebar .font-bold');
        const sidebarAvatar = document.querySelector('.sidebar div[style*="width: 40px"]');

        if (sidebarName) {
            sidebarName.textContent = (user.first_name + ' ' + user.last_name).trim() || user.email;
        }

        const sidebarRole = document.querySelector('.sidebar .text-xs.text-muted');
        if (sidebarRole) {
            sidebarRole.textContent = user.role === 'SELLER' ? 'Satıcı Hesabı' : 'Müşteri Hesabı';
        }

        if (sidebarAvatar) {
            const initials = (user.first_name?.[0] || '') + (user.last_name?.[0] || '');
            sidebarAvatar.textContent = initials.toUpperCase() || user.email[0].toUpperCase();
        }

        // Attach logout to any logout triggers found
        document.querySelectorAll('.logout-trigger').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                auth.logout();
            });
        });
    }
});
