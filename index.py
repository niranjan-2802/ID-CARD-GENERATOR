import sys
import os
import sqlite3
import webbrowser
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTabWidget, QFormLayout, QLineEdit, QComboBox,
                             QDateEdit, QPushButton, QMessageBox, QApplication,
                             QStatusBar, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QDate, QSize
from PIL import Image
import cv2
from id_gen import IDCardGenerator
from PyQt5 import QtCore



class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional ID Card Generator - KREDIX XYPHER")
        self.setGeometry(100, 100, 1000, 800)
        
        # Set window icon
        try:
            self.setWindowIcon(QIcon('assets/icon.png'))
        except:
            pass
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header with GitHub button
        header_layout = QHBoxLayout()
        
        header = QLabel("Advanced ID Card Generator")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e3a8a;")
        header.setAlignment(Qt.AlignLeft)
        
        # GitHub button
        self.github_btn = QPushButton()
        try:
            self.github_btn.setIcon(QIcon('assets/github.png'))
        except:
            pass
        self.github_btn.setIconSize(QtCore.QSize(32, 32))
        self.github_btn.setToolTip("Visit developer's GitHub")
        self.github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/kredix-xypher"))
        self.github_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0;
            }
        """)
        
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.github_btn)
        main_layout.addLayout(header_layout)
        
        # Tab Widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create ID Tab
        self.create_tab = QWidget()
        self.setup_create_tab()
        self.tabs.addTab(self.create_tab, "Enter Information")
        
        # Generate ID Card Tab
        self.generate_tab = IDCardGenerator()
        self.tabs.addTab(self.generate_tab, "Generate Card")
        
        # Status Bar with watermark
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("MADE BY KREDIX XYPHER")
        self.setStatusBar(self.status_bar)
        
        # Apply stylesheet
        self.set_application_style()

    def set_application_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QTabWidget::pane {
                border: 1px solid #d1d5db;
                border-radius: 5px;
                padding: 10px;
                background: white;
                margin-top: 10px;
            }
            QTabBar::tab {
                padding: 10px 20px;
                background: #e5e7eb;
                border: 1px solid #d1d5db;
                border-radius: 5px;
                margin-right: 5px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #3b82f6;
                color: white;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
                min-width: 200px;
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
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

    def setup_create_tab(self):
        layout = QVBoxLayout()
        self.create_tab.setLayout(layout)
        
        # Form Layout
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)
        layout.addLayout(form_layout)
        
        # Personal Information
        personal_header = QLabel("Personal Information")
        personal_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e3a8a;")
        form_layout.addRow(personal_header)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        form_layout.addRow("Full Name:", self.name_input)
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter ID number")
        form_layout.addRow("ID Number:", self.id_input)
        
        self.department_combo = QComboBox()
        self.department_combo.addItems(["Management", "IT", "HR", "Finance", "Operations", "Marketing"])
        form_layout.addRow("Department:", self.department_combo)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        form_layout.addRow("Gender:", self.gender_combo)
        
        # Contact Information
        contact_header = QLabel("Contact Information")
        contact_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e3a8a; margin-top: 15px;")
        form_layout.addRow(contact_header)
        
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter your address")
        form_layout.addRow("Address:", self.address_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        form_layout.addRow("Phone:", self.phone_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        form_layout.addRow("Email:", self.email_input)
        
        # Photo Section
        photo_header = QLabel("Photo")
        photo_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e3a8a; margin-top: 15px;")
        form_layout.addRow(photo_header)
        
        self.photo_layout = QHBoxLayout()
        
        self.capture_btn = QPushButton("Capture Image")
        self.capture_btn.clicked.connect(self.capture_image)
        self.photo_layout.addWidget(self.capture_btn)
        
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        self.photo_layout.addWidget(self.upload_btn)
        
        form_layout.addRow(self.photo_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_btn = QPushButton("Save & Generate")
        self.save_btn.setObjectName("success")
        self.save_btn.clicked.connect(self.save_and_generate)
        button_layout.addWidget(self.save_btn)
        
        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.setObjectName("danger")
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push everything up
        layout.addStretch()

    def capture_image(self):
        # Similar to your IDCardGenerator's capture method
        camera = cv2.VideoCapture(0)
        
        while True:
            return_value, image = camera.read()
            image = cv2.flip(image, 1)
            cv2.imshow('Capture Image - Press ENTER to capture, ESC to cancel', image)
            
            key = cv2.waitKey(1)
            if key == 13:  # Enter key
                height, width = image.shape[:2]
                start_row, start_col = int(height * .25), int(width * .25)
                end_row, end_col = int(height * .80), int(width * .80)
                cropped_img = image[start_row:end_row, start_col:end_col]
                cv2.imwrite('temp_capture.jpg', cropped_img)
                
                # Update the generate tab's image
                if hasattr(self.generate_tab, 'update_photo'):
                    self.generate_tab.update_photo('temp_capture.jpg')
                
                break
            elif key == 27:  # ESC key
                break
        
        camera.release()
        cv2.destroyAllWindows()

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
                img.save('temp_upload.jpg')
                
                # Update the generate tab's image
                if hasattr(self.generate_tab, 'update_photo'):
                    self.generate_tab.update_photo('temp_upload.jpg')
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load image: {str(e)}")

    def save_and_generate(self):
        name = self.name_input.text()
        uid = self.id_input.text()
        department = self.department_combo.currentText()
        
        if not name or not uid:
            QMessageBox.warning(self, "Warning", "Please fill in all required fields")
            return
            
        # Update the generate tab with the new information
        self.generate_tab.update_fields(name, uid, department)
        
        # Switch to the generate tab
        self.tabs.setCurrentIndex(1)
        
        # Show success message
        self.status_bar.showMessage("Information saved successfully! You can now generate the ID card.")

    def clear_form(self):
        self.name_input.clear()
        self.id_input.clear()
        self.department_combo.setCurrentIndex(0)
        self.gender_combo.setCurrentIndex(0)
        self.address_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        
        # Clear any temporary image files
        for temp_file in ['temp_capture.jpg', 'temp_upload.jpg']:
            if os.path.exists(temp_file):
                os.remove(temp_file)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()