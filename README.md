# Stead-Watch

The purpose of this application is to provide an easy and modular way to manage your homestead. 


## Background
Like many people, I enjoy having a homestead but I still have a full time job. I love knowing where my food comes from and having a part in its production but I do not do this full time. When you have "part-time" homestead, you have to be extremely efficient with your time - this involes configuring your homestead in the most efficient way possible.

I have found that having a simple monitoring system for animal feed, animal water, animal pen gate closures allows you to prioritize your time better. In instances where you need to quickly perform your homestead chores, its nice to know when the chickens are topped off on food and their coop door is open, without necessarily having to run out to the coop to check. 

My goal is for this project to remain open source, so that homesteaders can start managing their homestead without significant overhead. Everyone should have the ability to have a hand in how their food is made (if they choose) and I would love to help lower the barrier to entry by freeing up time for people. 
<br><br>


# Project Design Overview

The system will consist of a "Base Station", a data relay , and several sensor modules. 

### Base Station
The base station is where all of the heavy lifting happens in this project. It will contain a basic FastApi Backend that will ingest http request from the data relay and store the data into a time series based DB (InfluxDB).

### Data Relay
This will consist of an ESP32 Microcontroller that has a LoRa (Long range Radio Transmission)  module attached. LoRa is how the sensors will transmit the data to the relay. LoRa is low power method of communication and it is capable of transmitting data EXTREMELY far ( More info to follow). The relay will receive data and convert the data ( As well as the metadata stating where the data came from) into an http request which is then sent to the Base Station. The relay may also have an NFC reader enabled, which will allow easy registration of new sensors.

### Sensor Modules
The stations will consist of simple microcontroller boards attached to LoRa  module, the appropriate sensor, an NFC tag for registration with the relay, and a small battery. They will be packaged in a waterproof housing capable of withstanding the elements. As of right now, the modules will have very basic controls enabled to allow for the adjustment of how often data is sent ( More often means less battery life) as well a indicator for the battery life. The Sensor Modules will send battery life information with the sensor data to allow for the base station to have up to date battery information. 


Tips to run 

Run this command in the steadwatch repo
`python -m uvicorn app.main:app --reload`