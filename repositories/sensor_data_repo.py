from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

class InfluxClientRepository:
    """ A simple wrapper around the InfluxDBClient to handle writing and querying data. """
    def __init__(self,token,org,bucket, host, port): 
        self._org=org 
        self._bucket = bucket
        self._client = InfluxDBClient(url=f"http://{host}:{port}", token=token)


    def write_data(self,data,write_option=SYNCHRONOUS):
        """ Write Data to InfluxDB using the provided write option (SYNCHRONOUS or ASYNCHRONOUS)"""

        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org , data,write_precision='s')
    
    def query_data(self,query):
    
        query_api = self._client.query_api()
        result = query_api.query(org=self._org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value(), record.get_field()))
        print(results)
        return results
    
