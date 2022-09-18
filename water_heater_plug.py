import miio.chuangmi_plug
import os

class WaterHeaterPlug(miio.chuangmi_plug.ChuangmiPlug):

    def __init__(self, 
                 ip: str = None,
                 token: str = None,
                 start_id: int = 0, 
                 debug: int = 0, 
                 lazy_discover: bool = True, 
                 timeout: int = None, *, 
                 model: str = None) -> None:

        super().__init__(ip, 
                         token, 
                         start_id, 
                         debug, 
                         lazy_discover, 
                         timeout, 
                         model=model)
        
    @property
    def get_plug_data(self) -> dict:
        """
        Retrieve data from water heater plug.

        Returns:
            dict: Plug properties.
        """
        plug_status = self.status()
        data = {'is_on': plug_status.is_on}
        data['led'] = plug_status.led
        data['load_power'] = plug_status.load_power
        return data



if __name__ == '__main__':
    plug = WaterHeaterPlug(os.environ.get('HEATER_IP'),
                           os.environ.get('HEATER_TK'))
    print(plug.get_plug_data)
    plug.on()
    plug.set_led(True)
    print(plug.get_plug_data)