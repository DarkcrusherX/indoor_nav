
import sys
import copy
import rospy
import actionlib
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from armf import armtakeoff
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

msg = Path()
current_position= PoseStamped()

rospy.init_node('points',anonymous=True)

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    print("Enter coordinates x and y :")
    x = input()
    y = input()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = float(x)
    goal.target_pose.pose.position.y = float(y)
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    # wait = client.wait_for_result()
    # if not wait:
    #     rospy.logerr("Action server not available!")
    #     rospy.signal_shutdown("Action server not available!")
    # else:
    return client.get_result()

def callback(data):

    global msg

    msg = data


def callback_pos(pos):

    global current_position
    current_position = pos

def calc_dist(trajectory,current_position):
    x1= trajectory.pose.position.x
    y1 = trajectory.pose.position.y
    x2= current_position.pose.position.x
    y2= current_position.pose.position.y


    dist = (x1-x2)**2 + (y1-y2)**2 
    return dist


def main(i):

    publish = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped,queue_size=20)

    trajectory = PoseStamped()

    trajectory = msg.poses[i]

    rospy.Subscriber('/mavros/local_position/pose',PoseStamped,callback_pos)

    dist =  calc_dist(trajectory,current_position)
    print(i)
    print(msg.poses[i])
    #print(dist)
    rate = rospy.Rate(10)
    while dist > 0.1:

        rate.sleep()
        rospy.Subscriber('/mavros/local_position/pose',PoseStamped,callback_pos)
        rospy.Subscriber('/move_base/NavfnROS/plan',Path,callback)

        dist =  calc_dist(trajectory,current_position)
        trajectory = msg.poses[i]    
        trajectory.pose.position.z = current_position.pose.position.z

        print(" Dist new : {}".format(dist))
        publish.publish(trajectory)



    if dist <0.1 :
        i = i+1
        main(i)

if __name__ == '__main__':
     try:
            armclass = armtakeoff()
            result = movebase_client()
            if result:
                rospy.loginfo("Goal execution done!")

            for i in range(1000):
                #setpoint.publish(goal)

                rospy.Subscriber('/move_base/NavfnROS/plan',Path,callback)

            armclass.arm()
            armclass.takeoff()

            main(0)

     except rospy.ROSInterruptException:
            pass




