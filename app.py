import streamlit as st
from datetime import datetime, date
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="URAMix - Waste to Wealth",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for green theme
st.markdown("""
    <style>
    .main {
        background-color: #f0f8f0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1, h2, h3 {
        color: #2E7D32;
    }
    .credit-box {
        background-color: #C8E6C9;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'credits' not in st.session_state:
    st.session_state.credits = 0
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'total_manure' not in st.session_state:
    st.session_state.total_manure = 0
if 'daily_credits' not in st.session_state:
    st.session_state.daily_credits = [5, 8, 12, 15, 20, 18, 22]

# Login page
def login_page():
    st.title("🌿 Welcome to URAMix")
    st.subheader("Login to Continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        username = st.text_input("👤 Enter Username", key="login_username")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔐 User Login", use_container_width=True):
                if username:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.is_admin = False
                    st.session_state.credits = 150  # Demo credits
                    st.rerun()
                else:
                    st.error("Please enter a username")
        
        with col_btn2:
            if st.button("👨‍💼 Admin Login", use_container_width=True):
                if username == "admin":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Admin username is 'admin'")

# Home page
def home_page():
    # Header
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>♻️ URAMix - Smart Waste to Wealth Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>From Waste to Wealth 🌱</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Images and tagline
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=600", 
                 caption="Smart Waste Segregation", use_container_width=True)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=600", 
                 caption="Organic Manure Production", use_container_width=True)
    
    # How it works
    st.markdown("---")
    st.header("🔄 How URAMix Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 📦 Step 1")
        st.write("Segregate waste at home (Organic & Inorganic)")
    
    with col2:
        st.markdown("### 🚚 Step 2")
        st.write("Book a pickup slot through URAMix")
    
    with col3:
        st.markdown("### 🌾 Step 3")
        st.write("Earn credits for waste submission")
    
    with col4:
        st.markdown("### 💰 Step 4")
        st.write("Convert credits to money or buy manure")
    
    st.markdown("---")
    
    # Action buttons
    st.header("🚀 Get Started")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Book Waste Slot", use_container_width=True):
            st.session_state.page = "Book Slot"
            st.rerun()
    
    with col2:
        if st.button("💳 View Credits", use_container_width=True):
            st.session_state.page = "Credits"
            st.rerun()
    
    with col3:
        if st.button("🌱 Buy Manure", use_container_width=True):
            st.session_state.page = "Manure"
            st.rerun()

# About Us page
def about_page():
    st.title("ℹ️ About URAMix")
    st.markdown("---")
    
    # Problem Statement
    st.header("🚨 The Problem")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Waste Crisis in India")
        st.write("• India generates nearly **62 million tons of waste per year**")
        st.write("• More than **70% of waste ends up in landfills**")
        st.write("• Landfills cause **soil pollution** and **groundwater contamination**")
        st.write("• Serious **health problems** in nearby communities")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?w=500", 
                 caption="Landfill pollution affecting our environment")
    
    st.markdown("---")
    
    # Why improper disposal
    st.header("❓ Why People Dispose Waste Improperly")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### ⏰")
        st.write("Cannot wait until dustbins are full")
    
    with col2:
        st.markdown("### 🚫")
        st.write("Irregular garbage collection")
    
    with col3:
        st.markdown("### 💭")
        st.write("No reward or motivation")
    
    with col4:
        st.markdown("### 🗑️")
        st.write("Waste gets mixed together")
    
    st.markdown("---")
    
    # Natural farming problem
    st.header("🌾 Natural Farming Challenge")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=500", 
                 caption="Farmers need affordable organic manure")
    
    with col2:
        st.markdown("### 💸 Cost Barriers")
        st.write("• **Organic manure is costly** - farmers cannot afford it")
        st.write("• Many farmers rely on **chemical fertilizers**")
        st.write("• Chemical fertilizers **damage soil health** over time")
        st.write("• Need for **affordable organic alternatives**")
    
    st.markdown("---")
    
    # URAMix Solution
    st.header("✅ URAMix Solution")
    st.success("We bridge the gap between waste management and natural farming!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### For Citizens 🏠")
        st.write("✓ Segregate waste at home")
        st.write("✓ Book pickup slots conveniently")
        st.write("✓ Earn credits for participation")
        st.write("✓ Convert credits to real money")
        st.write("✓ Buy affordable manure for gardens")
    
    with col2:
        st.markdown("### For Environment & Farmers 🌍")
        st.write("✓ Organic waste → Manure conversion")
        st.write("✓ Inorganic waste → Recycling")
        st.write("✓ Reduced landfill burden")
        st.write("✓ Affordable manure for farmers")
        st.write("✓ Promotes sustainable living")
    
    st.markdown("---")
    st.info("🎯 **Our Mission**: Make India Clean | Reduce Landfills | Support Natural Farming")

# Book Slot page
def book_slot_page():
    st.title("📅 Book Waste Pickup Slot")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Schedule Your Pickup")
        
        # Date selection
        pickup_date = st.date_input(
            "📆 Select Pickup Date",
            min_value=date.today(),
            value=date.today()
        )
        
        # Number of bags
        num_bags = st.number_input(
            "🗑️ Number of Organic Waste Bags",
            min_value=1,
            max_value=10,
            value=1,
            help="Each bag should be approximately 5-10 kg"
        )
        
        # Address
        address = st.text_area("📍 Pickup Address", placeholder="Enter your complete address")
        
        # Phone number
        phone = st.text_input("📱 Contact Number", placeholder="Enter 10-digit mobile number")
        
        # Booking button
        if st.button("✅ Confirm Booking", use_container_width=True):
            if address and phone:
                booking = {
                    'date': pickup_date.strftime("%Y-%m-%d"),
                    'bags': num_bags,
                    'address': address,
                    'phone': phone,
                    'username': st.session_state.username
                }
                st.session_state.bookings.append(booking)
                st.session_state.total_manure += num_bags * 2  # 2 kg manure per bag
                
                st.success(f"🎉 Booking Confirmed for {pickup_date.strftime('%B %d, %Y')}!")
                st.info(f"📦 Bags: {num_bags} | You will earn 1 credit upon pickup")
                st.balloons()
            else:
                st.error("Please fill all details")
    
    with col2:
        st.markdown("<div class='credit-box'>", unsafe_allow_html=True)
        st.markdown("### 💡 Important Notes")
        st.write("✓ Segregate organic waste")
        st.write("✓ Keep bags ready")
        st.write("✓ Earn 1 credit per day")
        st.write("✓ No quantity-based credits")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.image("https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?w=400",
                 caption="Keep waste segregated")

# Credits page
def credits_page():
    st.title("💳 Credits & Wallet")
    st.markdown("---")
    
    # Calculate rupees
    rupees = st.session_state.credits / 20
    
    # Wallet display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='credit-box'>", unsafe_allow_html=True)
        st.markdown("### 🪙 Total Credits")
        st.markdown(f"<h1 style='color: #2E7D32;'>{st.session_state.credits}</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='credit-box'>", unsafe_allow_html=True)
        st.markdown("### 💰 Wallet Balance")
        st.markdown(f"<h1 style='color: #2E7D32;'>₹{rupees:.2f}</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='credit-box'>", unsafe_allow_html=True)
        st.markdown("### 📊 Conversion Rate")
        st.markdown("<h1 style='color: #2E7D32;'>20:1</h1>", unsafe_allow_html=True)
        st.write("20 Credits = ₹1")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Withdrawal section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💸 Withdraw Credits")
        
        if st.session_state.credits >= 500:
            withdraw_credits = st.number_input(
                "Enter credits to withdraw (Min: 500)",
                min_value=500,
                max_value=st.session_state.credits,
                value=500,
                step=100
            )
            
            withdraw_amount = withdraw_credits / 20
            
            st.info(f"You will receive: ₹{withdraw_amount:.2f}")
            
            if st.button("💵 Withdraw to Bank", use_container_width=True):
                st.session_state.credits -= withdraw_credits
                st.success(f"✅ ₹{withdraw_amount:.2f} withdrawn successfully!")
                st.balloons()
                st.rerun()
        else:
            st.warning(f"⚠️ You need {500 - st.session_state.credits} more credits to withdraw")
            st.info("💡 Keep submitting waste daily to earn more credits!")
    
    with col2:
        st.markdown("### 📋 How to Earn")
        st.write("• Submit waste daily")
        st.write("• Earn 1 credit per day")
        st.write("• Quantity doesn't matter")
        st.write("• Minimum 500 to withdraw")
        
        # Add credits button (demo)
        if st.button("🎁 Add Demo Credits (+50)", use_container_width=True):
            st.session_state.credits += 50
            st.rerun()

# Manure page
def manure_page():
    st.title("🌱 Buy Organic Manure")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Available Manure")
        
        # Manure stats
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("📦 Total Available", f"{st.session_state.total_manure} kg")
        
        with col_b:
            st.metric("💵 Price per kg", "₹15")
        
        with col_c:
            st.metric("🏷️ Market Price", "₹40-50")
        
        st.markdown("---")
        
        # Purchase section
        st.subheader("🛒 Purchase Manure")
        
        quantity = st.number_input(
            "Quantity (in kg)",
            min_value=1,
            max_value=min(100, st.session_state.total_manure),
            value=5,
            disabled=(st.session_state.total_manure == 0)
        )
        
        total_price = quantity * 15
        
        st.info(f"💰 Total Amount: ₹{total_price}")
        
        address = st.text_area("📍 Delivery Address", placeholder="Enter delivery address")
        
        if st.button("🛍️ Buy Now", use_container_width=True, disabled=(st.session_state.total_manure == 0)):
            if address:
                st.session_state.total_manure -= quantity
                st.success(f"✅ Order placed successfully for {quantity} kg!")
                st.info("📦 Manure will be delivered in 2-3 days")
                st.balloons()
            else:
                st.error("Please enter delivery address")
    
    with col2:
        st.markdown("### 🌟 Benefits")
        st.write("✓ 100% Organic")
        st.write("✓ Improves soil health")
        st.write("✓ No chemicals")
        st.write("✓ Affordable price")
        st.write("✓ Supports sustainability")
        
        st.image("https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400",
                 caption="Pure organic manure")
    
    st.markdown("---")
    
    # Benefits details
    st.header("🌾 Why Choose Organic Manure?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌍 For Environment")
        st.write("• Reduces chemical pollution")
        st.write("• Sustainable farming")
        st.write("• Reduces carbon footprint")
    
    with col2:
        st.markdown("### 🌱 For Soil")
        st.write("• Improves soil structure")
        st.write("• Increases water retention")
        st.write("• Boosts microbial activity")
    
    with col3:
        st.markdown("### 🥬 For Crops")
        st.write("• Better crop yield")
        st.write("• Healthier produce")
        st.write("• Long-term benefits")

# Admin Dashboard
def admin_page():
    st.title("👨‍💼 Admin Dashboard")
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total Bookings", len(st.session_state.bookings))
    
    with col2:
        total_bags = sum([b['bags'] for b in st.session_state.bookings])
        st.metric("🗑️ Total Bags", total_bags)
    
    with col3:
        st.metric("🌱 Manure Produced", f"{st.session_state.total_manure} kg")
    
    with col4:
        total_credits_issued = len(st.session_state.bookings)
        st.metric("🪙 Credits Issued", total_credits_issued)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Credits Issued Per Day")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ax.plot(days, st.session_state.daily_credits, marker='o', color='#4CAF50', linewidth=2)
        ax.fill_between(range(len(days)), st.session_state.daily_credits, alpha=0.3, color='#4CAF50')
        ax.set_xlabel('Day')
        ax.set_ylabel('Credits')
        ax.set_title('Daily Credits Distribution')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("📈 Waste Collection Stats")
        
        if st.session_state.bookings:
            fig, ax = plt.subplots(figsize=(8, 4))
            bag_counts = [b['bags'] for b in st.session_state.bookings[-7:]]
            ax.bar(range(len(bag_counts)), bag_counts, color='#8BC34A', alpha=0.8)
            ax.set_xlabel('Booking Number')
            ax.set_ylabel('Bags Collected')
            ax.set_title('Recent Waste Collections')
            ax.grid(True, alpha=0.3, axis='y')
            st.pyplot(fig)
        else:
            st.info("No bookings yet")
    
    st.markdown("---")
    
    # Recent bookings table
    st.subheader("📋 Recent Bookings")
    
    if st.session_state.bookings:
        df = pd.DataFrame(st.session_state.bookings)
        st.dataframe(df[['username', 'date', 'bags', 'phone']], use_container_width=True)
    else:
        st.info("No bookings to display")

# Main app logic
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.title("♻️ URAMix")
            st.write(f"👤 Welcome, **{st.session_state.username}**!")
            
            st.markdown("---")
            
            # Navigation
            if st.session_state.is_admin:
                page = st.radio(
                    "Navigation",
                    ["Home", "About Us", "Admin Dashboard"]
                )
            else:
                page = st.radio(
                    "Navigation",
                    ["Home", "About Us", "Book Slot", "Credits", "Manure"]
                )
            
            st.markdown("---")
            
            # Credits display for users
            if not st.session_state.is_admin:
                st.markdown("<div class='credit-box'>", unsafe_allow_html=True)
                st.write("💳 **Your Credits**")
                st.markdown(f"<h2 style='color: #2E7D32;'>{st.session_state.credits}</h2>", unsafe_allow_html=True)
                st.write(f"= ₹{st.session_state.credits/20:.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Logout
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.is_admin = False
                st.rerun()
        
        # Page routing
        if page == "Home":
            home_page()
        elif page == "About Us":
            about_page()
        elif page == "Book Slot":
            book_slot_page()
        elif page == "Credits":
            credits_page()
        elif page == "Manure":
            manure_page()
        elif page == "Admin Dashboard":
            admin_page()

if __name__ == "__main__":
    main()