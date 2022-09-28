# Solar Automation

Python script automating turning on/off Xiaomi Plug that manage water heater in my house.

Script is fetching solar data from Fronius Inverter via Fronius JSON API. It switch on water heater when production is more than 2kW,
or switch off heater when production is less than 2kW.

Additionaly script is collecting solar data and saving it to file when fetching for further analysis (Power usage, heater on duration time) etc.
