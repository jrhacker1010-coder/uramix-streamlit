# 🌱 URAMix - Waste to Value

## India's Reward-Based Waste Management Platform

URAMix is a revolutionary circular economy platform designed to solve India's waste management crisis while making natural manure affordable for farmers.

---

## 🌍 Project Ideology & Mission

### Core Mission
- 🇮🇳 **Make India Clean** - Support Swachh Bharat Mission
- 🗑️ **Reduce Landfills** - Combat India's biggest waste problem
- ♻️ **Encourage Segregation** - Reward proper waste management
- 🌾 **Affordable Manure** - Convert waste into natural fertilizer
- 💰 **Reward Users** - Earn credits and real money

### The Circular Economy
```
Waste Segregation → Credits → Money → Affordable Manure → Sustainable Farming
```

---

## 💡 Real-World Problems We Solve

### 🚮 Waste Management Crisis
1. **Early Dumping** - People dump waste early because bins fill before collection
2. **Irregular Collection** - Inconsistent garbage pickup schedules
3. **No Incentives** - Zero motivation for proper waste segregation
4. **Overflowing Landfills** - Urban areas struggling with waste accumulation

### 🌾 Farming Challenges
1. **Expensive Manure** - Natural manure is costly and unaffordable for small farmers
2. **Market Competition** - Small farmers can't compete with big manure companies
3. **Soil Degradation** - Chemical fertilizers harming long-term soil health
4. **Lack of Alternatives** - Limited access to affordable organic options

---

## ✨ Key Features

### For Users

#### 🎁 Credit System
- **Organic Waste**: 150 credits per submission
- **Inorganic Waste**: 100 credits per submission
- **Referral Bonus**: 20 credits on signup
- **Note**: Credits based on waste TYPE, not quantity

#### 💳 Credit-to-Money Conversion
- **1 credit = ₹0.05**
- **20 credits = ₹1**
- **Minimum withdrawal**: 500 credits (₹25)

#### 🛒 Flipkart-Style Manure Store
- Product cards with images
- Multiple manure types
- Quantity selection
- Buy with wallet credits
- Track URAM Count (manure purchased)

#### 📱 Seamless Process
1. Submit waste (Organic/Inorganic)
2. Admin verifies and generates QR
3. Scan QR to claim credits
4. Accumulate 500+ credits
5. Withdraw money or buy manure

### For Admins

#### 📊 Dashboard Controls
- View all platform metrics
- Total users and bookings
- Credits issued tracking
- Pending verification queue

#### ✅ Waste Management
- Verify waste submissions
- Enter verified quantity
- Generate QR codes
- Approve/reject bookings

#### 🌾 Manure Management
- Manage URAM Count (stock)
- Set price per kg
- Track sales analytics
- Revenue monitoring

#### 📈 Analytics
- Daily credits distribution
- Waste type charts
- Manure sales trends
- User feedback review

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

```bash
# 1. Clone/download the repository
git clone <repository-url>
cd uramix

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py

# 4. Open in browser
# http://localhost:8501
```

---

## 👥 User Guide

### Creating Account

1. Go to **Sign Up** tab
2. Enter email and password (6+ characters)
3. Click "Create Account"
4. **Receive 20 referral credits instantly!**

### Alternative: Google Demo Login
- Click "Google Sign-In (Demo)" button
- Instant demo account creation

### Submitting Waste

1. Navigate to **♻️ Submit Waste**
2. Select waste type:
   - **Organic** → 150 credits
   - **Inorganic** → 100 credits
3. Enter pickup address and phone
4. Submit booking request
5. Wait for admin verification

### Claiming Credits

1. Admin verifies waste and generates QR
2. Check "Your Bookings" section
3. Find approved booking
4. Click "📱 Scan & Claim Credits"
5. **Credits added instantly!**

### Withdrawing Money

1. Accumulate **500+ credits** (₹25)
2. Go to **💰 Wallet**
3. Enter credits to withdraw
4. Provide bank details
5. Confirm withdrawal

### Buying Manure

1. Visit **🛒 Manure Store**
2. Browse Flipkart-style product cards:
   - Organic Manure
   - Premium Compost
   - Vermicompost
