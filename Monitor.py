'''
This is the main monitor
'''

class Monitor(object):
    '''Main class for all monitoring'''

    def __init__(self):
        print "Initialized Monitor"

    def __str__(self):
        return "I'm a monitor"

if __name__ == "__main__":
    monitor = Monitor()

    print monitor
