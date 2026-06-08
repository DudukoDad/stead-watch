from influxdb_client import InfluxDBClient, Point
from influxdb_client_3 import InfluxDBClient3
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxClientRepository:
    """ A simple wrapper around the InfluxDBClient to handle writing and querying data. """
    def __init__(self,token,org, database, host, port): 
        self.database = database
        self._client = InfluxDBClient3(
                        host=f"http://{host}:{port}",
                        token=token,
                        org=org,
                        database=database,
                        auth_scheme="Bearer"
                        )
        # self._client = InfluxDBClient3(url=f"http://{host}:{port}", token=token)


    def create(self, sensor_data: Point) -> None:
        """ Write Data to InfluxDB using the provided write option (SYNCHRONOUS or ASYNCHRONOUS)"""

        # write_api = self._client.write_api(write_option)
        print(sensor_data)
        r = self._client.write( record=sensor_data)
        print(r)
    
    @staticmethod
    def _format_query(device_id: str, location: str, bucket: str, start="-1h"):
        """ Helper method to format a Flux query for InfluxDB based on device_id and location. """
        query = f'''
        from(bucket: "{bucket}")
          |> range(start: {start})
          |> filter(fn: (r) => r["device_id"] == "{device_id}")
          |> filter(fn: (r) => r["location"] == "{location}")
        '''
        return query

    def get_by_id(self,id: str, location: str) -> list[tuple]:
        measurement_name = 'homestead'
        target_id = id
        # Construct the SQL query
        # Note: replace 'id_column_name' with your actual tag or field name for the ID
        query = f"SELECT * FROM {measurement_name} WHERE device_id = '{target_id}'"

        # Execute the query and convert to a Pandas DataFrame
        table = self._client.query(query)
        df = table.to_pandas()
        return df.to_dict(orient='records')
    