3. Select quantity
4. Click "🛍️ Buy Now"
5. **URAM Count increases!**

---

## 🔐 Admin Access

### Login Credentials
```
Username: admin
Password: 12345
```

### Admin Capabilities

#### Booking Management
1. View pending waste submissions
2. Enter verified quantity
3. Generate QR codes
4. Approve bookings

#### Stock Management
1. View current URAM Count
2. Add new stock
3. Update pricing
4. Monitor sales

#### Analytics Dashboard
- Daily credits chart
- Waste distribution pie chart
- Manure sales trends
- Total platform statistics

#### Feedback Review
- Read user feedback
- View ratings
- Mark as reviewed
- Respond to concerns

---

## 🛠️ Technical Architecture

### Frontend
- **Streamlit** - Web interface
- **Custom CSS** - Green & white theme
- **Responsive Design** - Mobile-friendly

### Backend
- **Session State** - In-memory database
- **Python Dictionaries** - Data storage
- **No External DB** - Fully self-contained

### Features
- **QR Generation** - qrcode library
- **Charts** - Matplotlib visualizations
- **Image Handling** - Pillow (PIL)
- **Data Analysis** - Pandas DataFrames

---

## 📊 Credit & Money Logic

### Earning Credits

| Waste Type | Credits | Rupee Value |
|-----------|---------|-------------|
| Organic | 150 | ₹7.50 |
| Inorganic | 100 | ₹5.00 |
| Referral Bonus | 20 | ₹1.00 |

### Conversion Rates
- **Credits → Rupees**: Multiply by 0.05
  - Example: 1000 credits = ₹50
- **Rupees → Credits**: Multiply by 20
  - Example: ₹10 = 200 credits

### Withdrawal Rules
- **Minimum**: 500 credits (₹25)
- **Maximum**: No limit
- **Frequency**: Unlimited withdrawals

---

## 🌾 Manure Marketplace

### Product Catalog

1. **🌿 Organic Manure**
   - Base price: ₹12/kg
   - Standard quality
   - Large availability

2. **🌾 Premium Compost**
   - Price: ₹15/kg
   - High-grade quality
   - 60% of stock

3. **🪱 Vermicompost**
   - Price: ₹17/kg
   - Earthworm-processed
   - 40% of stock

### Purchase Process
1. Check wallet balance
2. Select product and quantity
3. View total cost
4. Confirm purchase
5. Credits deducted automatically
6. URAM Count updated

---

## 📝 Feedback System

### User Side
- Text area for detailed feedback
- 1-5 star rating system
- Submit button

### Admin Side
- View all feedback chronologically
- See user email and timestamp
- Read ratings and comments
- Mark as reviewed

### Email Integration (Mock)
```python
# Production SMTP example:
import smtplib
from email.mime.text import MIMEText

sender = "uramix@gmail.com"
recipient = "admin@uramix.com"
msg = MIMEText(feedback_text)
msg['Subject'] = f'Feedback from {user_email}'
msg['From'] = sender
msg['To'] = recipient

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, 'app_password')
    smtp.send_message(msg)
```

---

## 🎨 UI/UX Design

