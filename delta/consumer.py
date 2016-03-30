# -*- coding:utf-8 -*-
from delta.lib import BaseDeltaObject
from delta.log import LOGGER
import pika
from pika import exceptions
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol,task

class BaseDeltaConsumer(BaseDeltaObject):
    
    @defer.inlineCallbacks
    def consumeChannel(self, channel):
        queueName = self.getQueue()
        queue_object, consumer_tag = yield channel.basic_consume(queue=queueName,
                                                                 no_ack=False)
        return queue_object

    def getReadLoop(self, queue_object):
        loop = task.LoopingCall(
            self.readMessage, queue_object)
        return loop

    @defer.inlineCallbacks
    def readMessage(self, queue_object):
        ch,method,properties,body = yield queue_object.get()
        if body:
            message = "Received message with contents of {body}".format(body=body)
            LOGGER.info(message)
            LOGGER.info("Running success script...")
            result = yield self.runSuccess(body)
            LOGGER.info("Success script finished. Returned {result}".format(result=result))
        yield ch.basic_ack(delivery_tag=method.delivery_tag)
        
        
    def runSuccess(self, body):
        return None
    
class ExampleConsumer(BaseDeltaConsumer):
    _queue = "info"
    _exchange = "info"
    _routing_key = "info"


def ebPrint(result):
    print("Error recieved:")
    print(result)
    print(dir(result))
    reactor.stop()
    

class DeltaConsumerApplication(object):
    
    def __init__(self, Consumer, hostname="127.0.0.1"):
        self.consumer = Consumer()
        self.hostname = hostname

    def run(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(host=self.hostname, port=5672,
            virtual_host='/',credentials=credentials)
        cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, parameters)
        d = cc.connectTCP(self.hostname, 5672)
        
        d.addCallback(lambda protocol: protocol.ready)
        d.addCallback(self.consumer.establishChannel)
        d.addCallback(self.consumer.consumeChannel)
        d.addCallback(self.consumer.getReadLoop)
        d.addCallback(lambda loop: loop.start(0.01))
        
        d.addErrback(ebPrint)
        reactor.run()