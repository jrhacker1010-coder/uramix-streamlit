import streamlit as st
import matplotlib.pyplot as plt
import datetime
import random
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(
    page_title="URAMix - Waste to Value",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for green and white theme
st.markdown("""
<style>
    .main {
        background-color: #f0f8f0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .problem-statement {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        animation: fadeIn 1.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .tagline {
        font-size: 28px;
        color: #2e7d32;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .eco-quote {
        background-color: #e8f5e9;
        padding: 20px;
        border-left: 5px solid #4CAF50;
        border-radius: 5px;
        margin: 20px 0;
        font-size: 18px;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'users' not in st.session_state:
        st.session_state.users = {}
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'waste_bookings' not in st.session_state:
        st.session_state.waste_bookings = []
    if 'manure_stock' not in st.session_state:
        st.session_state.manure_stock = 1000  # kg
    if 'manure_price' not in st.session_state:
        st.session_state.manure_price = 15  # rupees per kg
    if 'feedback_list' not in st.session_state:
        st.session_state.feedback_list = []
    if 'daily_credits' not in st.session_state:
        st.session_state.daily_credits = []
    if 'qr_codes' not in st.session_state:
        st.session_state.qr_codes = {}

init_session_state()

# Helper functions
def generate_qr_code(booking_id, credits):
    """Generate a simple QR code image"""
    img = Image.new('RGB', (300, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw QR-like pattern (simplified)
    for i in range(10):
        for j in range(10):
            if random.random() > 0.5:
                draw.rectangle([i*30, j*30, (i+1)*30, (j+1)*30], fill='black')
    
    # Add text
    try:
        draw.text((150, 270), f"ID: {booking_id}", fill='black', anchor='mm')
    except:
        draw.text((80, 270), f"ID: {booking_id}", fill='black')
    
    return img

def calculate_credits(waste_type, quantity):
    """Calculate credits based on waste type and quantity"""
    if waste_type == "Organic":
        return quantity * 10  # 10 credits per kg
    else:  # Inorganic
        return quantity * 6  # 6 credits per kg

def send_feedback_email(user_email, feedback_text):
    """Mock email sending function"""
    # In production, use actual SMTP credentials
    try:
        # This is a mock function - actual email sending would require SMTP setup
        st.session_state.feedback_list.append({
            'email': user_email,
            'feedback': feedback_text,
            'timestamp': datetime.datetime.now()
        })
        return True
    except:
        return False

# Authentication functions
def login_user(email, password):
    """Login user with email and password"""
    # Check admin login
    if email == "admin" and password == "12345":
        st.session_state.logged_in = True
        st.session_state.is_admin = True
        st.session_state.current_user = "admin"
        return True
    
    # Check regular user login
    if email in st.session_state.users:
        if st.session_state.users[email]['password'] == password:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.current_user = email
            return True
    return False

def signup_user(email, password):
    """Sign up new user"""
    if email in st.session_state.users:
        return False
    
    st.session_state.users[email] = {
        'password': password,
        'credits': 20,  # Referral bonus
        'wallet_rupees': 0,
        'bookings': [],
        'transactions': []
    }
    return True

def logout_user():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.is_admin = False

# Page functions
def login_page():
    """Login and signup page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and tagline
        st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🌱 URAMix</h1>", unsafe_allow_html=True)
        st.markdown("<p class='tagline'>♻️ WASTE TO VALUE ♻️</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Login", use_container_width=True):
                    if login_user(email, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            with col_b:
                if st.button("Sign in with Google (Demo)", use_container_width=True):
                    # Mock Google login
                    demo_email = "demo@google.com"
                    if demo_email not in st.session_state.users:
                        st.session_state.users[demo_email] = {
                            'password': 'demo',
                            'credits': 20,
                            'wallet_rupees': 0,
                            'bookings': [],
                            'transactions': []
                        }
                    login_user(demo_email, 'demo')
                    st.success("Logged in with Google!")
                    st.rerun()
        
        with tab2:
            st.subheader("Create New Account")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Sign Up", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif signup_user(new_email, new_password):
                    st.success("Account created! You received 20 referral credits!")
                    st.info("Please login with your credentials")
                else:
                    st.error("Email already exists")

def home_page():
    """Home page with eco-friendly design"""
    # Header with logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🌱 URAMix</h1>", unsafe_allow_html=True)
        st.markdown("<p class='tagline'>♻️ WASTE TO VALUE ♻️</p>", unsafe_allow_html=True)
    
    # Eco-quote with dynamic percentage
    user_data = st.session_state.users.get(st.session_state.current_user, {})
    credits = user_data.get('credits', 0)
    reduction_percentage = round(credits * 0.05, 2)  # Mock calculation
    
    st.markdown(f"""
    <div class='eco-quote'>
        🌍 You helped reduce landfill emissions by {reduction_percentage}% today! 
        Your eco-credits increased! 🌱
    </div>
    """, unsafe_allow_html=True)
    
    # Dustbin and manure visualization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 🗑️ Waste Collection")
        st.write("Turn your waste into credits!")
        st.metric("Total Bookings", len(user_data.get('bookings', [])))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 💰 Your Wallet")
        st.metric("Credits", user_data.get('credits', 0))
        st.metric("Balance (₹)", user_data.get('wallet_rupees', 0))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 🌾 Natural Manure")
        st.write("Buy affordable organic manure!")
        st.metric("Price per kg", f"₹{st.session_state.manure_price}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Problem statement section
    st.markdown("""
    <div class='problem-statement'>
        <h2 style='text-align: center; margin-bottom: 20px;'>💡 The Problem We Solve</h2>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
            <div>
                <h3>🚮 Waste Management Issues</h3>
                <ul>
                    <li>People dump waste early - can't wait for bins to fill</li>
                    <li>Irregular garbage collection schedules</li>
                    <li>No incentive for waste segregation</li>
                    <li>Increasing landfill emissions</li>
                </ul>
            </div>
            <div>
                <h3>🌾 Farming Challenges</h3>
                <ul>
                    <li>Natural manure is expensive for farmers</li>
                    <li>Chemical fertilizers harm soil health</li>
                    <li>Need for affordable organic alternatives</li>
                    <li>Circular economy opportunities missed</li>
                </ul>
            </div>
        </div>
        <h3 style='text-align: center; margin-top: 30px; font-size: 24px;'>
            ✨ URAMix creates a circular economy: Waste → Credits → Affordable Manure 🌱
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("---")
    st.subheader("📊 Platform Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = len(st.session_state.users)
    total_bookings = len(st.session_state.waste_bookings)
    total_credits = sum([u.get('credits', 0) for u in st.session_state.users.values()])
    
    col1.metric("👥 Total Users", total_users)
    col2.metric("📦 Waste Collections", total_bookings)
    col3.metric("⭐ Total Credits Issued", total_credits)
    col4.metric("🌾 Manure Stock (kg)", st.session_state.manure_stock)

def waste_submission_page():
    """Waste submission page for users"""
    st.title("🗑️ Submit Waste for Credits")
    
    user_data = st.session_state.users[st.session_state.current_user]
    
    # Display current credits
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💳 Your Credits", user_data['credits'])
    with col2:
        st.metric("💰 Wallet Balance", f"₹{user_data['wallet_rupees']}")
    
    st.markdown("---")
    
    # Waste submission form
    st.subheader("📝 Book Waste Collection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        waste_type = st.selectbox(
            "Select Waste Type",
            ["Organic", "Inorganic"],
            help="Organic waste earns more credits!"
        )
        
        estimated_quantity = st.number_input(
            "Estimated Quantity (kg)",
            min_value=1,
            max_value=100,
            value=5
        )
    
    with col2:
        st.info(f"""
        **Credit Rates:**
        - 🌿 Organic: 10 credits/kg
        - ♻️ Inorganic: 6 credits/kg
        
        **Estimated Credits:** {calculate_credits(waste_type, estimated_quantity)}
        """)
    
    address = st.text_area("Pickup Address")
    
    if st.button("📤 Submit Booking", use_container_width=True):
        if address:
            booking_id = f"WB{len(st.session_state.waste_bookings) + 1:04d}"
            booking = {
                'booking_id': booking_id,
                'user': st.session_state.current_user,
                'waste_type': waste_type,
                'estimated_quantity': estimated_quantity,
                'address': address,
                'status': 'Pending',
                'timestamp': datetime.datetime.now(),
                'actual_quantity': None,
                'credits_earned': None
            }
            st.session_state.waste_bookings.append(booking)
            user_data['bookings'].append(booking_id)
            
            st.success(f"✅ Booking submitted! Booking ID: {booking_id}")
            st.info("Admin will verify and generate QR code. You can scan it to earn credits!")
        else:
            st.error("Please provide pickup address")
    
    # Show user's bookings
    st.markdown("---")
    st.subheader("📋 Your Bookings")
    
    user_bookings = [b for b in st.session_state.waste_bookings 
                     if b['user'] == st.session_state.current_user]
    
    if user_bookings:
        for booking in reversed(user_bookings):
            with st.expander(f"🎫 {booking['booking_id']} - {booking['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Type:** {booking['waste_type']}")
                    st.write(f"**Quantity:** {booking['estimated_quantity']} kg")
                    st.write(f"**Status:** {booking['status']}")
                with col2:
                    st.write(f"**Date:** {booking['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                    if booking['credits_earned']:
                        st.write(f"**Credits Earned:** {booking['credits_earned']} ⭐")
                
                # Show QR if approved
                if booking['status'] == 'Approved' and booking['booking_id'] in st.session_state.qr_codes:
                    st.image(st.session_state.qr_codes[booking['booking_id']], width=200)
                    
                    if st.button(f"Scan QR & Claim Credits", key=f"scan_{booking['booking_id']}"):
                        if booking['status'] == 'Approved' and booking['credits_earned']:
                            user_data['credits'] += booking['credits_earned']
                            booking['status'] = 'Completed'
                            st.success(f"🎉 {booking['credits_earned']} credits added to your wallet!")
                            st.rerun()
    else:
        st.info("No bookings yet. Submit your first waste collection!")

def wallet_page():
    """Wallet and withdrawal page"""
    st.title("💰 Wallet & Withdrawals")
    
    user_data = st.session_state.users[st.session_state.current_user]
    
    # Display wallet info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("⭐ Total Credits", user_data['credits'])
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("💵 Wallet Balance", f"₹{user_data['wallet_rupees']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        withdrawal_available = user_data['credits'] >= 500
        st.metric("🎯 Withdrawal Status", "Available" if withdrawal_available else "Locked")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Withdrawal section
    st.subheader("💸 Convert Credits to Money")
    
    if user_data['credits'] >= 500:
        st.success("✅ You can withdraw money now!")
        
        credits_to_convert = st.number_input(
            "Credits to Convert (Min 500)",
            min_value=500,
            max_value=user_data['credits'],
            step=100,
            value=500
        )
        
        conversion_rate = 0.5  # 1 credit = ₹0.50
        money_equivalent = credits_to_convert * conversion_rate
        
        st.info(f"💵 You will receive: ₹{money_equivalent}")
        
        if st.button("💰 Withdraw to Bank", use_container_width=True):
            user_data['credits'] -= credits_to_convert
            user_data['wallet_rupees'] += money_equivalent
            
            transaction = {
                'type': 'Withdrawal',
                'credits': credits_to_convert,
                'amount': money_equivalent,
                'timestamp': datetime.datetime.now()
            }
            user_data['transactions'].append(transaction)
            
            st.success(f"✅ ₹{money_equivalent} added to your wallet!")
            st.balloons()
            st.rerun()
    else:
        remaining = 500 - user_data['credits']
        st.warning(f"⚠️ You need {remaining} more credits to withdraw money")
        st.progress(user_data['credits'] / 500)
    
    # Transaction history
    st.markdown("---")
    st.subheader("📜 Transaction History")
    
    if user_data['transactions']:
        for trans in reversed(user_data['transactions']):
            with st.expander(f"{trans['type']} - {trans['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                st.write(f"**Credits:** {trans['credits']}")
                st.write(f"**Amount:** ₹{trans['amount']}")
    else:
        st.info("No transactions yet")

def manure_page():
    """Manure marketplace page"""
    st.title("🌾 Natural Manure Marketplace")
    
    user_data = st.session_state.users[st.session_state.current_user]
    
    # Display manure info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Available Stock", f"{st.session_state.manure_stock} kg")
    with col2:
        st.metric("💰 Price per kg", f"₹{st.session_state.manure_price}")
    with col3:
        st.metric("💵 Your Wallet", f"₹{user_data['wallet_rupees']}")
    
    st.markdown("---")
    
    # Purchase section
    st.subheader("🛒 Buy Natural Manure")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        quantity_to_buy = st.number_input(
            "Quantity (kg)",
            min_value=1,
            max_value=min(100, st.session_state.manure_stock),
            value=10
        )
        
        total_cost = quantity_to_buy * st.session_state.manure_price
        
        st.info(f"""
        **Order Summary:**
        - Quantity: {quantity_to_buy} kg
        - Rate: ₹{st.session_state.manure_price}/kg
        - Total: ₹{total_cost}
        """)
        
        delivery_address = st.text_area("Delivery Address")
        
        if st.button("🛍️ Buy Now (Demo)", use_container_width=True):
            if delivery_address:
                if user_data['wallet_rupees'] >= total_cost:
                    user_data['wallet_rupees'] -= total_cost
                    st.session_state.manure_stock -= quantity_to_buy
                    
                    st.success(f"✅ Order placed! {quantity_to_buy} kg manure will be delivered soon!")
                    st.balloons()
                else:
                    st.error("Insufficient balance. Convert more credits to money!")
            else:
                st.error("Please provide delivery address")
    
    with col2:
        st.markdown("""
        ### ✨ Benefits
        - 🌱 100% Organic
        - 💪 Improves soil health
        - 🌾 Higher crop yield
        - ♻️ Eco-friendly
        - 💰 Affordable pricing
        """)
    
    # Info section
    st.markdown("---")
    st.subheader("📚 Why Natural Manure?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Environmental Benefits:**
        - Reduces chemical pollution
        - Improves soil microbiome
        - Sustainable farming
        - Reduces carbon footprint
        """)
    
    with col2:
        st.markdown("""
        **Economic Benefits:**
        - Cost-effective solution
        - Long-term soil fertility
        - Better crop quality
        - Supports Clean India mission
        """)

def feedback_page():
    """User feedback page"""
    st.title("📝 Feedback & Support")
    
    st.write("We value your feedback! Help us improve URAMix.")
    
    feedback_text = st.text_area(
        "Share your thoughts, suggestions, or report issues:",
        height=200,
        placeholder="Tell us about your experience with URAMix..."
    )
    
    rating = st.slider("Rate your experience", 1, 5, 5)
    
    if st.button("📤 Submit Feedback", use_container_width=True):
        if feedback_text:
            feedback = {
                'email': st.session_state.current_user,
                'feedback': feedback_text,
                'rating': rating,
                'timestamp': datetime.datetime.now()
            }
            st.session_state.feedback_list.append(feedback)
            
            # Mock email sending
            send_feedback_email(st.session_state.current_user, feedback_text)
            
            st.success("✅ Thank you for your feedback! Admin will review it soon.")
            st.balloons()
        else:
            st.error("Please enter your feedback")
    
    st.markdown("---")
    
    # Contact info
    st.subheader("📞 Contact Us")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Email:** support@uramix.com
        
        **Phone:** +91-XXXX-XXXXXX
        """)
    
    with col2:
        st.info("""
        **Address:** Clean India Initiative
        
        **Working Hours:** 24/7
        """)

def admin_dashboard():
    """Admin dashboard page"""
    st.title("👨‍💼 Admin Dashboard")
    
    # Overview metrics
    st.subheader("📊 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = len(st.session_state.users)
    total_bookings = len(st.session_state.waste_bookings)
    pending_bookings = len([b for b in st.session_state.waste_bookings if b['status'] == 'Pending'])
    total_credits = sum([u.get('credits', 0) for u in st.session_state.users.values()])
    
    col1.metric("👥 Total Users", total_users)
    col2.metric("📦 Total Bookings", total_bookings)
    col3.metric("⏳ Pending Bookings", pending_bookings)
    col4.metric("⭐ Credits Issued", total_credits)
    
    st.markdown("---")
    
    # Tabs for different admin functions
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Manage Bookings", "📈 Analytics", "🌾 Manure Management", "💬 Feedback"])
    
    with tab1:
        st.subheader("Waste Collection Bookings")
        
        pending_bookings = [b for b in st.session_state.waste_bookings if b['status'] == 'Pending']
        
        if pending_bookings:
            for booking in pending_bookings:
                with st.expander(f"🎫 {booking['booking_id']} - {booking['waste_type']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**User:** {booking['user']}")
                        st.write(f"**Type:** {booking['waste_type']}")
                        st.write(f"**Estimated:** {booking['estimated_quantity']} kg")
                        st.write(f"**Address:** {booking['address']}")
                    
                    with col2:
                        actual_quantity = st.number_input(
                            "Actual Quantity (kg)",
                            min_value=1,
                            max_value=100,
                            value=booking['estimated_quantity'],
                            key=f"qty_{booking['booking_id']}"
                        )
                        
                        credits = calculate_credits(booking['waste_type'], actual_quantity)
                        st.info(f"Credits to award: {credits}")
                        
                        if st.button(f"✅ Approve & Generate QR", key=f"approve_{booking['booking_id']}"):
                            booking['status'] = 'Approved'
                            booking['actual_quantity'] = actual_quantity
                            booking['credits_earned'] = credits
                            
                            # Generate QR code
                            qr_img = generate_qr_code(booking['booking_id'], credits)
                            st.session_state.qr_codes[booking['booking_id']] = qr_img
                            
                            # Add to daily credits
                            st.session_state.daily_credits.append({
                                'date': datetime.datetime.now(),
                                'credits': credits
                            })
                            
                            st.success("✅ Booking approved! QR generated!")
                            st.rerun()
        else:
            st.info("No pending bookings")
        
        # Show approved bookings
        st.markdown("---")
        st.subheader("Approved Bookings")
        
        approved_bookings = [b for b in st.session_state.waste_bookings if b['status'] == 'Approved']
        
        if approved_bookings:
            for booking in approved_bookings:
                with st.expander(f"✅ {booking['booking_id']} - {booking['waste_type']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**User:** {booking['user']}")
                        st.write(f"**Credits:** {booking['credits_earned']}")
                    with col2:
                        if booking['booking_id'] in st.session_state.qr_codes:
                            st.image(st.session_state.qr_codes[booking['booking_id']], width=150)
        else:
            st.info("No approved bookings yet")
    
    with tab2:
        st.subheader("📈 Platform Analytics")
        
        # Credits issued over time
        if st.session_state.daily_credits:
            fig, ax = plt.subplots(figsize=(10, 5))
            dates = [c['date'].strftime('%Y-%m-%d') for c in st.session_state.daily_credits[-10:]]
            credits = [c['credits'] for c in st.session_state.daily_credits[-10:]]
            
            ax.bar(dates, credits, color='#4CAF50')
            ax.set_xlabel('Date')
            ax.set_ylabel('Credits Issued')
            ax.set_title('Daily Credits Distribution')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No data available yet")
        
        # Waste type distribution
        organic_count = len([b for b in st.session_state.waste_bookings if b['waste_type'] == 'Organic'])
        inorganic_count = len([b for b in st.session_state.waste_bookings if b['waste_type'] == 'Inorganic'])
        
        if organic_count + inorganic_count > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie([organic_count, inorganic_count], 
                   labels=['Organic', 'Inorganic'],
                   colors=['#8BC34A', '#FFC107'],
                   autopct='%1.1f%%',
                   startangle=90)
            ax.set_title('Waste Type Distribution')
            st.pyplot(fig)
    
    with tab3:
        st.subheader("🌾 Manure Stock Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current Stock", f"{st.session_state.manure_stock} kg")
            
            new_stock = st.number_input("Add Stock (kg)", min_value=0, max_value=5000, value=100)
            if st.button("➕ Add Stock"):
                st.session_state.manure_stock += new_stock
                st.success(f"Added {new_stock} kg to stock!")
                st.rerun()
        
        with col2:
            st.metric("Current Price", f"₹{st.session_state.manure_price}/kg")
            
            new_price = st.number_input("Update Price (₹/kg)", min_value=5, max_value=100, value=st.session_state.manure_price)
            if st.button("💰 Update Price"):
                st.session_state.manure_price = new_price
                st.success(f"Price updated to ₹{new_price}/kg!")
                st.rerun()
    
    with tab4:
        st.subheader("💬 User Feedback")
        
        if st.session_state.feedback_list:
            for feedback in reversed(st.session_state.feedback_list):
                with st.expander(f"📧 {feedback['email']} - {feedback['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**Rating:** {'⭐' * feedback.get('rating', 5)}")
                    st.write(f"**Feedback:** {feedback['feedback']}")
        else:
            st.info("No feedback received yet")

# Main app logic
def main():
    """Main application controller"""
    
    # Show login page if not logged in
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🌱 URAMix")
        st.markdown("**Waste to Value**")
        st.markdown("---")
        
        if st.session_state.is_admin:
            st.markdown("### Admin Panel")
            page = st.radio(
                "Navigation",
                ["Dashboard"],
                label_visibility="collapsed"
            )
        else:
            user_data = st.session_state.users[st.session_state.current_user]
            st.markdown(f"**User:** {st.session_state.current_user}")
            st.metric("Credits", user_data['credits'])
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                ["🏠 Home", "🗑️ Submit Waste", "💰 Wallet", "🌾 Manure Shop", "📝 Feedback"],
                label_visibility="collapsed"
            )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px;'>
            <p>🌍 Clean India Initiative</p>
            <p>♻️ Building a Sustainable Future</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if st.session_state.is_admin:
        admin_dashboard()
    else:
        if page == "🏠 Home":
            home_page()
        elif page == "🗑️ Submit Waste":
            waste_submission_page()
        elif page == "💰 Wallet":
            wallet_page()
        elif page == "🌾 Manure Shop":
            manure_page()
        elif page == "📝 Feedback":
            feedback_page()

# Run the app
if __name__ == "__main__":
    main()
