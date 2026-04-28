"""
QuickShop AI - PDF Document Generator
Creates 3 realistic e-commerce policy PDFs for the RAG pipeline.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import os

DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
os.makedirs(DOCS_DIR, exist_ok=True)

# ============================================
# Styles
# ============================================
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Heading1'],
    fontSize=22, textColor=HexColor('#1a73e8'),
    spaceAfter=20, alignment=TA_LEFT, fontName='Helvetica-Bold'
)
heading_style = ParagraphStyle(
    'CustomHeading', parent=styles['Heading2'],
    fontSize=14, textColor=HexColor('#202124'),
    spaceAfter=10, spaceBefore=15, fontName='Helvetica-Bold'
)
body_style = ParagraphStyle(
    'CustomBody', parent=styles['BodyText'],
    fontSize=11, textColor=HexColor('#3c4043'),
    spaceAfter=8, alignment=TA_JUSTIFY, leading=15
)

def build_pdf(filename, title, sections):
    """Build a PDF from a list of (heading, body) tuples."""
    path = os.path.join(DOCS_DIR, filename)
    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    story = [Paragraph(title, title_style), Spacer(1, 0.2*inch)]
    for heading, body in sections:
        story.append(Paragraph(heading, heading_style))
        for para in body:
            story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 0.1*inch))
    doc.build(story)
    print(f"✓ Created: {path}")

# ============================================
# 1. RETURN POLICY
# ============================================
return_policy = [
    ("1. Return Window", [
        "QuickShop AI offers a 30-day return window from the date of delivery for most products. Customers can initiate a return request through their account dashboard or by contacting customer support.",
        "Items must be returned in their original condition with all tags, packaging, and accessories intact. Used or damaged items will not be eligible for refunds."
    ]),
    ("2. Eligible Categories", [
        "Apparel, Footwear, Home Decor, and Sports items are eligible for the standard 30-day return policy. Beauty and Personal Care products can be returned only if unopened and sealed.",
        "Electronics including smartphones, laptops, and headphones have a reduced return window of 7 days from delivery, subject to inspection."
    ]),
    ("3. Non-Returnable Items", [
        "The following items cannot be returned: innerwear, swimwear, opened beauty products, customized or personalized items, perishable goods, and items marked as 'Final Sale' on the product page.",
        "Gift cards and digital downloads are non-refundable under all circumstances."
    ]),
    ("4. Refund Processing", [
        "Once a returned item is received and inspected at our warehouse, refunds are processed within 5-7 business days to the original payment method.",
        "For Cash on Delivery orders, refunds are issued via UPI or bank transfer to the registered customer account. Customers will receive an email and SMS notification once the refund is initiated."
    ]),
    ("5. Exchange Policy", [
        "Apparel and footwear can be exchanged for a different size or color within 15 days of delivery, subject to stock availability. Exchange requests should be raised through the order details page.",
        "Only one exchange is allowed per order. If the desired size is unavailable, customers can opt for a full refund instead."
    ]),
    ("6. Damaged or Defective Products", [
        "If you receive a damaged, defective, or incorrect product, please report it within 48 hours of delivery with clear photographs. QuickShop AI will arrange a free pickup and provide a replacement or full refund.",
        "For high-value electronics, an authorized service center inspection may be required before refund approval."
    ]),
    ("7. Return Pickup", [
        "QuickShop AI offers free reverse pickup in 12,000+ pin codes across India. Customers can schedule a convenient pickup slot during return initiation.",
        "In areas where reverse pickup is unavailable, customers may need to self-ship the product to our nearest warehouse. Self-shipping costs will be reimbursed up to ₹150 upon successful return."
    ])
]

# ============================================
# 2. SHIPPING GUIDE
# ============================================
shipping_guide = [
    ("1. Shipping Coverage", [
        "QuickShop AI delivers to over 25,000 pin codes across India, covering all major metros, tier-2 cities, and most rural locations. Customers can verify delivery availability by entering their pin code on the product page.",
        "International shipping is currently not available. We are working to expand to UAE, Singapore, and the United States by Q3 2026."
    ]),
    ("2. Delivery Timelines", [
        "Standard delivery: 3-5 business days to metro cities (Mumbai, Delhi, Bangalore, Chennai, Kolkata, Hyderabad). Express delivery: 1-2 business days, available at additional cost.",
        "Tier-2 cities and remote locations: 5-8 business days. Same-day delivery is available in select Mumbai, Delhi, and Bangalore zones for orders placed before 12:00 PM IST."
    ]),
    ("3. Shipping Charges", [
        "Standard shipping is FREE on all orders above ₹499. For orders below ₹499, a flat shipping charge of ₹49 applies.",
        "Express shipping is charged at ₹99 per order regardless of cart value. Same-day delivery is priced at ₹149."
    ]),
    ("4. Order Tracking", [
        "All orders include real-time tracking with SMS, email, and push notifications. Customers receive tracking links once the order is dispatched from our warehouse.",
        "The order status moves through: Order Confirmed → Packed → Shipped → Out for Delivery → Delivered. Estimated delivery times are updated based on transit progress."
    ]),
    ("5. Delivery Partners", [
        "QuickShop AI partners with leading logistics providers including Delhivery, Blue Dart, Ekart, DTDC, and Indian Post for nationwide reach.",
        "For high-value electronics and fragile items, we use specialized handling partners with insurance coverage during transit."
    ]),
    ("6. Address Changes", [
        "Delivery addresses can be modified within 30 minutes of placing the order. Once the order is packed for dispatch, address changes are not possible.",
        "If you need to change your delivery address after dispatch, please contact customer support. Re-routing charges of ₹100 may apply."
    ]),
    ("7. Failed Delivery Attempts", [
        "Our delivery partners make up to 3 attempts to deliver your order. If all attempts fail, the package is returned to our warehouse and refund is initiated automatically.",
        "Customers can also choose store pickup at select locations. Packages are held for 5 days at pickup points before being returned."
    ])
]

# ============================================
# 3. PRODUCT FAQ
# ============================================
product_faq = [
    ("1. Sizing & Fit", [
        "All apparel products include a detailed size chart on the product page with measurements in inches and centimeters. We recommend measuring yourself and comparing with the chart before ordering.",
        "If you are between sizes, we generally recommend going one size up for a comfortable fit. Free size exchanges are available within 15 days for apparel and footwear."
    ]),
    ("2. Product Authenticity", [
        "All products sold on QuickShop AI are 100% authentic and sourced directly from authorized brand distributors. Each electronics item includes a manufacturer warranty card and original packaging.",
        "If you suspect a product is not genuine, please raise a concern within 7 days of delivery. We offer a full refund and warehouse investigation for all authenticity claims."
    ]),
    ("3. Care Instructions", [
        "Care instructions for apparel products are listed on the product label and on the product detail page. Generally, dark colors should be washed separately for the first 2-3 washes to prevent color bleeding.",
        "For electronics, we recommend reading the user manual carefully and using only original chargers and accessories provided in the box."
    ]),
    ("4. Warranty Coverage", [
        "Smartphones, laptops, and tablets come with 1-year manufacturer warranty covering manufacturing defects. Headphones, smart watches, and accessories include 6-month warranty.",
        "Apparel and home decor items do not carry a warranty but are covered by our 30-day return policy. Beauty and personal care products are non-returnable once opened."
    ]),
    ("5. Stock Availability", [
        "Out-of-stock items are clearly marked on the product page. Customers can opt for the 'Notify Me' feature to receive alerts when restocked.",
        "Most popular items are restocked within 7-10 business days. Limited edition or seasonal products may not be restocked once sold out."
    ]),
    ("6. Customization Requests", [
        "Currently, QuickShop AI does not offer product customization or personalization. All products are sold as displayed on the product page.",
        "For bulk corporate orders above 50 units, custom branding options may be available. Please reach out to our B2B team at corporate@quickshop-ai.example for more details."
    ]),
    ("7. Bulk Orders", [
        "Customers placing orders above ₹25,000 in a single transaction qualify for our Premium customer benefits including priority shipping, dedicated support, and extended return windows.",
        "For corporate or institutional bulk orders, please contact our B2B sales team for volume-based pricing and customized payment terms."
    ]),
    ("8. Customer Support", [
        "Customer support is available 24/7 through chat, email (support@quickshop-ai.example), and phone (1800-QUICK-AI). Average response time is under 5 minutes for chat queries.",
        "For order-specific issues, please have your order ID ready. Most queries are resolved on the first contact."
    ])
]

# ============================================
# Build all 3 PDFs
# ============================================
if __name__ == '__main__':
    build_pdf('return_policy.pdf', 'QuickShop AI - Return & Refund Policy', return_policy)
    build_pdf('shipping_guide.pdf', 'QuickShop AI - Shipping & Delivery Guide', shipping_guide)
    build_pdf('product_faq.pdf', 'QuickShop AI - Product FAQ', product_faq)
    print("\n✓ All PDFs generated successfully!")
