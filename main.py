from fetch_solar_data import FetchSolarData
from water_heater_plug import WaterHeaterPlug
import datetime, pandas as pd, os, time, sys
from geo_data import sunrise_sunset, lat_log_data
from create_summary import create_plot
from miio.exceptions import DeviceError, DeviceException

def main():
    current_time = datetime.datetime.now().replace(tzinfo=None)
    
    data = sunrise_sunset(*lat_log_data('Słopnice', 'Poland'),
                          timezone='Europe/Warsaw',
                          name='n',
                          region='PL')

    sunrise = data.sunrise.replace(tzinfo=None)
    sunset = data.sunset.replace(tzinfo=None) 

    inverter = FetchSolarData(os.environ.get('INVERTER_IP'))
    inverter.create_data_dir()
    heater = WaterHeaterPlug(os.environ.get('HEATER_IP'),
                             os.environ.get('HEATER_TK'))
    
    
    wattage = int(input("Specify heater threshold for switching on heater: (defaults to 2000):"))

    print("Starting automation...")

    while sunrise < current_time < sunset:

        if (prod := inverter.fetch()) > wattage:

            if not heater.get_plug_data['is_on']:
                try:
                    heater.on()
                    heater.set_led(True)
                except (DeviceException, DeviceError) as e:
                    print(f"Something went wrong!\n{e}")

            print(f"Heater is on current production: {prod}W.")

        else:
            try:
                heater.off()
                heater.set_led(False)
            except (DeviceException, DeviceError) as e:
                print(f"Something went wrong!\n{e}")

            print(f"Heater is off current production: {prod}W at {current_time}")
        time.sleep(15)
        current_time = datetime.datetime.now().replace(tzinfo=None)
    create_plot(str(datetime.date.today()), wattage)
    return wattage
    

if __name__ == '__main__':
    try:
        a = main()
    except KeyboardInterrupt:
        inpt = input('\nDo you want to exit execution? [y/n]').lower()
        match inpt:
            case 'y':
                print("Finishing automation...\nGoodbye!")
                wattage = int(input("Specify heater threshold for switching on heater: (defaults to 2000):"))
                create_plot(str(datetime.date.today()), wattage)
                sys.exit(0)
            case 'n':
                print('Keeping execution.')
            # case _:
                # print("Wrong answer!")
                # inpt = input('Do you want to exit execution? [y/n]')