### Theme
- **Primary Color**: Green (#4CAF50)
- **Secondary**: White (#FFFFFF)
- **Accent**: Gold (#FFC107)
- **Style**: Clean, modern, eco-friendly

### Components
- ✅ Animated problem statement cards
- ✅ Gradient hero sections
- ✅ Metric cards with hover effects
- ✅ Flipkart-style product cards
- ✅ Progress bars and charts
- ✅ Responsive sidebar navigation

### Animations
- Fade-in effects
- Slide-in transitions
- Hover transformations
- Smooth color gradients

---

## 📈 Analytics & Charts

### Admin Dashboard Charts

1. **Daily Credits Distribution**
   - Bar chart showing credits issued per day
   - Green gradient bars
   - Date-wise breakdown

2. **Waste Type Distribution**
   - Pie chart: Organic vs Inorganic
   - Percentage breakdown
   - Color-coded segments

3. **Manure Sales Trend**
   - Line chart: Cumulative sales
   - Quantity over transactions
   - Growth visualization

---

## 🌟 User Journey

### New User
```
1. Sign Up → Get 20 credits
2. Explore home page
3. Read problem statements
4. Submit first waste
5. Wait for verification
6. Scan QR, earn credits
7. Repeat and accumulate
8. Reach 500 credits
9. Withdraw or shop
```

### Returning User
```
1. Login
2. Check wallet balance
3. View URAM Count
4. Submit more waste
5. Buy manure
6. Provide feedback
7. Track progress
```

---

## 🔒 Security Features

- Password-based authentication
- Session state management
- Unique email IDs
- Admin-only access controls
- Secure QR code generation
- Transaction logging

---

## 🚀 Deployment

### Streamlit Community Cloud

1. **Prepare Repository**
   ```bash
   git add app.py requirements.txt README.md
   git commit -m "URAMix application"
   git push origin main
   ```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repository
   - Select main branch
   - Choose app.py as main file
   - Click Deploy

3. **Environment**
   - No environment variables needed
   - All dependencies in requirements.txt
   - Ready to use immediately

---

## 📱 Platform Statistics

Track these metrics on home page:
- 👥 Total registered users
- ♻️ Total waste collections
- ⭐ Total credits issued
- 🌾 Current manure stock

---

## 🎯 Future Enhancements

- 📍 GPS-based waste pickup
- 🤖 AI waste classification
- 📱 Native mobile app
- 💳 Payment gateway integration
- 🏆 Leaderboards and gamification
- 🤝 Municipal partnerships
- 🌐 Multi-language support
- 📊 Advanced analytics dashboard

---

## 🤝 Contributing

This is a hackathon-ready project. Feel free to:
- Report bugs via issues
- Suggest new features
- Improve documentation
- Enhance UI/UX
- Add functionality

---

## 📧 Support & Contact

**Email**: support@uramix.com  
**Phone**: +91-8438386610
**Hours**: 24/7 Support  
**Address**: Clean India Initiative, New Delhi

---

## 📜 License & Credits

### Project
URAMix - Waste to Value Platform

### Purpose
- Support Swachh Bharat Mission
- Promote circular economy
- Empower farmers
- Reduce environmental impact

### Acknowledgments
- Clean India Initiative
- Sustainable farming communities
- Environmental activists
- All contributing users

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Full-stack Streamlit development
- ✅ Session state management
- ✅ QR code generation
- ✅ Data visualization
- ✅ User authentication
- ✅ E-commerce functionality
- ✅ Admin dashboard creation
- ✅ Feedback systems

---

## 🌱 Impact Goals

### Environmental
- ♻️ Reduce landfill waste by 30%
- 🌍 Lower methane emissions
- 🌿 Promote organic farming
- 💚 Increase recycling rates

### Social
- 👥 Engage 10,000+ users
- 🤝 Support small farmers
- 📚 Educate on waste segregation
- 🏆 Build eco-conscious community

### Economic
- 💰 Generate income for users
- 🌾 Reduce farming costs
- 💼 Create green jobs
- 📈 Build sustainable model

---

## 🏆 Why URAMix?

### Problem-Solution Fit
- ✅ Addresses real waste crisis
- ✅ Rewards positive behavior
- ✅ Helps farming community
- ✅ Creates circular economy

### User Benefits
- 💰 Earn real money
- 🎁 Referral bonuses
- 🛒 Affordable shopping
- 🌍 Environmental impact

### Scalability
- 🌏 Pan-India deployment
- 📱 Mobile-ready
- 🔌 Easy integration
- 💡 Proven model

---

**Built with 💚 for a cleaner, greener India**

**URAMix - Where Waste Becomes Value** 🌱♻️

---

## 📞 Quick Links

- 🏠 [Home](#uramix---waste-to-value)
- 🚀 [Getting Started](#getting-started)
- 👥 [User Guide](#user-guide)
- 🔐 [Admin Access](#admin-access)
- 📊 [Analytics](#analytics--charts)
- 🌟 [Future Plans](#future-enhancements)

---


