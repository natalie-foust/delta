from delta.consumer import ExampleConsumer, DeltaConsumerApplication
import logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app = DeltaConsumerApplication(ExampleConsumer)
    app.run()