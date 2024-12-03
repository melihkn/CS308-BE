from sqlalchemy.orm import Session
from models.models import Product
from fpdf import FPDF
import os

class InvoiceService:
    @staticmethod
    def generate_invoice(order, db: Session):
        """
        Generate an invoice PDF for the given order.
        """
        # Create a new PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add Order Details
        pdf.cell(200, 10, txt=f"Invoice for Order: {order.order_id}", ln=True, align="C")
        pdf.ln(10)

        # Fetch product details for each item in the order
        pdf.cell(200, 10, txt="Order Items:", ln=True)
        pdf.ln(5)
        for item in order.order_items:
            # Fetch product details from the database
            product = db.query(Product).filter_by(product_id=item.product_id).first()
            if not product:
                product_name = "Unknown Product"
            else:
                product_name = product.name  # Get the product name
            
            # Add item details to the invoice
            pdf.cell(
                200,
                10,
                txt=f"Product: {product_name}, Quantity: {item.quantity}, Actual Price: ${product.price},  Price at Purchase: ${item.price_at_purchase}",
                ln=True,
            )

        # Add Total Price
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Price: ${order.total_price}", ln=True)

        # Save the PDF file
        invoice_path = f"./invoices/INV-{order.order_id}.pdf"
        pdf.output(invoice_path)
        return invoice_path


"""
from fpdf import FPDF
from models.models import Product, Order, OrderItem
from sqlalchemy.orm import Session
from utils.db_utils import get_db


class InvoiceService:
    @staticmethod
    def generate_invoice(order, invoice_dir="./invoices"):
        '''
        Generate an invoice PDF for the given order.

        Input:
        - order: The order object to create an invoice for.
        - invoice_dir: Directory to save the invoice file.

        Output:
        - File path of the generated invoice.
        '''
        invoice_id = f"INV-{order.order_id}"
        file_name = f"{invoice_id}.pdf"
        file_path = f"{invoice_dir}/{file_name}"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, f"Invoice: {invoice_id}", ln=True, align="C")

        # Add customer details
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Customer: {order.customer_id}", ln=True, align="L")
        pdf.cell(200, 10, f"Order Date: {order.order_date.strftime('%Y-%m-%d')}", ln=True, align="L")
        pdf.cell(200, 10, f"Total Price: ${order.total_price:.2f}", ln=True, align="L")
        pdf.cell(200, 10, "Items:", ln=True, align="L")
        
        # Add order items
        for item in order.order_items:
            pdf.cell(
                200,
                10,
                f"  - {item.product_id}: {item.quantity} x ${item.price_at_purchase:.2f}",
                ln=True,
                align="L",
            )

        # Save the PDF
        pdf.output(file_path)
        return file_path

    # to get the invoice link
    @staticmethod
    def get_invoice_link(order_id: str, db: Session):
        '''
        Get the invoice link for the given order ID.

        Input:
        - order_id: The ID of the order to get the invoice link for.
        - db: Database session.

        Output:
        - Invoice link if found, None otherwise.
        '''
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if order:
            return order.invoice_link
        return None
"""