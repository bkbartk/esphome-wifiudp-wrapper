# WiFiUDP Wrapper for ESP-IDF

A drop-in replacement for ESPHome's `WiFiUdp.h` that provides ESPHome-compatible UDP functionality for ESP-IDF projects.

## Overview

This wrapper implements the ESPHome WiFiUDP interface using ESP-IDF's native socket API, allowing you to use ESPHome components that depend on `WiFiUdp.h` in ESP-IDF projects without any code modifications.

## Features

- **ESPHome Compatibility**: Drop-in replacement for ESPHome's WiFiUdp.h
- **ESP-IDF Integration**: Built on top of ESP-IDF's native socket API
- **Multicast Support**: Full multicast UDP functionality
- **Non-blocking Operations**: Asynchronous packet handling
- **Memory Management**: Automatic buffer management and cleanup
- **Error Handling**: Comprehensive error reporting and recovery

## Files

- `WiFiUdp.h` - Header file with ESPHome-compatible interface
- `WiFiUdp.cpp` - Implementation using ESP-IDF socket API

## Installation

### Method 1: Direct Copy (Recommended for ESPHome)

1. **Copy the files** to your ESPHome project:
   ```bash
   cp WiFiUdp.h /path/to/your/esphome/project/
   cp WiFiUdp.cpp /path/to/your/esphome/project/
   ```

2. **Include in your ESPHome configuration**:
   ```yaml
   # In your ESPHome YAML file
   external_components:
     - source: .
       components: [ "WiFiUdp" ]
   ```

### Method 2: ESP-IDF Component

1. **Create a components directory**:
   ```bash
   mkdir -p components/wifi_udp_wrapper
   cp WiFiUdp.h components/wifi_udp_wrapper/
   cp WiFiUdp.cpp components/wifi_udp_wrapper/
   ```

2. **Create CMakeLists.txt** in the component directory:
   ```cmake
   idf_component_register(
       SRCS "WiFiUdp.cpp"
       INCLUDE_DIRS "."
       REQUIRES esp_wifi esp_netif lwip esp_event
   )
   ```

## Usage

### Basic Usage

Simply include the header and use the same API as ESPHome:

```cpp
#include "WiFiUdp.h"

WiFiUDP udp;

// Start UDP server
if (udp.begin(8888)) {
    ESP_LOGI(TAG, "UDP server started on port 8888");
}

// Send packet
if (udp.beginPacket("192.168.1.100", 8888)) {
    udp.write("Hello from ESP32!");
    udp.endPacket();
}

// Receive packet
int packetSize = udp.parsePacket();
if (packetSize) {
    char buffer[1024];
    int bytesRead = udp.read(buffer, sizeof(buffer) - 1);
    buffer[bytesRead] = '\0';
    ESP_LOGI(TAG, "Received: %s", buffer);
}
```

### ESPHome Integration

In your ESPHome component that requires `WiFiUdp.h`:

```cpp
// Instead of: #include "WiFiUdp.h"
#include "WiFiUdp.h"  // This now uses our wrapper

class MyComponent : public Component {
private:
    WiFiUDP udp;
    
public:
    void setup() override {
        // Your existing ESPHome code works unchanged
        if (udp.begin(8888)) {
            ESP_LOGI(TAG, "UDP server started");
        }
    }
    
    void loop() override {
        // Your existing ESPHome code works unchanged
        int packetSize = udp.parsePacket();
        if (packetSize) {
            // Handle received packet
        }
    }
};
```

### Multicast Support

```cpp
WiFiUDP udp;

// Join multicast group
if (udp.beginMulticast(8888, "239.255.255.250", "192.168.1.100")) {
    ESP_LOGI(TAG, "Multicast server started");
}

// Receive multicast packets
while (true) {
    int packetSize = udp.parsePacket();
    if (packetSize) {
        ESP_LOGI(TAG, "Multicast packet: %d bytes from %s:%d", 
                 packetSize, udp.remoteIP(), udp.remotePort());
        
        char buffer[1024];
        int bytesRead = udp.read(buffer, sizeof(buffer) - 1);
        buffer[bytesRead] = '\0';
        ESP_LOGI(TAG, "Content: %s", buffer);
    }
    
    vTaskDelay(pdMS_TO_TICKS(100));
}
```

