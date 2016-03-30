from twisted.internet import defer

class BaseDeltaObject(object):
    _queue = "Undefined"
    _exchange = "Undefined"
    _routing_key = "Undefined"
    _AMQP_URL = None
    _APP_ID = None
            
    def getQueue(self):
        if self._queue == "Undefined":
            raise NotImplementedError("")
        return self._queue
    
    def getExchange(self):
        if self._exchange == "Undefined":
            raise NotImplementedError("")
        return self._exchange
    
    def getRoutingKey(self):
        if self._routing_key == "Undefined":
            raise NotImplementedError("")
        return self._routing_key

    def getAppId(self):
        if self._APP_ID == None:
            raise NotImplementedError("")
        return self._APP_ID
    
    def getAMQPUrl(self):
        if self._AMQP_URL == None:
            raise NotImplementedError()
        return self._AMQP_URL
    
    @defer.inlineCallbacks
    def establishChannel(self, connection):
        
        queueName = self.getQueue()
        exchangeName  = self.getExchange()
        routingKey = self.getRoutingKey()

        channel = yield connection.channel()
        exchange = yield channel.exchange_declare(exchange=exchangeName,type='topic')
        queue = yield channel.queue_declare(queue=queueName,
                                            auto_delete=False, exclusive=False)
        

        yield channel.queue_bind(exchange       = exchangeName,
                                 queue          = queueName,
                                 routing_key    = routingKey)
        yield channel.basic_qos(prefetch_count=1)

        return channel