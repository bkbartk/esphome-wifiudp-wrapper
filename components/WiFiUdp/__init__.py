"""
WiFiUdp Component for ESPHome

This component provides ESPHome-compatible WiFiUDP functionality for ESP-IDF projects.
It's a drop-in replacement for ESPHome's WiFiUdp.h that works with ESP-IDF.
"""

CODEOWNERS = ["@bkbartk"]
DEPENDENCIES = ["wifi"]
REQUIRED_ESP_IDF_VERSION = ">=4.4.0"

# This is a C++ component, so we don't need Python code here
# The actual implementation is in WiFiUdp.h and WiFiUdp.cpp 