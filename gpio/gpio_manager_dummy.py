import random
import logutil

class GPioManagerDummy:
    last_generated_temp = 40
    threshold_max = 80
    threshold_min = 20
    increment = 1

    config = None

    def __init__(self, config):
        self.config = config

    def turnOn(self):
        logutil.info('Turning on')


    def turnOFF(self):
        logutil.info('Turning off')


    def get_temp_test(self):
        increment_range = (random.randrange(1, 5, 1) * self.increment)
        temp = self.last_generated_temp + increment_range
        self.last_generated_temp = temp
        if temp >= self.threshold_max or temp <= self.threshold_min:
            self.increment = (self.increment * -1)

        logutil.info('Test temp '+str(temp))
        return temp

    def get_temp(self):
        return self.get_temp_test()


    def cleanup(self):
        logutil.info('Cleanup')
