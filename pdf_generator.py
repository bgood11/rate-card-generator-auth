"""
PDF Generator for Rate Cards with Stax Branding
"""
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
from typing import Dict


class PDFGenerator:
    def __init__(self):
        # Stax brand colors
        self.primary_blue = colors.HexColor('#477085')
        self.pink = colors.HexColor('#C668A8')
        self.light_blue = colors.HexColor('#2AB7E3')
        self.gray = colors.HexColor('#666666')
        self.light_gray = colors.HexColor('#F5F5F5')
        
        # Page setup
        self.page_width = A4[0]
        self.page_height = A4[1]
        self.margin = 0.75 * inch
        
    def create_styles(self):
        """Create custom styles for the PDF"""
        styles = getSampleStyleSheet()
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=self.primary_blue,
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=self.primary_blue,
            spaceAfter=6,
            spaceBefore=12
        ))
        
        # Footer style
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=self.gray,
            alignment=TA_CENTER,
            leading=12
        ))
        
        # Date style
        styles.add(ParagraphStyle(
            name='DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.gray,
            alignment=TA_RIGHT
        ))
        
        # Table cell style for wrapping text
        styles.add(ParagraphStyle(
            name='TableCell',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            alignment=TA_LEFT
        ))
        
        # Table cell center style
        styles.add(ParagraphStyle(
            name='TableCellCenter',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            alignment=TA_CENTER
        ))
        
        return styles
    
    def create_table_style(self):
        """Create branded table style"""
        return TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Lender column left aligned
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Other columns centered
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.light_gray]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
        ])
    
    def add_header(self, story, retailer_name, logo_path=None):
        """Add header with logo and title"""
        styles = self.create_styles()
        
        # Add logo if available
        if logo_path and os.path.exists(logo_path):
            logo = Image(logo_path, width=2*inch, height=0.8*inch, kind='proportional')
            story.append(logo)
            story.append(Spacer(1, 0.3*inch))
        
        # Add title
        title = Paragraph(f"{retailer_name} - Rate Card Analysis", styles['CustomTitle'])
        story.append(title)
        
        # Add generation date
        date_text = Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y')}", styles['DateStyle'])
        story.append(date_text)
        story.append(Spacer(1, 0.5*inch))
    
    def add_footer_to_canvas(self, canvas, doc):
        """Add footer to each page"""
        canvas.saveState()
        
        # Confidentiality statement
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(self.gray)
        
        footer_y = 0.5 * inch
        canvas.drawCentredString(
            self.page_width / 2.0,
            footer_y + 36,
            "PRIVATE & CONFIDENTIAL - This document contains proprietary information"
        )
        canvas.drawCentredString(
            self.page_width / 2.0,
            footer_y + 24,
            "and is not for sharing without written permission from Stax"
        )
        
        # Stax address
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawCentredString(
            self.page_width / 2.0,
            footer_y + 12,
            "Stax • Floor 2, Copthall House, Stourbridge, West Midlands, DY8 1PH"
        )
        
        # Page number
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(
            self.page_width - self.margin,
            footer_y,
            f"Page {doc.page}"
        )
        
        canvas.restoreState()
    
    def generate_pdf(self, retailer_name: str, data: Dict[str, pd.DataFrame], output_path: str, hide_commissions: bool = False):
        """Generate PDF rate card"""
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin + 0.5*inch  # Extra space for footer
        )
        
        # Build the story
        story = []
        styles = self.create_styles()
        
        # Add header with logo
        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'stax-logo.png')
        self.add_header(story, retailer_name, logo_path)
        
        # Process each product vertical
        for vertical_name, df in data.items():
            if df.empty:
                continue
            
            # Section header
            section_header = Paragraph(f"{vertical_name} Waterfall", styles['SectionHeader'])
            story.append(section_header)
            story.append(Spacer(1, 0.1*inch))
            
            # Prepare table data with wrapped headers
            header_style = ParagraphStyle(
                name='HeaderStyle',
                parent=styles['Normal'],
                fontSize=9,
                leading=11,
                alignment=TA_CENTER,
                textColor=colors.white,
                fontName='Helvetica-Bold'
            )
            
            if hide_commissions:
                headers = [
                    Paragraph('Lender', header_style),
                    Paragraph('Position', header_style),
                    Paragraph('Term', header_style),
                    Paragraph('Product Type', header_style),
                    Paragraph('Deferred Period', header_style),
                    Paragraph('APR Range', header_style),
                    Paragraph('Subsidy', header_style)
                ]
            else:
                headers = [
                    Paragraph('Lender', header_style),
                    Paragraph('Position', header_style),
                    Paragraph('Shermin Commission', header_style),
                    Paragraph('Term', header_style),
                    Paragraph('Product Type', header_style),
                    Paragraph('Deferred Period', header_style),
                    Paragraph('APR Range', header_style),
                    Paragraph('Subsidy', header_style)
                ]
            
            table_data = [headers]
            
            for _, row in df.iterrows():
                # Wrap lender name and position in Paragraph for text wrapping
                lender_name = Paragraph(str(row.get('Lender_Name', '')), styles['TableCell'])
                position = Paragraph(str(row.get('Position', '')), styles['TableCellCenter'])
                
                # Keep other cells as centered text, conditionally exclude commission
                if hide_commissions:
                    table_data.append([
                        lender_name,
                        position,
                        str(row.get('Term', '')),
                        str(row.get('Product_Type', '')),
                        str(row.get('Deferred_Period', '')),
                        str(row.get('APR_Range', '')),
                        str(row.get('Subsidy', ''))
                    ])
                else:
                    table_data.append([
                        lender_name,
                        position,
                        str(row.get('Shermin_Commission', '')),
                        str(row.get('Term', '')),
                        str(row.get('Product_Type', '')),
                        str(row.get('Deferred_Period', '')),
                        str(row.get('APR_Range', '')),
                        str(row.get('Subsidy', ''))
                    ])
            
            # Create table
            table = Table(table_data, repeatRows=1)
            table.setStyle(self.create_table_style())
            
            # Calculate column widths (proportional to page width)
            available_width = self.page_width - 2 * self.margin
            if hide_commissions:
                # Redistribute commission column width when hidden
                col_widths = [
                    available_width * 0.22,  # Lender (increased)
                    available_width * 0.12,  # Position (increased)
                    available_width * 0.12,  # Term (increased)
                    available_width * 0.14,  # Product Type (increased)
                    available_width * 0.15,  # Deferred Period (increased)
                    available_width * 0.12,  # APR Range (increased)
                    available_width * 0.13   # Subsidy (increased)
                ]
            else:
                col_widths = [
                    available_width * 0.18,  # Lender (reduced) 
                    available_width * 0.10,  # Position 
                    available_width * 0.12,  # Commission (reduced)
                    available_width * 0.10,  # Term
                    available_width * 0.12,  # Product Type
                    available_width * 0.13,  # Deferred Period
                    available_width * 0.10,  # APR Range
                    available_width * 0.15   # Subsidy (increased to balance)
                ]
            table._argW = col_widths
            
            story.append(table)
            story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story, onFirstPage=self.add_footer_to_canvas, onLaterPages=self.add_footer_to_canvas)
        
        return output_path