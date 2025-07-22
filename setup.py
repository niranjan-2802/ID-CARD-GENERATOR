from setuptools import setup, find_packages
import os

# Create necessary directories
os.makedirs('templates', exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('assets', exist_ok=True)

# Create a default icon file (you should replace this with your actual icon)
with open('assets/icon.png', 'wb') as f:
    pass  # This creates an empty file - replace with your actual icon

setup(
    name="idcard-generator",
    version="1.0.0",
    author="KREDIX XYPHER",
    author_email="",  # Add your email if needed
    description="Advanced ID Card Generator with QR Code and Custom Templates",
    long_description="""
    Advanced ID Card Generator with features including:
    - Multiple professional templates
    - Photo capture and editing
    - QR code generation
    - Customizable fields
    - Preview before saving
    """,
    url="https://github.com/kredix-xypher/ID-Card-Generator",
    packages=find_packages(),
    package_data={
        '': ['*.ui', '*.png', '*.jpg', '*.ttf'],
    },
    install_requires=[
        'PyQt5>=5.15.0',
        'Pillow>=8.0.0',
        'qrcode>=7.0',
        'opencv-python>=4.5.0',
        'numpy>=1.20.0'
    ],
    entry_points={
        'console_scripts': [
            'idcard-generator=index:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires='>=3.6',
    keywords='id card generator qr code pyqt5',
    project_urls={
        'Source': 'https://github.com/kredix-xypher/ID-Card-Generator',
        'Bug Reports': 'https://github.com/kredix-xypher/ID-Card-Generator/issues',
    },
)

print("\n" + "="*50)
print("ID Card Generator by KREDIX XYPHER")
print("GitHub: https://github.com/kredix-xypher")
print("="*50 + "\n")