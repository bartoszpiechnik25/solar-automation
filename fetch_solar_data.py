import requests, os, time, pandas as pd
from datetime import date
from requests.exceptions import ConnectionError

class FetchSolarData:

    def __init__(self, inverter_IP: str) -> None:
        """
        Object fetching and saving data to DataFrame.

        Args:
            inverter_IP (str, optional): Inverter IP
                 variable 'INVERTER_IP'.
        """
        self._inverter_ip = inverter_IP

        self._endpoints =\
             ["/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System"]
        self._data_frame = None
        self._data_path = os.path.join(os.getcwd(), 'data', str(date.today()))
    

    def create_data_dir(self):
        """
        Create directory for data to be stored.

        Raises:
            FileExistsError: If directory already exists.
        """
        try:
            os.makedirs(self._data_path)
        except FileExistsError:
            text =\
            f"Directory {os.path.basename(self._data_path)} already exists!"
            print(text)
    
    
    def load_df(self, data: dict) -> None:
        """
        Loads DataFrame from file and concatenate data or create new one.

        Args:
            data (dict): Data to be filled into DataFrame or concatenated into\
                 existing.

        Raises:
            ValueError: If DataFrame is empty, create new one.
        """
        #DF name
        name = f'{str(date.today())}.pickle'
        #Df path
        dir = os.path.join(self._data_path, name)

        try:
            #Read df, if not found raise FileNotFoundError
            self._data_frame = pd.read_pickle(dir)
            #If empty raise Value Error and create new df.
            if self._data_frame.empty:
                raise ValueError         
        except (FileNotFoundError, ValueError):
            #Create new
            self._data_frame = pd.DataFrame([data])
        else:
            #Create auxilarity df to be concatenated with loaded df.
            conc = pd.DataFrame([data])
            self._data_frame = pd.concat([conc, self._data_frame],
                                        ignore_index=True)
        finally:
            #Save to file
            self._data_frame.to_pickle(dir)


    def fetch(self):
        """
        Fetch data from Fronius JSON API and saves it to pd.DataFrame.

        Returns:
            _type_: _description_
        """
        #url for data to be fetch.
        self.url = "http://" + self._inverter_ip + self._endpoints[0]

        #Request data until suceed.
        request = None
        while request is None:
            try:
                request = requests.get(self.url, timeout=10)
                request.raise_for_status()
            except ConnectionError:
                request = None
                print('Fetching failed trying again...')

        #Return fetched data
        body, head = request.json()['Body']['Data'], request.json()['Head']

        #Create dict to passed into pd.DataFrame constructor.
        to_df = {}
        for key, value in body.items():
            to_df[f"{key}({value['Unit']})"] = value['Values'].get('1')
        to_df['Time'] = pd.Timestamp(head['Timestamp'])

        #Fill df with fetched data.
        self.load_df(to_df)

        current_production = body['PAC']['Values'].get('1')

        return current_production


if __name__ == '__main__':
    d = FetchSolarData(os.environ.get('INVERTER_IP'))
    d.create_data_dir()
    # d.fetch()
    # time.sleep(3)
    # d.fetch()
    # time.sleep(5)
    print(d.fetch())
    