import sys
sys.path.append('.')

from CommandResponse import CommandResponse

rqst = "get sensor data: Temp, temp_1, 20"

resp = CommandResponse(rqst)
resp.get_response()
