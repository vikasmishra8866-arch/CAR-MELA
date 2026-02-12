import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import datetime
import io
import pytz 
import qrcode 

# --- CONFIGURATION (PAYMENT DETAILS) ---
MY_UPI_ID = "9696159863@ibl" 
MY_WHATSAPP = "919696159863" 
SECRET_ACCESS_KEY = "CAR786"  # Updated Key

# --- VALIDITY LOGIC (5 DAYS) ---
# Setting the activation start date
START_DATE = datetime.date(2026, 2, 12) 
EXPIRY_DATE = START_DATE + datetime.timedelta(days=5)

# --- INDIAN TIME SETTING ---
IST = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(IST)
current_time = now.strftime("%d-%m-%Y %I:%M %p")
today_date = now.date()

# Page Setup
st.set_page_config(page_title="CAR MELA", page_icon="🚗", layout="centered")

# Custom CSS for Small Boxes and Centering
st.markdown("""
    <style>
    /* Main container width control */
    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
    }
    /* Input box size control */
    .stTextInput input, .stNumberInput input {
        height: 35px !important;
    }
    /* Label font size */
    .stMarkdown p {
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Session State for Payment Lock
if 'paid' not in st.session_state:
    st.session_state['paid'] = False

# --- 1. PAYMENT LOCK SCREEN ---
if not st.session_state['paid']:
    st.markdown("<h1 style='text-align: center;'>🚗 CAR MELA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>🔐 Premium Portal Access</h3>", unsafe_allow_html=True)
    
    # Check if Key is already expired
    if today_date > EXPIRY_DATE:
        st.error(f"🚨 Ye Access Key ({SECRET_ACCESS_KEY}) Expire ho chuki hai! Kripya naye subscription ke liye contact karein.")
    else:
        st.error("Aapka Access expired hai ya aap naye user hain. Kripya payment karein.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.info("💰 **Subscription Amount: ₹499 / Month**")
        upi_url = f"upi://pay?pa={MY_UPI_ID}&pn=CAR%20MELA&am=499&cu=INR"
        pay_qr = qrcode.make(upi_url)
        pay_buf = io.BytesIO()
        pay_qr.save(pay_buf, format='PNG')
        st.image(pay_buf, caption="Scan and Pay ₹499 to Unlock", width=200)

    with col_b:
        st.subheader("Activation Steps:")
        st.write("1️⃣ QR Scan karke ₹499 pay karein.")
        st.write("2️⃣ Screenshot WhatsApp par bhejein.")
        
        msg = "Sir, maine CAR MELA app ke liye ₹499 pay kar diye hain. Please mujhe Access Key bhej dijiye."
        wa_url = f"https://wa.me/{MY_WHATSAPP}?text={msg.replace(' ', '%20')}"
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%;">
                    ✅ WhatsApp Screenshot
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        key_input = st.text_input("Enter Access Key", type="password", placeholder="Yahan Key bharein...")
        
        if st.button("Unlock Calculator Now 🚀"):
            if today_date > EXPIRY_DATE:
                st.error("Access Denied: Key has Expired!")
            elif key_input == SECRET_ACCESS_KEY:
                st.session_state['paid'] = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Galat Key!")

# --- 2. MAIN APP CONTENT (Unlocked) ---
else:
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        h1 { color: #1e3d59 !important; text-align: center; }
        .whatsapp-btn {
            position: fixed; bottom: 20px; right: 20px; background-color: #25d366;
            color: white !important; border-radius: 50px; padding: 12px 20px;
            font-weight: bold; text-decoration: none; z-index: 1000;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 10px;
        }
        </style>
        <a href="https://wa.me/919696159863" class="whatsapp-btn" target="_blank"><span>💬 WhatsApp</span></a>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.success("✅ Premium Active")
        st.info("🚗 CAR MELA Dashboard")
        st.write(f"Key Expires on: {EXPIRY_DATE.strftime('%d-%m-%Y')}")
        if st.button("Logout"):
            st.session_state['paid'] = False
            st.rerun()

    st.title("🚗 CAR MELA")
    st.markdown(f"<div style='text-align:center;'><b>Managed by: Vikas Mishra</b></div>", unsafe_allow_html=True) 
    st.write(f"<div style='text-align:center; font-size:12px;'>📅 {current_time}</div>", unsafe_allow_html=True)

    st.markdown("---")
    service_mode = st.radio("Select Quotation Type", ["Vehicle Purchase", "Loan on Vehicle"], horizontal=True)

    cust_name = st.text_input("Customer Name", placeholder="e.g. CAR MELA")
    veh_name = st.text_input("Vehicle Name", placeholder="e.g. TOYOTA FORTUNER")

    col1, col2 = st.columns(2)

    if service_mode == "Vehicle Purchase":
        with col1:
            price = st.number_input("Vehicle Price (Rs)", value=None, placeholder="Enter Price...")
            down = st.number_input("Down Payment (Rs)", value=None, placeholder="Enter Down Payment...")
            file_charges = st.number_input("File Charges (Rs)", value=None, placeholder="Enter File Charges...")
        with col2:
            other_charges = st.number_input("Other Charges (Rs)", value=None, placeholder="Enter Other Charges...")
            int_type = st.radio("Interest Type", ["Flat Rate", "Reducing Balance"], horizontal=True)
            roi = st.number_input(f"{int_type} (%)", value=18.0) 
        
        loan_amt = (price or 0) - (down or 0) + (file_charges or 0) + (other_charges or 0)
        pdf_labels = [("Vehicle Price", price or 0), ("Down Payment", down or 0), ("File Charges", file_charges or 0), ("Other Charges", other_charges or 0)]
    else: 
        with col1:
            l_amt = st.number_input("Loan Amount (Rs)", value=None, placeholder="Enter Loan Amt...")
            ins_ch = st.number_input("Insurance Charge (Rs)", value=None, placeholder="0.0")
            pass_ch = st.number_input("Passing Charge (Rs)", value=None, placeholder="0.0")
            trans_ch = st.number_input("Transfer Charge (Rs)", value=None, placeholder="0.0")
        with col2:
            hp_term = st.number_input("HP Terminate Charge (Rs)", value=None, placeholder="0.0")
            hp_add = st.number_input("HP Add Charge (Rs)", value=None, placeholder="0.0")
            oth_ch = st.number_input("Other Charge (Rs)", value=None, placeholder="0.0")
            int_type = st.radio("Interest Type", ["Flat Rate", "Reducing Balance"], horizontal=True)
            roi = st.number_input(f"{int_type} (%)", value=18.0) 
        
        loan_amt = (l_amt or 0) + (ins_ch or 0) + (pass_ch or 0) + (trans_ch or 0) + (hp_term or 0) + (hp_add or 0) + (oth_ch or 0)
        pdf_labels = [("Loan Amount", l_amt or 0), ("Ins/Pass/Trans", (ins_ch or 0)+(pass_ch or 0)+(trans_ch or 0)), ("HP Term/Add", (hp_term or 0)+(hp_add or 0)), ("Other Charges", oth_ch or 0)]

    st.markdown("---")
    st.subheader(f"📊 Live EMI Preview")
    if loan_amt > 0:
        all_tenures = [5, 10, 12, 15, 18, 24, 30, 36]
        for i in range(0, len(all_tenures), 4):
            cols = st.columns(4)
            for m, col in zip(all_tenures[i:i+4], cols):
                if int_type == "Flat Rate": emi = (loan_amt + (loan_amt * roi * (m/12) / 100)) / m
                else: r = roi / (12 * 100); emi = (loan_amt * r * (1 + r)**m) / ((1 + r)**m - 1)
                col.metric(f"{m} Mo", f"₹{emi:,.0f}")
    else: st.info("Enter values to see EMI preview.")

    if st.button("Generate Premium PDF Quotation"):
        if not cust_name or loan_amt == 0: st.error("Please fill details!")
        else:
            qr_buf = io.BytesIO()
            qrcode.make("----------").save(qr_buf, format='PNG') 
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            
            c.setFillColor(colors.HexColor("#1e3d59")); c.rect(0, 740, 600, 110, fill=1)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 28); c.drawCentredString(300, 805, "CAR MELA")
            c.setFont("Helvetica-Bold", 16); c.drawCentredString(300, 785, "....................")
            c.setFont("Helvetica-Oblique", 9)
            c.drawCentredString(300, 770, "....................................................................................................")
            
            c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 715, f"CUSTOMER NAME: {cust_name.upper()}")
            c.drawString(50, 695, f"VEHICLE MODEL: {veh_name.upper()}")
            c.drawRightString(540, 715, f"DATE: {current_time}"); c.line(50, 685, 540, 685)
            
            y = 655
            for label, val in pdf_labels:
                c.setFont("Helvetica-Bold", 12); c.drawString(70, y, label); c.drawRightString(520, y, f"Rs. {val:,.2f}"); y -= 25
            
            c.setFont("Helvetica-Bold", 12); c.drawString(70, y, "Net Loan Amount"); c.drawRightString(520, y, f"Rs. {loan_amt:,.2f}")
            y -= 25
            c.drawString(70, y, "Interest Rate"); c.drawRightString(520, y, f"{roi}% ({int_type})")
            c.line(50, y-10, 540, y-10)

            y -= 50; c.setFillColor(colors.HexColor("#1e3d59")); c.rect(50, y-10, 490, 30, fill=1)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 14); c.drawCentredString(300, y, "REPAYMENT SCHEDULE")
            c.setFillColor(colors.black); y -= 40
            c.setFont("Helvetica-Bold", 11); c.drawString(60, y, "TENURE"); c.drawCentredString(260, y, "MONTHLY EMI (RS)"); c.drawRightString(530, y, "TOTAL PAYABLE (RS)")
            c.line(50, y-5, 540, y-5); y -= 25
            
            for m in [5, 10, 12, 15, 18, 24, 30, 36]:
                if int_type == "Flat Rate": emi = (loan_amt + (loan_amt * roi * (m/12) / 100)) / m
                else: r = roi / (12 * 100); emi = (loan_amt * r * (1 + r)**m) / ((1 + r)**m - 1)
                c.setFont("Helvetica", 11); c.drawString(60, y, f"{m} Months Plan"); c.drawCentredString(260, y, f"{emi:,.2f}"); c.drawRightString(530, y, f"{emi*m:,.2f}"); y -= 22
                
            qr_y_pos = 45 
            c.drawImage(ImageReader(qr_buf), 50, qr_y_pos, width=60, height=60)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(50, qr_y_pos - 8, "ADDRESS:....................................") 
            c.line(50, 115, 540, 115) 
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(50, 122, f"* This is a computer-generated quotation based on {int_type.lower()}.") 
            
            c.setFont("Helvetica-Bold", 12)
            c.drawRightString(540, 85, "FOR, CAR MELA")
            c.drawRightString(540, 65, "Authorized Signature")

            c.save(); st.success("Quotation Ready!")
            st.download_button("📥 Download Premium Quotation", buffer.getvalue(), f"Quotation_{cust_name}.pdf", "application/pdf")
