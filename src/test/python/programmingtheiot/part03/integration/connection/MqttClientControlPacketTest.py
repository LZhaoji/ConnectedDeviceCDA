import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData 
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData 
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):

    @classmethod
    def setUpClass(self)->None:
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Executing the MqttClientControlPacketTest class...")
        
        self.cfg = ConfigUtil()
        self.mcc = MqttClientConnector()
        
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    @unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        # TODO: implement this test
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
        
        self.mcc.connectClient()
        
        sleep(delay + 5)
        
        self.mcc.disconnectClient()
    
    def testServerPing(self):
        # TODO: implement this test
        self.mcc.keepAlive = 10
        logging.info('\tChange MQTT Keep Alive to:' + str(self.mcc.keepAlive))
        delay = 20
        self.mcc.connectClient()
        for i in range(1,10):
            logging.info('this is ' + str(i) + 'th connecting from client')
            
            sleep(delay)
        
        self.mcc.disconnectClient()
        
    @unittest.skip("Ignore for now.")
    def testPubSub(self):
        # TODO: implement this test
        # 
        # IMPORTANT: be sure to use QoS 1 and 2 to see ALL control packets
        qoss = [1,2]
        for qos in qoss:
            logging.info('This is MQTT under QoS:\t' + str(qos))
            delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
            
            self.mcc.connectClient()
            self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos = qos)
            sleep(5)
            
            self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST: This is the CDA message payload.", qos = qos)
            sleep(5)
            
            self.mcc.unsubscribeFromTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
            sleep(5)
            
            sleep(delay)
            
            self.mcc.disconnectClient()