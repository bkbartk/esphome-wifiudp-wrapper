idf_component_register(
    SRCS "src/WiFiUdp.cpp"
    INCLUDE_DIRS "."
    REQUIRES esp_wifi esp_netif lwip esp_event
)

# Make WiFiUdp.h available globally for other components
target_include_directories(${COMPONENT_LIB} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
) 