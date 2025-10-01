import connector
import time

class TReaderAgent:
    def __init__(self):
        self.connector = connector.Connector('ipc', 'temperature', None, connector.ConnectionMode.subscriber)
        self.work = False

    def read_temperature(self):
        if self.connector.connected:
            try:
                message = self.connector.block_read_message()
                print(f'read temperature {message}')
            except Exception as e:
                print(f'no temperature sent - timeout happens {e}')
        else:
            self.connector.connect()

    def run(self):
        self.work = True
        while self.work:
            self.read_temperature()
            time.sleep(0.5)

class ManagerAgent:
    def __init__(self):
        self.connector = connector.Connector('ipc', 'mng', None, connector.ConnectionMode.request)

    def send_cmd(self, cmd: str):
        if self.connector.connected:
            try:
                self.connector.block_send_message(cmd)
            except Exception as e:
                print(f'filed send cmd {e}')

            try:
                answer = self.connector.block_read_message()
            except Exception as e:
                answer ='error'
                print(f'filed read answer {e}')

            return answer
        else:
            return 'error'