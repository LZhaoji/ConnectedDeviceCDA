#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

from coapthon import defines
from coapthon.resources.resource import Resource

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData

class GetTelemetryResourceHandler(Resource,ITelemetryDataListener):
	"""
	Observable resource that will collect telemetry based on the given
	name from the data message listener implementation.
	
	ITelemetryDataListener defines a single method that provides a callback
	function for the DeviceDataManager to use to send the latest SensorData 
	to the implementing class.
	
	NOTE: Your implementation will likely need to extend from the selected
	CoAP library's observable resource base class.
	
	"""

	def __init__(self, name: str = ConfigConst.SENSOR_MSG, coap_server = None):
		super(GetTelemetryResourceHandler, self).__init__( \
			name, coap_server, visible = True, observable = True, allow_children = True)
		
		self.pollCycles = \
			ConfigUtil().getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, \
				key = ConfigConst.POLL_CYCLES_KEY, \
				defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
			
		self.sensorData = None
		self.dataUtil = DataUtil()
		
		# for testing
		self.payload = "GetSensorData"
		
	def onSensorDataUpdate(self, data: SensorData = None) -> bool:
		pass
	
	def render_GET_advanced(self,request,response):
		if request:
			response.code = defines.Codes.CONTENT.number
			
			if not self.sensorData:
				response.code = defines.Codes.EMPTY.number
				self.sensorData = SensorData()
				
			jsonData = DataUtil().sensorDataToJson(self.sensorData )
			
			response.payload = (defines.Content_types["application/json"], jsonData)
			response.max_age = self.pollCycles
	
			# 'changed' will be discussed in a later exercise
			self.changed = False
				
		return self, response
	