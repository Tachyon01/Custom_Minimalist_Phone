# Custom Minimalist Phone
HackGT 2025 Project by Ayush Banerjee & Pulkit Goel

## Inspiration
Modern phones are filled with distractions, such as social media, and this product goes back to the basics with an interesting twist. The fundamental features of this simple yet innovative product are:
Wi-Fi calling, SMS texting, mobile-interface buttons, LCD screen, and status LEDs.

## What Does it Do
This product has the basic phone features, but it also has a new feature, which is hot-swappable sensor integration. The use case for this product is not only being a minimalist device, perfect for users looking for a digital detox, but it can also be used by technicians in industry who rely on sensors to log data. 

With this device, they can easily swap their sensors, gather data passively, and have fewer distractions, enabling them to do their job more safely and easily. A phone with plug-and-play sensor integration has not been implemented before, and this product is the next step towards leveraging powerful computing in the field.

## The Building Process
The Raspberry Pi is mounted on a custom-designed PCB with a 16x2 LCD, keypad buttons, and slots for sensors.
From designing the PCB, breadboarding, and Python script, they were all custom-developed in this Hackathon.

## Challenges We Ran Into
The PCB machine was not working due to the lack of the solder mask in the HIVE ECE Makerspace at Georgia Tech, so we ended up removing some features, such as a keypad to dial phone numbers and audio circuitry for a speaker. We switched to breadboarding the product with the Raspberry Pi, LCD, Grove connector sensors, LEDs, and a few buttons. 

## Our Accomplishments
We were able to implement the calling, texting, and sensor integration, which were our features for the product's MVP. We implemented calling and texting through the Pi's Wi-Fi capabilities and the Twilio API, which allows calling and texting over Wi-Fi.

## What We Learned
We attempted to manufacture a PCB version of this device, but we had a lot of trouble soldering and assembling the components due to the lack of electroplating and soldermask in the makerspace PCB fabrication machine. We also learned to take the feature addition step-by-step to ensure all parts are properly made before thinking about more complicated features.

## Next Steps for a Custom Minimalist Phone
We will update the PCB to accommodate additional slots for IoT devices, manufacture a legitimate PCB that houses all the essential components, and add custom circuitry to make the phone more interactive, such as a biometric sensor and an audio speaker system.
