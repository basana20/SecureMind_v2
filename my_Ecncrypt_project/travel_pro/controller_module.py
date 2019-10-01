#Author: Kranthi Kumar K
#Date: 30/09/2019

import time, threading
import database_module as db
lock = threading.Lock()


class controller_mod(object):
    def __init__(self):
        self.db_obj = db.DB_module()

    def moniter(self, customer_id, customer_name, pickup_point, drop_point):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.pickup_point = pickup_point
        self.drop_point = drop_point
        self.cab_num = self.check_cab_avaliability()
        if self.cab_num == None:
            print "NO cabs are avalible in your location...!"
            exit()
        else:
            self.distance = self.get_distance(self.pickup_point, self.drop_point)
            self.total_fair = self.get_fair(self.distance)
            self.suspen()
    def get_suspend_time(self, distance):
        speed = 80.00 / 3.6
        distance = distance * 1000
        sus_time = (distance / speed) / 100
        return sus_time
    def suspen(self):
        # lock.acquire()
        sus_time = self.get_suspend_time(self.distance)
        self.update_cab_status(cab_num=self.cab_num, status="R", loc=self.pickup_point, book_status='BLOCK')
        print str(self.customer_name) + " your cab is Booked,"+" cab number = "+str(self.cab_num)+" it takes " + str(sus_time)+ " sec. to reach the destination"
        time.sleep(int(sus_time))
        self.update_fair_details()
        self.update_cab_status(cab_num=self.cab_num, status="F", loc=self.drop_point, book_status='FREE')
        # lock.release()

    def get_distance(self, start_point, end_point):
        distance = 15
        a, b, c = 0, 0, 0
        locations = self.get_locations()
        for x in range(len(locations)):
            if start_point.upper() == locations[x]:
                a = x
            elif end_point.upper() == locations[x]:
                b = x
            else:
                pass
        if a < b:
            c = b - a
        elif b < a:
            c = a - b
        else:
            pass
        dis = c * distance
        return dis

    def get_fair(self, total_distance_traveled):
        base_fair_per_5km = 100.00
        min_distance = 5
        base_fair = 10.00
        total_fair = 0.00
        if total_distance_traveled > min_distance:
            total_fair = base_fair_per_5km
            extra_distance = total_distance_traveled - min_distance
            extra_distance = extra_distance / 2
            total_fair = total_fair + extra_distance * base_fair
        return total_fair

    def get_total_bill(self, cab= ""):
        bill = self.db_obj.get_price_from_db(cab_id=cab)
        return bill

    def check_cab_avaliability(self):
        cabs = self.db_obj.check_avalible_free_cabs()
        print cabs
        if len(cabs) != 0:
            for key, value in cabs.items():
                if value == self.pickup_point:
                    cab_num = str(key)
                    return cab_num
            cabs_distance = {}
            for key, value in cabs.items():
                dis = self.get_distance(self.pickup_point, value)
                cabs_distance[key] = dis
            li = []
            print cabs_distance
            for value in cabs_distance.values():
                li.append(value)
            print li
            li = sorted(li)
            dict_min = {}
            for key, value in cabs_distance.items():
                if li[0] == value:
                    dict_min[key] = value
            cab_num = ""
            print dict_min
            distance = 0
            for x, y in dict_min.items():
                cab_num = str(x)
                distance = int(y)
            print "cab_num "+str(cab_num)
            print "distance "+str(distance)

            wait_time = self.get_suspend_time(distance)
            print "waiting time "+str(wait_time)
            self.update_cab_status(cab_num=str(cab_num), status='F', loc=self.pickup_point, book_status='BLOCK')
            print self.customer_name + " your cab will be arriving soon in " + str(wait_time) + " Sec.., Your Cab Number is "+ str(cab_num)
            time.sleep(float(wait_time+2))
            return cab_num
        else:
            return None
    def update_cab_status(self, cab_num, status, loc, book_status):
        res = self.db_obj.update_cab_curr_status(cab_num, status, loc, book_status)
        return res

    def update_fair_details(self):
        res = self.db_obj.update_fair_details(self.cab_num,self.customer_id,self.pickup_point,self.drop_point,self.distance,self.total_fair)
        return res

    def close_control_module(self):
        return self.db_obj.close_db_module()

    def check_user_name(self, customer_id):
        result = self.db_obj.get_user_name(customer_id)
        if result.empty:
            return "NO"
        else:
            return str(result["customer_name"][0])
    def get_locations(self):
        locations = self.db_obj.get_locations()
        locations_list = []
        for x in range(locations.size):
            locations_list.append(str(locations["location_code"][x]))
        return locations_list

# obj = controller_mod()
# print obj.check_cab_avaliability()