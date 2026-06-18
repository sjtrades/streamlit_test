MAP_CONFIG = {
    "AmbroseValley": {
        "scale": 900,
        "origin_x": -370,
        "origin_z": -473,
        # "image": "minimaps/AmbroseValley_Minimap.png"
        "image": "minimaps/low/AmbroseValley_Minimap.jpg",
    },
    "GrandRift": {
        "scale": 581,
        "origin_x": -290,
        "origin_z": -290,
        # "image": "minimaps/GrandRift_Minimap.png"
        "image": "minimaps/low/GrandRift_Minimap.jpg",
    },
    "Lockdown": {
        "scale": 1000,
        "origin_x": -500,
        "origin_z": -500,
        # "image": "minimaps/Lockdown_Minimap.jpg"
        "image": "minimaps/low/Lockdown_Minimap.jpg",
    },
}

HEATMAP_CONFIG = {
    "AmbroseValley": {
        "High Traffic": {"size": 4, "color": "yellow", "opacity": 0.1, "symbol":"circle"},
        "Kill Zones": {"size": 8, "color": "red", "opacity": 0.3, "symbol":"x"},
        "Death Zones": {"size": 8, "color": "orange", "opacity": 0.5, "symbol":"diamond"},
    },
    "GrandRift": {
        "High Traffic": {"size": 4, "color": "yellow", "opacity": 0.3, "symbol":"circle"},
        "Kill Zones": {"size": 10, "color": "red", "opacity": 0.5, "symbol":"x"},
        "Death Zones": {"size": 10, "color": "orange", "opacity": 0.6, "symbol":"diamond"},
    },
    "Lockdown": {
        "High Traffic": {"size": 4, "color": "yellow", "opacity": 0.2, "symbol":"circle"},
        "Kill Zones": {"size": 10, "color": "red", "opacity": 0.4, "symbol":"x"},
        "Death Zones": {"size": 10, "color": "orange", "opacity": 0.5, "symbol":"diamond"},
    },
}
