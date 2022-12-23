#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		self.configUtil = ConfigUtil()
		
		self.pollRate     = \
			self.configUtil.getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.POLL_CYCLES_KEY, 
				defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)


		# If self.useEmulator is True, 
		# 	log a simple message indicating that emulators will be used.
		# if self.useEmulator is False, 
		# 	log a simple message indicating that simulators will be used.
		self.useEmulator  = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.ENABLE_EMULATOR_KEY)
			
		self.locationID   = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, 
				key = ConfigConst.DEVICE_LOCATION_ID_KEY, 
				defaultVal = ConfigConst.NOT_SET)
			
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		# technically we only need 1 instance - important to set coalesce
		# to True and allow for misfire grace period
		self.scheduler = BackgroundScheduler()
	
		# id (str) - 此作业的唯一标识符the unique identifier of this job
		# name (str) – 这份工作的描述the description of this job
		# func – 要执行的可调用对象the callable to execute
		# args (tuple|list) – 可调用的位置参数positional arguments to the callable
		# kwargs (dict) – 可调用的关键字参数keyword arguments to the callable
		# coalesce (bool) – 是否在多个运行时间到期时只运行一次作业
		# trigger – 控制此作业计划的触发器对象
		# executor (str) - 将运行此作业的 executor 的名称
		# misfire_grace_time (int) – 允许该作业执行延迟的时间（以秒为单位）（None 表示“无论多晚都允许作业运行”）
		# max_instances (int) - 此作业允许的最大并发执行实例数
		# next_run_time (datetime.datetime) – 此作业的下一个计划运行时间
		self.scheduler.add_job( \
			self.handleTelemetry, 
			'interval', 
			seconds = self.pollRate, 
			max_instances = 2, 
			coalesce = True, 
			misfire_grace_time = 15)
		
		self.dataMsgListener = None
	
		# see PIOT-CDA-03-006 description for thoughts on the next line of code
		self._initEnvironmentalSensorTasks()
		
	
	def _initEnvironmentalSensorTasks(self):
		humidityFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
		humidityCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
		
		pressureFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		pressureCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		
		tempFloor       = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
		tempCeiling     = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		
		if not self.useEmulator:
			self.dataGenerator = SensorDataGenerator()
			
			humidityData = \
				self.dataGenerator.generateDailyEnvironmentHumidityDataSet( \
					minValue = humidityFloor, maxValue = humidityCeiling, useSeconds = False)
			pressureData = \
				self.dataGenerator.generateDailyEnvironmentPressureDataSet( \
					minValue = pressureFloor, maxValue = pressureCeiling, useSeconds = False)
			tempData     = \
				self.dataGenerator.generateDailyIndoorTemperatureDataSet( \
					minValue = tempFloor, maxValue = tempCeiling, useSeconds = False)
			
			self.humidityAdapter = HumiditySensorSimTask(dataSet=humidityData)
			self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)
			self.tempAdapter     = TemperatureSensorSimTask(dataSet = tempData)
		else:
			heModule = import_module('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', 'HumiditySensorEmulatorTask')
			heClazz = getattr(heModule, 'HumiditySensorEmulatorTask')
			self.humidityAdapter = heClazz()
			
			peModule = import_module('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', 'PressureSensorEmulatorTask')
			peClazz = getattr(peModule, 'PressureSensorEmulatorTask')
			self.pressureAdapter = peClazz()
			
			teModule = import_module('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', 'TemperatureSensorEmulatorTask')
			teClazz = getattr(teModule, 'TemperatureSensorEmulatorTask')
			self.tempAdapter = teClazz()	
			
	

	def handleTelemetry(self):
		humidityData = self.humidityAdapter.generateTelemetry()
		pressureData = self.pressureAdapter.generateTelemetry()
		tempData     = self.tempAdapter.generateTelemetry()
		
		humidityData.setLocationID(self.locationID)
		pressureData.setLocationID(self.locationID)
		tempData.setLocationID(self.locationID)
		
		logging.debug('Generated humidity data: ' + str(humidityData.getValue()))
		logging.debug('Generated pressure data: ' + str(pressureData.getValue()))
		logging.debug('Generated temp data: ' + str(tempData.getValue()))
		
		if self.dataMsgListener:
			self.dataMsgListener.handleSensorMessage(humidityData)
			self.dataMsgListener.handleSensorMessage(pressureData)
			self.dataMsgListener.handleSensorMessage(tempData)
	def setDataMessageListener(self, listener: IDataMessageListener):
		if listener:
			self.dataMsgListener = listener

	def startManager(self) -> bool:
		logging.info("Started SensorAdapterManager.")
		
		if not self.scheduler.running:
			self.scheduler.start()
			return True
		else:
			logging.info("SensorAdapterManager scheduler already started. Ignoring.")
			return False
	
	def stopManager(self) -> bool:
		logging.info("Stopped SensorAdapterManager.")
		
		try:
			self.scheduler.shutdown()
			return True
		except:
			logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
			return False
