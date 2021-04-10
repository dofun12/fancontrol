import subprocess
import logutil

try:
    logutil.info('Starting Real MODE')
    from RPi.GPIO import GPIO
except ImportError:
    logutil.info('Starting Simulator MODE')
    import simulator.gpio as GPIO

class GPioManager:


    # from EmulatorGUI import GPIO
    # from gpiozero import OutputDevice
    ON_THRESHOLD = 65  # (degrees Celsius) Fan kicks on at this temperature.
    OFF_THRESHOLD = 45  # (degress Celsius) Fan shuts off at this temperature.
    SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
    GPIO_PIN = 18  # Which GPIO pin you're using to control the fan.

    config = None

    def __init__(self,config):

        self.config = config
        self.GPIO_PIN = int(config['gpio']['GPIO_PIN'])  # Which GPIO pin you're using to control the fan.
        self.ON_THRESHOLD = int(config['gpio']['ON_THRESHOLD'])  # (degrees Celsius) Fan kicks on at this temperature.
        self.OFF_THRESHOLD = int(config['gpio']['OFF_THRESHOLD'])  # (degress Celsius) Fan shuts off at this temperature.
        self.SLEEP_INTERVAL = int(config['gpio']['SLEEP_INTERVAL'])  # (seconds) How often we check the core temperature.

        try:
            logutil.info('Setuping and BCM....')
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.GPIO_PIN, GPIO.OUT)
        except AttributeError:
            logutil.info('Skipping BCM and Setup')

        GPIO.output(self.GPIO_PIN, False)


    def turnOn(self):
        GPIO.output(self.GPIO_PIN, True)


    def turnOFF(self):
        GPIO.output(self.GPIO_PIN, False)



    def get_temp(self):
        """Get the core temperature.
        Run a shell script to get the core temp and parse the output.
        Raises:
            RuntimeError: if response cannot be parsed.
        Returns:
            float: The core temperature in degrees Celsius.
        """
        output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
        temp_str = output.stdout.decode()
        try:
            value = float(temp_str.split('=')[1].split('\'')[0])
            logutil.info(value)
            return value
        except (IndexError, ValueError):
            raise RuntimeError('Could not parse temperature output.')

    def cleanup(self):
        GPIO.cleanup()
