# Multi-Vendor E-Commerce Platform - UI/UX Design Specification

## 1. Information Architecture

### Main Navigation Structure
*   **Public / Buyer (Top Nav)**
    *   **Left**: Logo, Hamburger Menu (Categories)
    *   **Center**: Smart Search Bar (Products, Sellers, Categories)
    *   **Right**: Account (Dropdown), Favorites, Cart, "Sell on Platform" (CTA)
*   **Seller (Sidebar - Dashboard)**
    *   **Items**: Dashboard, Products, Orders, Messages, Campaigns, Analytics, Settings, Support.
*   **Admin (Sidebar - Backoffice)**
    *   **Items**: Dashboard, Users, Sellers, Disputes, Content (Reviews/Products), Finance, System Reports.

### Page Hierarchy

#### Buyer Realm
*   `Index` (Home) -> `Search/Browse` -> `Product Detail` -> `Cart` -> `Checkout` -> `Success`
*   `Account` -> `My Orders` -> `Order Detail` (Track/Dispute)
*   `Account` -> `Messages` -> `Chat`

#### Seller Realm
*   `Dashboard` (Overview)
*   `Products` -> `Add/Edit Product` (Variants/Images)
*   `Orders` -> `Order Detail` (Shipment/Labels)
*   `Finance` -> `Earnings/Payouts`

#### Admin Realm
*   `Dashboard` (KPIs)
*   `Moderation Queue` (Pending Sellers, Pending Products)
*   `Dispute Center` (Resolution Interface)

---

## 2. Screen List (Detailed)

### Buyer Interfaces
1.  **Home**: Hero banner (Campaigns), Featured Categories (Grid), "Daily Deals", Recommended Products (Horizontal Scroll).
2.  **Product Listing (PLP)**: Advanced Filters (Left sidebar: Price, Brand, Rating), Sorting (Top right), Product Grid (Image, Title, Price, Rating, "Add to Cart").
3.  **Product Detail (PDP)**:
    *   **Top**: Image Gallery (thumbnails + zoom), Buy Box (Price, Quantity, "Add to Cart", Seller info/rating).
    *   **Middle**: Variant Selector (Pills), Bundle Offers, Description tabs.
    *   **Bottom**: Reviews Section (Star breakdown, User photos), "Message Seller" button.
4.  **Cart**: List of items grouped by **Seller**. Subtotals per seller. Global Checkout button.
5.  **Checkout**: 3-Step Accordion: Address -> Shipping -> Payment. Order Summary sticky on right.
6.  **My Orders**: List view. Status badges (Processing, Shipped, Delivered). Actions: "Track", "Review", "Problem?".
7.  **Order Detail**: Timeline tracker. breakdown of split shipments. "Chat with Seller" context button.
8.  **Dispute Modal**: Form with Reason dropdown, Description text area, File upload (Images).
9.  **Messaging**: Inbox view. Threads grouped by Order ID.

### Seller Interfaces
1.  **Seller Dashboard**: Revenue Chart (Line graph), "Action Items" (Unshipped orders, Unread messages), Recent Activity feed.
2.  **Product Management**: Data Table view. Columns: Image, Name, Stock, Price, Status. Actions: Edit, Delete, Bulk Edit.
3.  **Add Product Wizard**: Steps: Basic Info -> Variants/Stock -> Images -> Shipping -> Review.
4.  **Order Management**: Kanban or List view. Tabs: New, Processing, Shipped, Completed, Returns.
5.  **Campaigns**: Calendar view or List. "Create Coupon" modal.
6.  **Store Settings**: Profile upload, Policy text editors, Bank Account form.

### Admin Interfaces
1.  **Admin Dashboard**: High-level metrics: GMV (Gross Merchandise Value), Active Users, Dispute Rate.
2.  **Seller Approval**: Grid of pending profiles. Documents preview (Tax ID). Approve/Reject with reasoning.
3.  **Dispute Resolution**: Split screen. Left: Dispute details & Evidence. Right: Order History & Chat Log. Bottom: Mediation controls (Refund/Close).

---

## 3. Wireframe Descriptions

