idf_component_register(
    SRCS "WiFiUdp.cpp"
    INCLUDE_DIRS "."
    REQUIRES esp_wifi esp_netif lwip esp_event
) 