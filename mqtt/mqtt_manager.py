import paho.mqtt.client as mqtt


class MqttManager:
    config = None

    def __init__(self, config):
        self.config = config

    def publish_temp(self, temp):
        if self.config['mqtt']['ENABLED'] != 'true':
            return
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
        client.connect(host,port,60)
        client.on_publish = self.on_publish
        client.publish(topic, temp)  # publish

        print("Published.... "+topic+" with "+str(temp))

    def on_publish(self, client, userdata, mid):
        print("Published.... ")
