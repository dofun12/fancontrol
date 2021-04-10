import paho.mqtt.client as mqtt
import time
import logutil


class MqttManager:
    config = None
    interval = 0
    last_time = 0.0
    last_period_sum = 0.0
    last_period_times = 0
    last_period_max = 0
    last_period_min = 0

    def reset(self):
        self.last_period_sum = 0
        self.last_period_times = 0
        self.last_period_min = 0
        self.last_period_max = 0

    def get_now(self):
        return time.perf_counter()

    def is_ready(self):
        now = self.get_now()
        if (now - self.last_time) >= (self.interval):
            self.last_time = self.get_now()
            return True
        return False

    def calculate(self,temp):
        self.last_period_times = self.last_period_times + 1
        self.last_period_sum = self.last_period_sum + temp
        if temp > self.last_period_max:
            self.last_period_max = temp
        if self.last_period_min == 0 or temp < self.last_period_min:
            self.last_period_min = temp

    def __init__(self, config):
        self.config = config
        self.interval = int(self.config['mqtt']['INTERVAL'])

    def publish_temp(self, temp):
        if 'true' != self.config['mqtt']['ENABLED']:
            return
        if not self.is_ready():
            self.calculate(temp)
            return
        if self.last_period_sum + self.last_period_times > 0:
            avg_temp = round(self.last_period_sum / self.last_period_times,2)
        else:
            avg_temp = temp
        min_temp = self.last_period_min
        max_temp = self.last_period_max

        self.reset()

        client = mqtt.Client()
        topic = self.config['mqtt']['TOPIC']
        user = self.config['mqtt']['USER']
        passwd = self.config['mqtt']['PASSWD']
        host = self.config['mqtt']['HOST']
        port = int(self.config['mqtt']['PORT'])

        client.username_pw_set(
            user,
            passwd
        )
        client.connect(host, port, 60)
        client.on_publish = self.on_publish
        client.publish(topic, temp)  # publish
        client.publish(topic+"/avg", avg_temp)  # publish
        client.publish(topic+"/min", min_temp)  # publish
        client.publish(topic+"/max", max_temp)  # publish

        logutil.info("Published Last.... " + topic + " with " + str(temp))
        logutil.info("Published AVG.... " + topic + " with " + str(avg_temp))
        logutil.info("Published MIN.... " + topic + " with " + str(min_temp))
        logutil.info("Published MAX.... " + topic + " with " + str(max_temp))

    def on_publish(self, client, userdata, mid):
        logutil.info("Published.... ")
