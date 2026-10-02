---
title: "ESP32 IN/OUT Solder Bridge for 5V"
date: 2026-09-06
tiltags: ["electronics", "esp32", "hardware", "microcontrollers"]
summary: "Some ESP32 boards require you to solder bridge the IN/OUT pad to get 5V output from the 5V pin."
url: "/til/esp32-in-out-solder-bridge"
---

{{< photocaption src="esp32-solder-5v.jpg" alt="Solder in/out pads for 5v on esp32 boards" width="80%" >}}Solder pads on ESP32 dev board for 5v{{< /photocaption >}}


Today I learned that on some [ESP32 development boards](https://l.rishikeshs.com/esp32board), the 5V pin doesn't actually output 5V by default. 

There's a small solder pad labeled "IN/OUT" that you need to bridge to connect USB power to the 5V pin.

Without this bridge, the 5V pin is disconnected and you won't be able to power external components from it. A quick dab of solder across the pad fixes it and then you can draw 5V. Otherwise you will alsways get 3.3V

I didn't know this and for few hours I thought something was wrong with my board!