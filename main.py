import configparser
import time
import sys

from gpio.gpio_manager import GPioManager
from gpio.gpio_manager_dummy import GPioManagerDummy
from mqtt.mqtt_manager import MqttManager

ON_THRESHOLD = 65  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 45  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 1  # (seconds) How often we check the core temperature.

if __name__ == '__main__':
    default_config = 'config.ini'
    if len(sys.argv) > 0:
        profile = sys.argv[1]
        if profile.startswith('--profile='):
            default_config = 'config_'+profile.split("=")[1]+'.ini'

    config = configparser.ConfigParser()
    config.read(default_config)
    if config['default']['TEST_MODE']:
        manager = GPioManagerDummy(config)
    else:
        manager = GPioManager(config)

    mqtt = MqttManager(config)

    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    last_status = False
    Run = True
    while Run:
        try:
            must_spin = last_status
            temp = manager.get_temp()

            if last_status:
                print("RUNNING...")

            if not last_status:
                print("OFF...")

            if temp >= ON_THRESHOLD:
               must_spin = True

            if temp <= OFF_THRESHOLD:
                must_spin = False

            if must_spin and must_spin != last_status:
                print("Ligando...")
                manager.turnOn()


            if not must_spin and must_spin != last_status:
                print("Desligando...")
                manager.turnOFF()

            last_status = must_spin
            mqtt.publish_temp(temp)

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            Run = False
        except Exception as e:
            print(e)
            print("Error")
        finally:
            time.sleep(SLEEP_INTERVAL)
    print("Clean")
    manager.cleanup()