## API Reference

### Constructor/Destructor
- `WiFiUDP()` - Create UDP instance
- `~WiFiUDP()` - Cleanup and close socket

### Server Operations
- `bool begin(uint16_t port)` - Start UDP server on port
- `bool beginMulticast(uint16_t port, const char* multicast_ip, const char* interface_ip)` - Start multicast server
- `void stop()` - Stop server and close socket

### Client Operations
- `bool beginPacket(const char* ip, uint16_t port)` - Prepare packet for sending
- `bool beginPacket(uint32_t ip, uint16_t port)` - Prepare packet with IP as uint32_t
- `bool endPacket()` - Send prepared packet

### Data Operations
- `size_t write(uint8_t byte)` - Write single byte
- `size_t write(const uint8_t* buffer, size_t size)` - Write buffer
- `size_t write(const char* str)` - Write string

### Receive Operations
- `int parsePacket()` - Check for incoming packet
- `int available()` - Get available bytes
- `int read()` - Read single byte
- `int read(uint8_t* buffer, size_t size)` - Read into buffer
- `int read(char* buffer, size_t size)` - Read into char buffer
- `int peek()` - Peek at next byte
- `void flush()` - Flush receive buffer

### Information
- `const char* remoteIP()` - Get sender IP
- `uint16_t remotePort()` - Get sender port
- `bool connected()` - Check if connected
- `uint16_t localPort()` - Get local port
- `const char* localIP()` - Get local IP
- `void setTimeout(int timeout_ms)` - Set receive timeout

## ESPHome Configuration Example (GitHub External Component)

You can use this wrapper directly from GitHub as an `external_components` source in ESPHome. Example:

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/bkbartk/esphome-wifiudp-wrapper
    components: ["WiFiUdp"]

esphome:
  name: my_udp_device
  platform: ESP32
  board: esp32dev

wifi:
  ssid: "YourWiFiSSID"
  password: "YourWiFiPassword"

# Your component that uses WiFiUdp.h will work without changes
```

## Building with ESP-IDF

If you're building directly with ESP-IDF:

1. **Add to your CMakeLists.txt**:
   ```cmake
   target_sources(${COMPONENT_TARGET} PRIVATE
       "WiFiUdp.cpp"
   )
   
   target_include_directories(${COMPONENT_TARGET} PRIVATE
       "."
   )
   
   target_link_libraries(${COMPONENT_TARGET}
       esp_wifi
       esp_netif
       lwip
       esp_event
   )
   ```

2. **Include in your source**:
   ```cpp
   #include "WiFiUdp.h"
   ```

## Troubleshooting

### Common Issues

1. **Compilation Errors**:
   - Ensure ESP-IDF is properly installed and sourced
   - Check that all required ESP-IDF components are linked

2. **Runtime Errors**:
   - **WiFi not connected**: Ensure WiFi is initialized before using UDP
   - **Port already in use**: Try a different port number
   - **Multicast not working**: Ensure network supports multicast

3. **ESPHome Integration**:
   - Make sure the files are in the correct location
   - Check that the external_components section is properly configured

### Debugging

Enable debug logging in your ESP-IDF project:

```cpp
#define LOG_LOCAL_LEVEL ESP_LOG_DEBUG
#include "esp_log.h"
```

## Compatibility

- **ESP-IDF**: v4.4+ and v5.0+
- **ESP32**: All variants (ESP32, ESP32-S2, ESP32-S3, ESP32-C3)
- **ESPHome**: All versions that use WiFiUdp.h

## License

This project is licensed under the MIT License.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: See the header file for detailed API documentation
- **Examples**: Check the usage examples above

## Changelog

### v1.0.0
- Initial release
- ESPHome-compatible WiFiUDP wrapper
- ESP-IDF native implementation
- Multicast support
- Comprehensive error handling 