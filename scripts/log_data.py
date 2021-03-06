#!/usr/bin/env python

import rospy
import yaml, json
import csv
import time
import datetime
import os

import message_filters

from crazyflie_driver.msg import GenericLogData
# header:
#   seq: 75
#   stamp:
#     secs: 3
#     nsecs: 546000000
#   frame_id: ''
# values: [0.0, 0.0, 0.0, 0.0]

CrazyswarmDir = os.path.dirname(os.path.realpath(__file__)) + "/../../crazyswarm"
LogDir = os.path.dirname(os.path.realpath(__file__)) + "/../data"
LogFiles = []
now = datetime.datetime.now()

def mf_callbacks(*collection):
	k = 0
	for data in collection:
		# rospy.loginfo(rospy.get_caller_id() + ": I got %s", data)
		# rospy.loginfo(LogFiles[k])
		# rospy.loginfo(str(rospy.get_param('/crazyswarm_server/genericLogTopic_log1_Variables')))

		# write values in csv
		with open(LogFiles[k], 'aw') as csvFile:
			writer = csv.writer(csvFile)
			row = [data.header.stamp.secs + data.header.stamp.nsecs/1e9]
			row.extend(data.values)
			writer.writerow(row)
		k = k + 1

if __name__ == '__main__':

	# read crazyflies.yaml to get IDs and create csv files
	ids = []
	subscriber = []
	with open(CrazyswarmDir+"/launch/crazyflies.yaml") as stream:
		allCFs = yaml.load(stream, yaml.FullLoader)
		for cf in allCFs['crazyflies']:
			id = cf['id']
			file = LogDir+"/log_"+now.strftime("%Y_%m_%d_%H_%M")+"/CF"+str(cf['id'])+'.csv'
			ids.append(id)
			LogFiles.append(file)
			subscriber.append(message_filters.Subscriber('/cf'+str(id)+'/log1', GenericLogData))
			# Check if dir exists and create CSV file with header:
			if not os.path.exists(os.path.dirname(file)):
			    try:
			        os.makedirs(os.path.dirname(file))
			    except OSError as exc: # Guard against race condition
			        if exc.errno != errno.EEXIST:
			            raise
			with open(file, 'w+') as csvFile:
				writer = csv.writer(csvFile)
				row = ["Time [s]"]
				row.extend(rospy.get_param('/crazyswarm_server/genericLogTopic_log1_Variables'))
				writer.writerow(row)

	rospy.init_node('log_data', anonymous=False)
	# rospy.Subscriber(ROS_TOPIC, GenericLogData, ros_callback)
	ts = message_filters.ApproximateTimeSynchronizer(subscriber, 10, 0.01, allow_headerless=False)
	# ts = message_filters.TimeSynchronizer([cf30, cf31], 15)
	ts.registerCallback(mf_callbacks)
	rospy.spin()
