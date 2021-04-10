import configparser
import time
import sys
import logutil

from gpio.gpio_manager import GPioManager
from gpio.gpio_manager_dummy import GPioManagerDummy
from mqtt.mqtt_manager import MqttManager

if __name__ == '__main__':
    default_config = 'config.ini'
    if len(sys.argv) > 1:
        profile = sys.argv[1]
        if profile.startswith('--profile='):
            default_config = 'config_' + profile.split("=")[1] + '.ini'

    config = configparser.ConfigParser()
    config.read(default_config)
    if config['default']['TEST_MODE'] == "true":
        logutil.info("RUNNING ON TEST MODE")
        manager = GPioManagerDummy(config)
    else:
        manager = GPioManager(config)

    mqtt = MqttManager(config)

    ON_THRESHOLD = int(config['gpio']['ON_THRESHOLD'])
    OFF_THRESHOLD = int(config['gpio']['OFF_THRESHOLD'])
    SLEEP_INTERVAL = int(config['gpio']['SLEEP_INTERVAL'])

    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    last_status = False
    Run = True

    manager.turnOFF()
    while Run:
        try:
            must_spin = last_status
            temp = manager.get_temp()

            if last_status:
                logutil.info("RUNNING...")

            if not last_status:
                logutil.info("OFF...")

            if temp >= ON_THRESHOLD:
                must_spin = True

            if temp <= OFF_THRESHOLD:
                must_spin = False

            if must_spin and must_spin != last_status:
                logutil.info("Ligando...")
                manager.turnOn()

            if not must_spin and must_spin != last_status:
                logutil.info("Desligando...")
                manager.turnOFF()

            last_status = must_spin
            mqtt.publish_temp(temp)

        except KeyboardInterrupt:
            logutil.info("Keyboard Interrupt")
            Run = False
        except Exception as e:
            logutil.info(e)
            logutil.info("Error")
        finally:
            time.sleep(SLEEP_INTERVAL)
    logutil.info("Clean")
    manager.cleanup()
