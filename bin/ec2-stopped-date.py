import boto.ec2    

class i_color:
  red   = '\033[31m'
  reset = '\033[0m'

def name(i):
  if 'Name' in i.tags:
    n = i.tags['Name']
    n = i_color.red + n + i_color.reset
  return n

#conn = boto.ec2.connect_to_region("us-east-1")
conn = boto.ec2.connect_to_region("us-west-2")
reservations = conn.get_all_instances()
for r in reservations:
    for i in r.instances:
        if i.state == 'stopped':
           print("%s [%s] %s" % (name(i),i.state,i.reason))


'''
import boto.ec2
conn = boto.ec2.connect_to_region("eu-west-1")
reservations = conn.get_all_instances()
for r in reservations:
    for i in r.instances:
        if i.state == 'stopped':
            print "%s [%s] %s" % (i.id, i.state, i.reason)
'''
