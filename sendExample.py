from delta.publisher import ExampleDeltaPublisher, DeltaPublisherApplication, LOGGER
import logging

LOGGER.setLevel(logging.DEBUG)

if __name__ == "__main__":
    publisher = DeltaPublisherApplication(ExampleDeltaPublisher, {"action":"test"})
    publisher.run()