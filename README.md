# Solar Automation

Python script automating turning on/off Xiaomi Plug that manage water heater in my house.

Script is fetching solar data from Fronius Inverter via Fronius JSON API. It turns heater on when production is more than 2kW,
or turn heater off when production is less than 2kW.

Additionaly script is collecting solar data and saving it to file when fetching for further analysis (Power usage, heater on duration time) etc.