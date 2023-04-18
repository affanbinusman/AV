import ev3_dc as ev3
with ev3.EV3(protocol=ev3.WIFI, host='00:16:53:42:2B:99') as my_robot:
    print(my_robot)