### Buyer - Product Detail Page (PDP)
*   **Header**: Standard Nav.
*   **Breadcrumbs**: Home > Category > Sub-Category > Product Name.
*   **Main Content (2 Column Layout)**:
    *   **Left (60%)**: Large Image container. Thumbnail strip below. Below that: Tabbed content (Description, specs).
    *   **Right (40%)**: Product Title (H1), Rating (Stars + Count), Price (Large bold), Variant Selectors (Radio buttons or pills), Stock Status (Green text), "Sold by [Seller Name]" (Link to store), Primary CTA "Add to Cart" (Full width), Secondary CTA "Wishlist" (Icon).
*   **Footer**: Standard Footer.

### Seller - Order Management
*   **Header**: Dashboard Nav.
*   **Filter Bar**: Date Range, Status Dropdown, Search (Order ID/Customer Name).
*   **Main Widget (Data Table)**:
    *   **Rows**: Order ID, Date, Items (Summary), Total, Shipping Status, Actions.
    *   **Expanded Row**: Shows customer address and specific item details.
*   **Action Drawer**: Clicking an order slides out a details panel from the right. Contains: Print Label button, Tracking Number input field, Mark Shipped button.

---

## 4. Design System

### Color Palette
*   **Primary**: `Royal Blue` (#2563EB) - Trust, Professionalism. Used for CTAs, Links, Active states.
*   **Secondary**: `Slate Dark` (#1E293B) - Text, Navbars.
*   **Accent**: `Warm Orange` (#F59E0B) - Warnings, "Add to Cart", Star ratings.
*   **Semantic**:
    *   Success: `Emerald` (#10B981)
    *   Error: `Rose` (#E11D48)
    *   Neutral: `Gray` (#F3F4F6) - Backgrounds.

### Typography
*   **Font Family**: `Inter` or `Roboto` (Clean sans-serif).
*   **Hierarchy**:
    *   H1: 32px Bold (Page Titles)
    *   H2: 24px SemiBold (Section Headers)
    *   Body: 16px Regular (Readability focus)
    *   Small: 14px Medium (Metadata, Secondary text)

### Components
*   **Buttons**:
    *   Primary: Solid Blue, Rounded-md, White Text.
    *   Secondary: White, Blue Border, Blue Text.
    *   Ghost: Transparent, Text hover effect.
*   **Cards**: White bg, subtle shadow (`box-shadow: 0 1px 3px rgba(0,0,0,0.1)`), 8px border radius.
*   **Inputs**: 48px height, 1px Gray border. Focus ring: Blue. Label above input.
*   **Modals**: Centered, Backdrop blur, distinct Title and Close button.

---

## 5. UX Principles

*   **Trust First**:
    *   Seller ratings visible immediately.
    *   "Verified Purchase" badges on reviews.
    *   Secure Payment icons near checkout.
*   **Frictionless Checkout**:
    *   Guest checkout option (if allowed).
    *   Auto-fill addresses.
    *   Single-page checkout process where possible.
*   **Seller Feedback Loop**:
    *   Immediate toasts/notifications when orders arrive.
    *   Clear visual indicators for "Urgent" items (e.g., Shipping deadline approaching).
*   **Empty States**:
    *   Never show a blank page. If Cart is empty, show "Trending Items" or "Continue Shopping" CTA.
    *   If no orders match filter, show "Clear Filter" button.
*   **Accessibility**:
    *   All images must have `alt` tags (Product names).
    *   Colors must pass WCAG AA contrast ratio.
    *   Keyboard navigation support for all forms.

---

## 6. Responsive Design

*   **Mobile (Portrait)**:
    *   Hamburger menu for all nav items.
    *   Tables convert to "Card views" (stacked data).
    *   Checkout steps become separate pages (Stepper).
    *   Bottom Navigation Bar for Buyers (Home, Categories, Cart, Account).
*   **Tablet**:
    *   Sidebar navigation (Sellers/Admin) collapses to Icon-only rail.
    *   Grid layouts adjust from 4 columns (Desktop) to 2 columns.
*   **Desktop**:
    *   Full usage of horizontal space.
    *   Hover effects enabled.
    *   Multi-column dashboards.

---

## Summary
The design prioritizes clarity and transactional efficiency. By separating the Buyer (Discovery focus), Seller (Operations focus), and Admin (Oversight focus) experiences into distinct UI paradigms, the platform ensures that each user type can perform their core tasks with minimal cognitive load. The aesthetic is "Invisible Design"—it gets out of the way to let the products and data shine.
