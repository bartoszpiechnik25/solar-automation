from fetch_solar_data import FetchSolarData
from water_heater_plug import WaterHeaterPlug
import datetime, pandas as pd, os, time, sys
from geo_data import sunrise_sunset, lat_log_data
from create_summary import create_plot

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

    print("Starting automation...")

    while sunrise < current_time < sunset:

        if (prod := inverter.fetch()) > 2000:
            heater.on()
            heater.set_led(True)

            print(f"Heater is on current production: {prod}W.\nPower load:\
             {heater.get_plug_data['load_power']}")
        else:
            heater.off()
            heater.set_led(False)
            print(f"Heater is off current production: {prod}W at {current_time}")
        time.sleep(15)
        current_time = datetime.datetime.now().replace(tzinfo=None)
    create_plot(str(datetime.date.today()))
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        inpt = input('\nDo you want to exit execution? [y/n]').lower()
        match inpt:
            case 'y':
                print("Finishing automation...\nGoodbye!")
                create_plot(str(datetime.date.today()))
                sys.exit()
            case 'n':
                print('Keeping execution.')
            # case _:
                # print("Wrong answer!")
                # inpt = input('Do you want to exit execution? [y/n]')
