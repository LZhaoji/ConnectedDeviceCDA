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

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData

class UpdateActuatorResourceHandler(Resource):
	"""
	Standard resource that will handle an incoming actuation command,
	and return the command response.
	
	NOTE: Your implementation will likely need to extend from the selected
	CoAP library's resource base class.
	
	"""

	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.dataMsgListener = dataMsgListener
		self.dataUtil = DataUtil()
		
	def render_PUT_advanced(self, request, response):
		if request:
			# Check payload
			# Check content-type (should be JSON)
			requestPayload = request.get_payload()	
			actuatorCmdData = self.dataUtil.jsonToActuatorData(requestPayload)
			
			response.payload = self._createResponse(response = response,data = actuatorCmdData)
			response.max_age = self.pollCycles
	
	def _createResponse(self,response = None,data: ActuatorData = None) -> str:
		actuatorResponseData = self.dataMsgListener.handleActuatorCommandMessage(data)
		
		if not actuatorResponseData:
			actuatorResponseData = ActuatorData()
			actuatorResponseData.updateData(data)
			actuatorResponseData.setAsResponse()
			actuatorResponseData.setStatusCode(-1)
			
			response.code = defines.Codes.PRECONDITION_FAILED.number
		else:
			response.code = defines.Codes.CHANGED.number
			
		jsonData = self.dataUtil.actuatorDataToJson(actuatorResponseData)
		
		return (defines.Content_types["application/json"],jsonData)
		
		