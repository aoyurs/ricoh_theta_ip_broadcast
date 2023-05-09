#!/usr/bin/env python3

""" Example of browsing for a service (in this case, HTTP) """
import binascii
import socket
from loguru import logger
from zeroconf import ServiceStateChange, Zeroconf, ServiceBrowser


def on_service_state_change(zeroconf, service_type, name, state_change):
    logger.debug("Service %s of type %s state changed: %s" %
                 (name, service_type, state_change))

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            logger.debug("  Address: %s:%d" %
                         (socket.inet_ntoa(info.address), info.port))
            logger.debug("  Weight: %d, priority: %d" % (info.weight, info.priority))
            logger.debug("  Server: %s" % (info.server,))
            if info.properties:
                logger.debug("  Properties are:")
                for key, value in info.properties.items():
                    logger.debug("    %s: %s" % (key, value))
            else:
                logger.debug("  No properties")
        else:
            logger.debug("  No info")
        logger.debug('\n')


class MyListener:

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.debug(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.debug(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        info_addresses_bytes = info.addresses[0]
        logger.debug(f"info_addresses_bytes:{info_addresses_bytes}")
        bytes_count = len(info_addresses_bytes)
        ip = ''
        for index, bytex in enumerate(info_addresses_bytes):
            ip += str(bytex)
            if index != bytes_count - 1:
                ip += '.'
        logger.debug(f"ip:{ip}")
        # binascii.hexlify(b_text)


if __name__ == '__main__':
    pass
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_osc._tcp.local.", listener)
    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()
