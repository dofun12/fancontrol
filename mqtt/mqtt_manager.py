import paho.mqtt.client as mqtt
from datetime import datetime


class MqttManager:
    config = None
    interval = 0
    last_time = 0.0
    last_period_sum = 0.0
    last_period_times = 0

    def is_ready(self):
        now = datetime.now().microsecond
        if now - self.last_time >= (self.interval*1000):
            self.last_time = now
            return True
        return False

    def __init__(self, config):
        self.config = config
        self.interval = int(self.config['mqtt']['INTERVAL'])

    def publish_temp(self, temp):
        if 'true' != self.config['mqtt']['ENABLED']:
            return
        if not self.is_ready():
            self.last_period_times = self.last_period_times+1
            self.last_period_sum = self.last_period_sum+temp
            return
        if self.last_period_sum + self.last_period_times > 0:
            temp = (self.last_period_sum / self.last_period_times)
        self.last_period_sum = 0
        self.last_period_times = 0

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

        print("Published.... " + topic + " with " + str(temp))

    def on_publish(self, client, userdata, mid):
        print("Published.... ")
