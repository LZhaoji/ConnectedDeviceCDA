# Lab Module 12 - Semester Project Proposal

## Description

Describe your idea in 1 paragraph (at least 2 or 3 sentences).

In Final Project, I decide to monitor my apartment about Humidity, Temperature and Pressure.
Constrained Device Sensor measures indoor temperature, humidity and pressure, and Actuator is 
used to remind me that if a certain value falls below a threshold after analyzing sensor data ,which is transformed under CoAP to the GDA and GDA do some action under MQTT to the top, by cloud tier, first make an alert and then automatically react, such as air conditionor on and off.

## What - The Problem 

What problem are you trying to solve and why does it matter? Write 1 to 2 paragraphs in response.

The main problem I want to solve is temperature detection, because it is coming to winter, the temperature is very low and I have poor sleep quality, if the air conditioner can be turned on in the middle of the night when it is very cold, I will probably be able to sleep well Sleep. The humidity is actually checked after the air conditioner is turned on. Because when the indoor temperature increases, the humidity may drop, and the actuator can turn on the humidifier, which further improves the quality of my sleep.


## Why - Who Cares? 

Why do you care about this particular problem? Write 1 to 2 paragraphs in response.

Getting quality sleep isn't just for me, it's important for everyone. A good night's sleep can improve a person's productivity the next day. The environment people stay in plays an important role. People won't get a deep sleep if they are breating cold and dry air.
If an actuator can help people to detect and conntrol these, people will do more what they are looking forward or concentrate on, which means it will improve our effectivity and living happiness.


## How - Expected Technical Approach

How do you plan to tackle this problem technically?

Include a high-level design diagram depicting your planned technical approach - it does not need to be final, but it must include the CDA, GDA, and cloud services you plan to use, as well as the protocol(s) you will use for communicating between the devices and the cloud.

Write 1 to 2 paragraphs describing your diagram.

Because most of what I'm describing happens at night, it may be necessary to set a boolean value to indicate whether the current time is between 5pm and 12pm to tell CDA whether to start monitoring. When within this time frame, the CDA begins to perform light, temperature and humidity detection. Here, I don't want CDA to check all the time, because no one wants their air conditioner or lights to be on and off or adjust the brightness and temperature all the time. For example, when detecting the temperature, if the values of the first three temperature measurements (measured every 20 minutes) after turning on the air conditioner are all within a normal range (the range of values suitable for my activities), let the subsequent measurements be half a hourly.
For data transfer between CDA and GDA, I choose to use the connectionless based CoAP transport protocol. In the case I described, GDA may only need to handle the POST and GET methods; and CDA not only uses the PUT method for GDA, but also uses the OBSERVER method to allow multiple CDAs in the house price to obtain the RESPONSE of GDA .
For the data transfer from GDA to CLOUD, I choose to use the MQTT transport protocol, which is a connection-oriented transport protocol used to transmit data received from CDA to CLOUD for data analysis.
When performing data analysis in CLOUD, the received data can be used to determine where the current data is from the CDA (such as my room, living room, kitchen or basement). For different areas, when calculating data , the tolerance range for judging whether the data is within the preset range may be different. For example, the CDA placed in the basement may feel the temperature drop earlier, but I can't feel this temperature change in the room, so I don't need to adjust the air conditioner temperature. The platforms that CLOUD can use are: Ubidots.

## Results - Expected Outcomes 

If your project is successful, what outcome do you expect (e.g. what will happen if everything works)? Write 1 to 2 paragraphs describing your expected outcomes.

For this winter, when the temperature drops to a certain value, my air conditioner can automatically turn on and maintain a certain temperature, and can automatically turn off in the middle of the night, leaving me some electricity bills. When the light goes down, the system can turn on the lights for me ahead of time due to the time the sun goes down.

I can also know through the analysis report of CLOUD to know when the temperature drops the fastest, when the light drops the fastest, and how much air-conditioning electricity I will spend each day. This allows me to have a clear understanding of my work and life status.

EOF.
