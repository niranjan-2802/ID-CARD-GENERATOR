from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QScrollArea
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import random
import os
import datetime
import qrcode
import cv2
import sys
from pathlib import Path
import webbrowser
import numpy as np
import io
import traceback

class IDCardGenerator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.watermark = "MADE BY KREDIX XYPHER"
        self.camera_active = False
        self.templates = {
            "Standard": "templates/standard.png",
            "Modern": "templates/modern.png",
            "Corporate": "templates/corporate.png",
            "Minimalist": "templates/minimalist.png",
            "Elegant": "templates/elegant.png",
            "Tech": "templates/tech.png"
        }
        
        self.setupUi(self)
        Path("templates").mkdir(exist_ok=True)
        Path("output").mkdir(exist_ok=True)
        self.generate_default_templates()
        self.setup_styles()
        
    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton#danger {
                background-color: #ef4444;
            }
            QPushButton#danger:hover {
                background-color: #dc2626;
            }
            QPushButton#success {
                background-color: #10b981;
            }
            QPushButton#success:hover {
                background-color: #059669;
            }
            QHeaderView::section {
                background-color: #3b82f6;
                color: white;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QCheckBox {
                spacing: 5px;
            }
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QScrollArea {
                border: none;
            }
        """)
        self.generate_btn.setObjectName("success")
        self.clear_btn.setObjectName("danger")
        
    def update_fields(self, name, uid, department):
        self.lineEdit_2.setText(name)
        self.lineEdit.setText(department)
        self.lineEdit_3.setText(uid)
        
    def generate_default_templates(self):
        # Standard template
        if not os.path.exists("templates/standard.png"):
            img = Image.new('RGB', (1000, 600), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 950, 550], outline=(0, 0, 0), width=5)
            draw.rectangle([600, 100, 900, 400], outline=(0, 0, 255), width=3)
            img.save("templates/standard.png")
        # Modern template
        if not os.path.exists("templates/modern.png"):
            img = Image.new('RGB', (1000, 600), (240, 240, 240))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 1000, 150], fill=(50, 100, 200))
            img.save("templates/modern.png")
        # Corporate template
        if not os.path.exists("templates/corporate.png"):
            img = Image.new('RGB', (1000, 600), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 1000, 100], fill=(0, 50, 100))
            draw.rectangle([0, 500, 1000, 600], fill=(0, 50, 100))
            img.save("templates/corporate.png")
        # Minimalist template
        if not os.path.exists("templates/minimalist.png"):
            img = Image.new('RGB', (1000, 600), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.line([50, 50, 950, 50], fill=(0, 0, 0), width=2)
            draw.line([50, 550, 950, 550], fill=(0, 0, 0), width=2)
            img.save("templates/minimalist.png")
        # Elegant template
        if not os.path.exists("templates/elegant.png"):
            img = Image.new('RGB', (1000, 600), (250, 245, 240))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 1000, 600], outline=(212, 175, 55), width=10)
            draw.rectangle([0, 120, 1000, 125], fill=(212, 175, 55))
            img.save("templates/elegant.png")
        # Tech template
        if not os.path.exists("templates/tech.png"):
            img = Image.new('RGB', (1000, 600), (20, 25, 30))
            draw = ImageDraw.Draw(img)
            for i in range(0, 1000, 50):
                draw.line([i, 0, i, 600], fill=(0, 100, 150, 50), width=1)
            for i in range(0, 600, 50):
                draw.line([0, i, 1000, i], fill=(0, 100, 150, 50), width=1)
            draw.rectangle([0, 0, 1000, 80], fill=(0, 150, 200))
            img.save("templates/tech.png")

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 800)
        Form.setMinimumSize(QtCore.QSize(900, 700))
        self.main_layout = QtWidgets.QVBoxLayout(Form)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header = QtWidgets.QLabel("Advanced ID Card Generator")
        self.header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e3a8a;")
        self.header.setAlignment(QtCore.Qt.AlignLeft)
        
       
        self.github_btn = QtWidgets.QPushButton()
        self.github_btn.setIcon(QtGui.QIcon.fromTheme("github"))  
        try:
            
            self.github_btn.setIcon(QtGui.QIcon("github.png"))
        except:
           
            pixmap = QtGui.QPixmap(32, 32)
            pixmap.fill(QtGui.QColor(0, 0, 0, 0))
            painter = QtGui.QPainter(pixmap)
            painter.setPen(QtGui.QColor(0, 0, 0))
            painter.setBrush(QtGui.QColor(0, 0, 0))
            painter.drawEllipse(0, 0, 32, 32)
            painter.setPen(QtGui.QColor(255, 255, 255))
            painter.drawText(0, 0, 32, 32, QtCore.Qt.AlignCenter, "Git")
            painter.end()
            self.github_btn.setIcon(QtGui.QIcon(pixmap))
            
        self.github_btn.setIconSize(QtCore.QSize(32, 32))
        self.github_btn.setToolTip("Visit developer's GitHub")
        self.github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/kredix-xypher"))
        self.github_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0;
            }
            QPushButton:hover {
                background-color: rgba(0,0,0,0.1);
                border-radius: 16px;
            }
        """)
        
        self.header_layout.addWidget(self.header)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.github_btn)
        self.main_layout.addLayout(self.header_layout)
        
        # Main form layout
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setVerticalSpacing(15)
        self.form_layout.setHorizontalSpacing(20)
        self.main_layout.addLayout(self.form_layout)
        
        # Basic fields
        self.label_2 = QtWidgets.QLabel("Company/Organization:")
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Enter company name")
        self.form_layout.addRow(self.label_2, self.lineEdit)
        
        self.label_3 = QtWidgets.QLabel("Full Name:")
        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setPlaceholderText("Enter your full name")
        self.form_layout.addRow(self.label_3, self.lineEdit_2)
        
        self.label_id = QtWidgets.QLabel("ID Number:")
        self.lineEdit_3 = QtWidgets.QLineEdit()
        self.lineEdit_3.setPlaceholderText("Enter ID number")
        self.form_layout.addRow(self.label_id, self.lineEdit_3)
        
        self.label_4 = QtWidgets.QLabel("Gender:")
        self.gender_combo = QtWidgets.QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.form_layout.addRow(self.label_4, self.gender_combo)
        
        self.label_dept = QtWidgets.QLabel("Department:")
        self.dept_combo = QtWidgets.QComboBox()
        self.dept_combo.addItems(["Management", "IT", "HR", "Finance", "Operations", "Marketing"])
        self.form_layout.addRow(self.label_dept, self.dept_combo)
        
        self.label_5 = QtWidgets.QLabel("Address:")
        self.lineEdit_4 = QtWidgets.QLineEdit()
        self.lineEdit_4.setPlaceholderText("Enter your address")
        self.form_layout.addRow(self.label_5, self.lineEdit_4)
        
        self.label_6 = QtWidgets.QLabel("Phone Number:")
        self.lineEdit_5 = QtWidgets.QLineEdit()
        self.lineEdit_5.setPlaceholderText("Enter phone number")
        self.form_layout.addRow(self.label_6, self.lineEdit_5)
        
        self.label_email = QtWidgets.QLabel("Email:")
        self.lineEdit_6 = QtWidgets.QLineEdit()
        self.lineEdit_6.setPlaceholderText("Enter email address")
        self.form_layout.addRow(self.label_email, self.lineEdit_6)
        
        self.label_template = QtWidgets.QLabel("Card Template:")
        self.template_combo = QtWidgets.QComboBox()
        self.template_combo.addItems(["Standard", "Modern", "Corporate", "Minimalist", "Elegant", "Tech"])
        self.template_preview_btn = QtWidgets.QPushButton("Preview")
        self.template_preview_btn.clicked.connect(self.preview_template)
        template_layout = QtWidgets.QHBoxLayout()
        template_layout.addWidget(self.template_combo)
        template_layout.addWidget(self.template_preview_btn)
        self.form_layout.addRow(self.label_template, template_layout)
        
        # Image handling
        self.image_layout = QtWidgets.QHBoxLayout()
        self.capture_btn = QtWidgets.QPushButton("Capture Image")
        self.capture_btn.clicked.connect(self.capture)
        self.image_layout.addWidget(self.capture_btn)
        self.upload_btn = QtWidgets.QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        self.image_layout.addWidget(self.upload_btn)
        self.edit_btn = QtWidgets.QPushButton("Edit Image")
        self.edit_btn.clicked.connect(self.edit_image)
        self.image_layout.addWidget(self.edit_btn)
        self.form_layout.addRow("Photo:", self.image_layout)

        # --- Advanced Options Section with Scroll Area ---
        self.advanced_group = QtWidgets.QGroupBox("Advanced Options")
        self.advanced_group.setCheckable(True)
        self.advanced_group.setChecked(False)
        
        # Create scroll area for advanced options
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(300)
        
        # Container widget for advanced options
        advanced_container = QtWidgets.QWidget()
        advanced_layout = QtWidgets.QVBoxLayout(advanced_container)
        advanced_layout.setContentsMargins(15, 15, 15, 15)
        advanced_layout.setSpacing(15)
        
        # QR Code Options
        qr_group = QtWidgets.QGroupBox("QR Code Content")
        qr_layout = QtWidgets.QVBoxLayout()
        qr_layout.setContentsMargins(10, 15, 10, 15)
        qr_layout.setSpacing(10)
        qr_group.setLayout(qr_layout)
        
        self.qr_basic = QtWidgets.QRadioButton("Basic Info (Name, ID)")
        self.qr_basic.setChecked(True)
        self.qr_full = QtWidgets.QRadioButton("Full Info (All fields)")
        self.qr_custom = QtWidgets.QRadioButton("Custom Text")
        self.qr_custom_text = QtWidgets.QLineEdit()
        self.qr_custom_text.setPlaceholderText("Enter custom QR code content")
        self.qr_custom_text.setEnabled(False)
        
        qr_layout.addWidget(self.qr_basic)
        qr_layout.addWidget(self.qr_full)
        qr_layout.addWidget(self.qr_custom)
        qr_layout.addWidget(self.qr_custom_text)
        
        self.qr_basic.toggled.connect(lambda checked: self.qr_custom_text.setEnabled(self.qr_custom.isChecked()))
        self.qr_full.toggled.connect(lambda checked: self.qr_custom_text.setEnabled(self.qr_custom.isChecked()))
        self.qr_custom.toggled.connect(lambda checked: self.qr_custom_text.setEnabled(checked))
        
        # Signature Options
        signature_group = QtWidgets.QGroupBox("Signature")
        signature_layout = QtWidgets.QVBoxLayout()
        signature_layout.setContentsMargins(10, 15, 10, 15)
        signature_layout.setSpacing(10)
        signature_group.setLayout(signature_layout)
        
        self.signature_check = QtWidgets.QCheckBox("Include Digital Signature")
        self.signature_check.setChecked(True)
        signature_layout.addWidget(self.signature_check)
        
        signature_style_layout = QtWidgets.QHBoxLayout()
        signature_style_layout.addWidget(QtWidgets.QLabel("Signature Style:"))
        self.signature_style = QtWidgets.QComboBox()
        self.signature_style.addItems(["Standard", "Handwritten", "Official"])
        self.signature_style.setEnabled(self.signature_check.isChecked())
        signature_style_layout.addWidget(self.signature_style)
        signature_style_layout.addStretch()
        signature_layout.addLayout(signature_style_layout)
        
        self.signature_check.toggled.connect(self.signature_style.setEnabled)

        # Image Processing Options
        image_group = QtWidgets.QGroupBox("Image Processing")
        image_layout = QtWidgets.QGridLayout()
        image_layout.setContentsMargins(10, 15, 10, 15)
        image_layout.setVerticalSpacing(10)
        image_layout.setHorizontalSpacing(15)
        image_group.setLayout(image_layout)
        
        # Row 0
        self.bg_blur = QtWidgets.QCheckBox("Blur Background")
        image_layout.addWidget(self.bg_blur, 0, 0, 1, 2)
        
        # Row 1 - Brightness
        brightness_label = QtWidgets.QLabel("Brightness:")
        image_layout.addWidget(brightness_label, 1, 0)
        
        self.bg_brightness = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.bg_brightness.setRange(-100, 100)
        self.bg_brightness.setValue(0)
        self.bg_brightness.setTickInterval(10)
        image_layout.addWidget(self.bg_brightness, 1, 1)
        
        # Row 2 - Contrast
        contrast_label = QtWidgets.QLabel("Contrast:")
        image_layout.addWidget(contrast_label, 2, 0)
        
        self.bg_contrast = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.bg_contrast.setRange(-100, 100)
        self.bg_contrast.setValue(0)
        self.bg_contrast.setTickInterval(10)
        image_layout.addWidget(self.bg_contrast, 2, 1)
        
        # Preview Checkbox
        self.preview_check = QtWidgets.QCheckBox("Show Preview Before Saving")
        self.preview_check.setChecked(True)
        
        # Add all groups to advanced layout
        advanced_layout.addWidget(qr_group)
        advanced_layout.addWidget(signature_group)
        advanced_layout.addWidget(image_group)
        advanced_layout.addWidget(self.preview_check)
        advanced_layout.addStretch()
        
        # Set up scroll area
        scroll.setWidget(advanced_container)
        self.advanced_group.setLayout(QtWidgets.QVBoxLayout())
        self.advanced_group.layout().addWidget(scroll)
        self.main_layout.addWidget(self.advanced_group)

        # Action buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(20)
        
        self.generate_btn = QtWidgets.QPushButton("Generate ID Card")
        self.generate_btn.clicked.connect(self.generate_idcard)
        
        self.clear_btn = QtWidgets.QPushButton("Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        
        self.button_layout.addWidget(self.generate_btn)
        self.button_layout.addWidget(self.clear_btn)
        self.main_layout.addLayout(self.button_layout)

        # Status label
        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #374151; 
                font-size: 13px; 
                padding: 8px;
                border-top: 1px solid #d1d5db;
            }
        """)
        self.main_layout.addWidget(self.status_label)

        # Set tab order
        self.setTabOrder(self.lineEdit, self.lineEdit_2)
        self.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        self.setTabOrder(self.lineEdit_3, self.gender_combo)
        self.setTabOrder(self.gender_combo, self.dept_combo)
        self.setTabOrder(self.dept_combo, self.lineEdit_4)
        self.setTabOrder(self.lineEdit_4, self.lineEdit_5)
        self.setTabOrder(self.lineEdit_5, self.lineEdit_6)
        self.setTabOrder(self.lineEdit_6, self.template_combo)
        self.setTabOrder(self.template_combo, self.capture_btn)
        self.setTabOrder(self.capture_btn, self.upload_btn)
        self.setTabOrder(self.upload_btn, self.edit_btn)
        self.setTabOrder(self.edit_btn, self.generate_btn)
        self.setTabOrder(self.generate_btn, self.clear_btn)

    def preview_template(self):
        template_name = self.template_combo.currentText()
        template_path = self.templates.get(template_name, "templates/standard.png")
        
        if os.path.exists(template_path):
            preview = QtWidgets.QMessageBox()
            preview.setWindowTitle(f"Template Preview: {template_name}")
            
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            
            label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(template_path)
            label.setPixmap(pixmap)
            scroll.setWidget(label)
            
            layout = preview.layout()
            layout.addWidget(scroll, 0, 0, 1, layout.columnCount())
            preview.setStyleSheet("QLabel{min-width: 600px; min-height: 400px;}")
            
            preview.exec_()
        else:
            self.status_label.setText(f"Template {template_name} not found")
            self.status_label.setStyleSheet("color: red;")

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Profile Image", "", 
            "Image Files (*.jpg *.jpeg *.png)", options=options
        )
        
        if file_name:
            try:
                img = Image.open(file_name)
                img = img.resize((300, 300))
                img.save('person.jpg')
                self.status_label.setText("Image uploaded successfully!")
                self.status_label.setStyleSheet("color: green;")
            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")
                self.status_label.setStyleSheet("color: red;")

    def edit_image(self):
        if not os.path.exists('person.jpg'):
            self.status_label.setText("No image to edit. Please capture or upload first.")
            self.status_label.setStyleSheet("color: red;")
            return
            
        try:
            # Create edit dialog
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Edit Profile Image")
            dialog.setMinimumSize(600, 400)
            
            layout = QtWidgets.QVBoxLayout()
            
            # Image display
            self.edit_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap('person.jpg')
            self.edit_label.setPixmap(pixmap)
            
            # Edit controls
            controls = QtWidgets.QHBoxLayout()
            
            # Brightness
            brightness = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            brightness.setRange(-100, 100)
            brightness.setValue(0)
            brightness_label = QtWidgets.QLabel("Brightness")
            
            # Contrast
            contrast = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            contrast.setRange(-100, 100)
            contrast.setValue(0)
            contrast_label = QtWidgets.QLabel("Contrast")
            
            # Blur
            blur = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            blur.setRange(0, 10)
            blur.setValue(0)
            blur_label = QtWidgets.QLabel("Blur")
            
            # Rotation
            rotate = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            rotate.setRange(0, 360)
            rotate.setValue(0)
            rotate_label = QtWidgets.QLabel("Rotation")
            
            # Add to layout
            controls.addWidget(brightness_label)
            controls.addWidget(brightness)
            controls.addWidget(contrast_label)
            controls.addWidget(contrast)
            controls.addWidget(blur_label)
            controls.addWidget(blur)
            controls.addWidget(rotate_label)
            controls.addWidget(rotate)
            
            # Buttons
            btn_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            btn_box.accepted.connect(dialog.accept)
            btn_box.rejected.connect(dialog.reject)
            
            # Connect sliders
            def update_image():
                img = Image.open('person.jpg')
                
                # Apply brightness
                enhancer = ImageEnhance.Brightness(img)
                factor = 1 + (brightness.value() / 100)
                img = enhancer.enhance(factor)
                
                # Apply contrast
                enhancer = ImageEnhance.Contrast(img)
                factor = 1 + (contrast.value() / 100)
                img = enhancer.enhance(factor)
                
                # Apply blur
                if blur.value() > 0:
                    img = img.filter(ImageFilter.GaussianBlur(blur.value()))
                
                # Apply rotation
                if rotate.value() > 0:
                    img = img.rotate(rotate.value(), expand=True)
                    img = img.resize((300, 300))
                
                # Update preview
                img.save('temp_edit.jpg')
                pixmap = QtGui.QPixmap('temp_edit.jpg')
                self.edit_label.setPixmap(pixmap)
                
            brightness.valueChanged.connect(update_image)
            contrast.valueChanged.connect(update_image)
            blur.valueChanged.connect(update_image)
            rotate.valueChanged.connect(update_image)
            
            # Add widgets to dialog
            layout.addWidget(self.edit_label)
            layout.addLayout(controls)
            layout.addWidget(btn_box)
            dialog.setLayout(layout)
            
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                os.replace('temp_edit.jpg', 'person.jpg')
                self.status_label.setText("Image edited successfully!")
                self.status_label.setStyleSheet("color: green;")
            else:
                if os.path.exists('temp_edit.jpg'):
                    os.remove('temp_edit.jpg')
                
        except Exception as e:
            self.status_label.setText(f"Error editing image: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

    def capture(self):
        if self.camera_active:
            return
            
        self.camera_active = True
        camera = cv2.VideoCapture(0)
        
        while self.camera_active:
            return_value, image = camera.read()
            image = cv2.flip(image, 1)
            cv2.imshow('Capture Image - Press ENTER to capture, ESC to cancel', image)
            
            key = cv2.waitKey(1)
            if key == 13:  # Enter key
                height, width = image.shape[:2]
                start_row, start_col = int(height * .25), int(width * .25)
                end_row, end_col = int(height * .80), int(width * .80)
                cropped_img = image[start_row:end_row, start_col:end_col]
                cv2.imwrite('person.jpg', cropped_img)
                self.status_label.setText("Image captured successfully!")
                self.status_label.setStyleSheet("color: green;")
                break
            elif key == 27:  # ESC key
                self.status_label.setText("Image capture cancelled")
                self.status_label.setStyleSheet("color: orange;")
                break
        
        camera.release()
        cv2.destroyAllWindows()
        self.camera_active = False

    def clear_form(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.gender_combo.setCurrentIndex(0)
        self.dept_combo.setCurrentIndex(0)
        self.template_combo.setCurrentIndex(0)
        self.qr_basic.setChecked(True)
        self.qr_custom_text.clear()
        self.signature_check.setChecked(True)
        self.bg_blur.setChecked(False)
        self.bg_brightness.setValue(0)
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: #374151;")
        
        if os.path.exists('person.jpg'):
            os.remove('person.jpg')

    def generate_idcard(self):
        # Validate inputs
        required_fields = [
            (self.lineEdit.text(), "Company name"),
            (self.lineEdit_2.text(), "Full name"),
            (self.lineEdit_3.text(), "ID number")
        ]
        
        for value, field in required_fields:
            if not value.strip():
                self.status_label.setText(f"Please enter {field}")
                self.status_label.setStyleSheet("color: red;")
                return
        
        if not os.path.exists('person.jpg'):
            self.status_label.setText("Please capture or upload a profile image")
            self.status_label.setStyleSheet("color: red;")
            return

        try:
            # Load selected template
            template_name = self.template_combo.currentText()
            template_path = self.templates.get(template_name, "templates/standard.png")
            image = Image.open(template_path)
            draw = ImageDraw.Draw(image)
            
            # Set fonts
            try:
                title_font = ImageFont.truetype('arial.ttf', size=45)
                normal_font = ImageFont.truetype('arial.ttf', size=35)
                small_font = ImageFont.truetype('arial.ttf', size=25)
                signature_font = ImageFont.truetype('arial.ttf', size=20)
            except:
                # Fallback to default font if Arial not available
                title_font = ImageFont.load_default()
                normal_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
                signature_font = ImageFont.load_default()
            
            # Get current date for card
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Add text to card based on template
            if template_name == "Standard":
                # Company name
                draw.text((100, 100), self.lineEdit.text(), fill=(0, 0, 0), font=title_font)
                
                # ID number
                id_no = self.lineEdit_3.text()
                draw.text((100, 180), f"ID: {id_no}", fill=(255, 0, 0), font=normal_font)
                
                # Name
                draw.text((100, 250), self.lineEdit_2.text(), fill=(0, 0, 0), font=normal_font)
                
                # Department
                draw.text((100, 320), f"Dept: {self.dept_combo.currentText()}", fill=(0, 0, 0), font=normal_font)
                
                # Phone
                draw.text((100, 390), f"Phone: {self.lineEdit_5.text()}", fill=(0, 0, 0), font=normal_font)
                
                # Email
                draw.text((100, 460), f"Email: {self.lineEdit_6.text()}", fill=(0, 0, 0), font=small_font)
                
                # Issue date
                draw.text((100, 520), f"Issued: {date}", fill=(100, 100, 100), font=small_font)
                
                # Photo position
                photo_pos = (600, 100)
                qr_pos = (600, 420)
                signature_pos = (600, 520)
                
            elif template_name == "Modern":
                # Company name (on blue header)
                draw.text((100, 50), self.lineEdit.text(), fill=(255, 255, 255), font=title_font)
                
                # Photo position
                photo_pos = (650, 180)
                qr_pos = (650, 420)
                signature_pos = (650, 520)
                
                # ID details
                y_pos = 180
                draw.text((100, y_pos), self.lineEdit_2.text(), fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"ID: {self.lineEdit_3.text()}", fill=(50, 100, 200), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Dept: {self.dept_combo.currentText()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Phone: {self.lineEdit_5.text()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Email: {self.lineEdit_6.text()}", fill=(0, 0, 0), font=small_font)
                
            elif template_name == "Corporate":
                # Company name (on blue header)
                draw.text((100, 30), self.lineEdit.text(), fill=(255, 255, 255), font=title_font)
                
                # Photo position
                photo_pos = (650, 120)
                qr_pos = (650, 370)
                signature_pos = (650, 520)
                
                # ID details
                y_pos = 120
                draw.text((100, y_pos), f"ID: {self.lineEdit_3.text()}", fill=(0, 50, 100), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), self.lineEdit_2.text(), fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Dept: {self.dept_combo.currentText()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Phone: {self.lineEdit_5.text()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Email: {self.lineEdit_6.text()}", fill=(0, 0, 0), font=small_font)
                
                # Footer
                draw.text((100, 530), f"Issued: {date}", fill=(255, 255, 255), font=small_font)
                
            elif template_name == "Minimalist":
                # Company name
                draw.text((100, 70), self.lineEdit.text(), fill=(0, 0, 0), font=title_font)
                
                # Photo position
                photo_pos = (650, 100)
                qr_pos = (650, 370)
                signature_pos = (650, 520)
                
                # ID details
                y_pos = 180
                draw.text((100, y_pos), self.lineEdit_2.text(), fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"ID: {self.lineEdit_3.text()}", fill=(100, 100, 100), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Dept: {self.dept_combo.currentText()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 40
                draw.text((100, y_pos), f"Phone: {self.lineEdit_5.text()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 40
                draw.text((100, y_pos), f"Email: {self.lineEdit_6.text()}", fill=(0, 0, 0), font=small_font)
                
            elif template_name == "Elegant":
                # Company name
                draw.text((100, 70), self.lineEdit.text(), fill=(212, 175, 55), font=title_font)
                
                # Photo position
                photo_pos = (650, 100)
                qr_pos = (650, 370)
                signature_pos = (650, 520)
                
                                # ID details
                y_pos = 180
                draw.text((100, y_pos), self.lineEdit_2.text(), fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"ID: {self.lineEdit_3.text()}", fill=(212, 175, 55), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Dept: {self.dept_combo.currentText()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Phone: {self.lineEdit_5.text()}", fill=(0, 0, 0), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Email: {self.lineEdit_6.text()}", fill=(0, 0, 0), font=small_font)
                
            elif template_name == "Tech":
                # Company name (on blue header)
                draw.text((100, 20), self.lineEdit.text(), fill=(255, 255, 255), font=title_font)
                
                # Photo position
                photo_pos = (650, 100)
                qr_pos = (650, 370)
                signature_pos = (650, 520)
                
                # ID details
                y_pos = 100
                draw.text((100, y_pos), f"ID: {self.lineEdit_3.text()}", fill=(0, 150, 200), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), self.lineEdit_2.text(), fill=(255, 255, 255), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Dept: {self.dept_combo.currentText()}", fill=(255, 255, 255), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Phone: {self.lineEdit_5.text()}", fill=(255, 255, 255), font=normal_font)
                y_pos += 60
                draw.text((100, y_pos), f"Email: {self.lineEdit_6.text()}", fill=(255, 255, 255), font=small_font)
                
                # Footer
                draw.text((100, 530), f"Issued: {date}", fill=(0, 150, 200), font=small_font)
            
            # Add profile photo
            try:
                profile_img = Image.open('person.jpg')
                
                # Apply image processing if enabled
                if self.bg_blur.isChecked():
                    # Create a blurred version of the image
                    blurred_img = profile_img.filter(ImageFilter.GaussianBlur(10))
                    
                    # Create a mask for the face area
                    mask = Image.new('L', profile_img.size, 0)
                    draw_mask = ImageDraw.Draw(mask)
                    
                    # Draw an ellipse in the center (assuming face is centered)
                    width, height = profile_img.size
                    draw_mask.ellipse((width//4, height//4, width*3//4, height*3//4), fill=255)
                    
                    # Combine original and blurred images
                    profile_img = Image.composite(profile_img, blurred_img, mask)
                
                # Apply brightness/contrast adjustments
                brightness_factor = 1 + (self.bg_brightness.value() / 100)
                contrast_factor = 1 + (self.bg_contrast.value() / 100)
                
                enhancer = ImageEnhance.Brightness(profile_img)
                profile_img = enhancer.enhance(brightness_factor)
                
                enhancer = ImageEnhance.Contrast(profile_img)
                profile_img = enhancer.enhance(contrast_factor)
                
                # Resize and paste onto ID card
                profile_img = profile_img.resize((250, 250))
                image.paste(profile_img, photo_pos)
            except Exception as e:
                self.status_label.setText(f"Error processing profile image: {str(e)}")
                self.status_label.setStyleSheet("color: red;")
                return
            
            # Add QR code if enabled
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=5,
                    border=2,
                )
                
                # Determine QR code content
                if self.qr_basic.isChecked():
                    qr_content = f"Name: {self.lineEdit_2.text()}\nID: {self.lineEdit_3.text()}"
                elif self.qr_full.isChecked():
                    qr_content = f"""
                    Company: {self.lineEdit.text()}
                    Name: {self.lineEdit_2.text()}
                    ID: {self.lineEdit_3.text()}
                    Dept: {self.dept_combo.currentText()}
                    Phone: {self.lineEdit_5.text()}
                    Email: {self.lineEdit_6.text()}
                    """
                else:  # Custom
                    qr_content = self.qr_custom_text.text()
                
                qr.add_data(qr_content)
                qr.make(fit=True)
                
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_img = qr_img.resize((150, 150))
                image.paste(qr_img, qr_pos)
            except Exception as e:
                self.status_label.setText(f"Error generating QR code: {str(e)}")
                self.status_label.setStyleSheet("color: red;")
                return
            
            # Add signature if enabled
            if self.signature_check.isChecked():
                signature_style = self.signature_style.currentText()
                
                if signature_style == "Standard":
                    draw.text(signature_pos, "Authorized Signature", fill=(100, 100, 100), font=signature_font)
                    draw.line([signature_pos[0], signature_pos[1]+30, 
                              signature_pos[0]+200, signature_pos[1]+30], 
                             fill=(0, 0, 0), width=2)
                elif signature_style == "Handwritten":
                    # Simulate handwritten signature
                    name_parts = self.lineEdit_2.text().split()
                    if len(name_parts) > 1:
                        signature_text = f"{name_parts[0][0]}. {name_parts[-1]}"
                    else:
                        signature_text = self.lineEdit_2.text()
                    
                    # Create a temporary image for the signature
                    temp_img = Image.new('RGBA', (300, 100), (0, 0, 0, 0))
                    temp_draw = ImageDraw.Draw(temp_img)
                    
                    # Draw the signature with slight randomness to simulate handwriting
                    x_pos = 10
                    for i, char in enumerate(signature_text):
                        y_offset = random.randint(-3, 3)
                        rotation = random.randint(-5, 5)
                        char_img = Image.new('RGBA', (30, 40), (0, 0, 0, 0))
                        char_draw = ImageDraw.Draw(char_img)
                        char_draw.text((0, y_offset), char, fill=(0, 0, 0), font=signature_font)
                        char_img = char_img.rotate(rotation, expand=1)
                        temp_img.paste(char_img, (x_pos, 20), char_img)
                        x_pos += 25 + random.randint(-5, 2)
                    
                    # Paste the signature onto the ID card
                    image.paste(temp_img, (signature_pos[0], signature_pos[1]-20), temp_img)
                else:  # Official
                    draw.text((signature_pos[0], signature_pos[1]-20), "OFFICIAL ID", 
                             fill=(150, 0, 0), font=signature_font)
                    draw.text((signature_pos[0], signature_pos[1]+10), "Authorized by:", 
                             fill=(100, 100, 100), font=ImageFont.truetype('arial.ttf', size=15))
                    draw.line([signature_pos[0], signature_pos[1]+40, 
                              signature_pos[0]+250, signature_pos[1]+40], 
                             fill=(0, 0, 0), width=1)
            
            # Add watermark
            watermark_font = ImageFont.truetype('arial.ttf', size=15)
            draw.text((20, image.height-30), self.watermark, 
                     fill=(200, 200, 200, 128), font=watermark_font)
            
            # Show preview if enabled
            if self.preview_check.isChecked():
                preview = QtWidgets.QMessageBox()
                preview.setWindowTitle("ID Card Preview")
                
                # Convert PIL image to QPixmap
                byte_arr = io.BytesIO()
                image.save(byte_arr, format='PNG')
                qimg = QtGui.QImage.fromData(byte_arr.getvalue())
                pixmap = QtGui.QPixmap.fromImage(qimg)
                
                # Create scrollable preview
                scroll = QtWidgets.QScrollArea()
                scroll.setWidgetResizable(True)
                
                label = QtWidgets.QLabel()
                label.setPixmap(pixmap)
                scroll.setWidget(label)
                
                layout = preview.layout()
                layout.addWidget(scroll, 0, 0, 1, layout.columnCount())
                
                preview.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Cancel)
                preview.setDefaultButton(QtWidgets.QMessageBox.Save)
                
                result = preview.exec_()
                if result != QtWidgets.QMessageBox.Save:
                    self.status_label.setText("ID card generation cancelled")
                    self.status_label.setStyleSheet("color: orange;")
                    return
            
            # Save the final image
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            filename = f"{output_dir}/{self.lineEdit_2.text().replace(' ', '_')}_ID_{self.lineEdit_3.text()}.png"
            image.save(filename)
            
            self.status_label.setText(f"ID card saved as {filename}")
            self.status_label.setStyleSheet("color: green;")
            
        except Exception as e:
            error_msg = f"Error generating ID card: {str(e)}\n{traceback.format_exc()}"
            self.status_label.setText(error_msg[:200] + "...")  # Limit displayed error length
            self.status_label.setStyleSheet("color: red;")