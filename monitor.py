'''
boto configuration in ~/.boto
Contains:
[Credentials]
aws_access_key_id = <key_id>
aws_secret_access_key = <secret_key>
'''

import boto3
from datetime import datetime
from datetime import timedelta
import sys

time_window = 60 #in minutes

end = datetime.utcnow()
start = end - timedelta(minutes=time_window)

client = boto3.client('cloudwatch', 'us-west-2')

dimensions = [{'Name': 'InstanceId', 'Value': 'i-f1177737'}]

class Stat(object):
    response = None
    def __init__(self, name, unit='Bytes'):
        self.name = name
        self.unit = unit
    def get_statistics(self):
        self.response = client.get_metric_statistics(Namespace='AWS/EC2',
                                                MetricName=self.name,
                                                StartTime=start,
                                                EndTime=end,
                                                Period=60*time_window,
                                                Unit=self.unit,
                                                Statistics=['Average', 'Maximum'],
                                                Dimensions=dimensions)
    def __str__(self):
        if not self.response:
            get_statistics()
        if not self.response['Datapoints']:
            return self.name + ": " + "No data"
        return '%-20s%-20s%-20s' % (self.name + ": ",
                                    str(self.response['Datapoints'][0]['Average']),
                                    str(self.response['Datapoints'][0]['Maximum'])
                                   )

stats = [Stat('CPUUtilization', 'Percent'),
         Stat('DiskReadBytes'), 
         Stat('DiskWriteBytes'),
         Stat('NetworkIn'),
         Stat('NetworkOut')]

print '%-20s%-20s%-20s' % ('Statistic', 'Average', 'Maximum')
for s in stats:
    s.get_statistics()
    print s


