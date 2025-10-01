#!/usr/bin/env python3

import agents
import threading


def main():
    t_reader = agents.TReaderAgent()
    t_reader.connector.connect()
    thread = threading.Thread(target=t_reader.run)
    thread.start()
    thread.join(5)

if __name__ == "__main__":
    main()