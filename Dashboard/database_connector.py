import mysql.connector
from mysql.connector import errorcode
from user import User
from shipper import Shipper
from current_jobs import Current_job
from bill_of_lading import BOL

class Database:

    config = {
        'user': 'pullinfreight',
        'password': 'Pull3778',
        'host': 'pullinfreightllc.cpunxilbhe7v.us-west-1.rds.amazonaws.com',
        'database': 'pullinFreight',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    def __init__(self):
        self.users_list = []
        self.shippers_list = []
        self.current_jobs_list = []

    def get_usernames(self):
        query = ("SELECT username FROM users ORDER BY username ASC")
        self.cursor.execute(query)

        username_list = []

        for username in self.cursor:
            username_list.append(str(username[0]))

        return username_list

    def get_users(self):
        query = ("SELECT * FROM users ORDER BY first_name ASC")
        self.cursor.execute(query)
        self.users_list = []

        for users in self.cursor:
            user = User(users[0], users[1], users[2], users[3], users[4], users[5], users[6], users[7], users[8])
            self.users_list.append(user)

        return self.users_list

    def update_user(self, user_id, first_name, last_name, phone_number, email, address):
        query = "UPDATE users SET first_name = %s, last_name = %s, phone_number = %s, email = %s, address = %s WHERE user_id = %s"
        val = (first_name, last_name, phone_number, email, address, user_id)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        val = (user_id, )
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def get_shippernames(self):
        query = ("SELECT name FROM shippers ORDER BY name ASC")
        self.cursor.execute(query)

        shippername_list = []

        for shipper_name in self.cursor:
            shippername_list.append(str(shipper_name[0]))

        return shippername_list

    def get_shippers(self):
        query = ("SELECT * FROM shippers ORDER BY name ASC")
        self.cursor.execute(query)
        self.shippers_list = []

        for shippers in self.cursor:
            shipper = Shipper(shippers[0], shippers[1], shippers[2], shippers[3], shippers[4], shippers[5], shippers[6])
            self.shippers_list.append(shipper)

        return self.shippers_list

    def update_shipper(self, shipper_id, name, broker_name, address, origin, destination, comments):
        query = "UPDATE shippers SET name= %s, broker_name= %s, address= %s, origin=%s, destination=%s, comments=%s WHERE shipper_id = %s"
        val = (name, broker_name, address, origin, destination, comments, shipper_id)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def get_shipper(self, shipper_id):
        query = "SELECT * FROM shippers WHERE shipper_id = %s"
        val = (shipper_id, )
        self.cursor.execute(query, val)
        for shippers in self.cursor:
            shipper = Shipper(shippers[0], shippers[1], shippers[2], shippers[3], shippers[4], shippers[5], shippers[6])
            self.shippers_list.append(shipper)
            return shipper

    def add_shipper(self, name, broker_name, address, origin, destination, comments):
        query = "INSERT INTO shippers (name, broker_name, address, origin, destination, comments) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, broker_name, address, origin, destination, comments)
        self.cursor.execute(query, val)
        self.cnx.commit()

    def delete_shipper(self, shipper_id):
        query = "DELETE FROM shippers WHERE shipper_id = %s"
        val = (shipper_id, )
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def get_current_jobs(self):
        query = ("SELECT * FROM current_jobs ORDER BY start_date DESC")
        self.cursor.execute(query)
        self.current_jobs_list.clear()
        self.current_jobs_list = []

        for jobs in self.cursor:
            job = Current_job(jobs[0], jobs[1], jobs[2], jobs[3], jobs[4], jobs[5], jobs[6], jobs[7], jobs[8], jobs[9])
            self.current_jobs_list.append(job)

        return self.current_jobs_list

    def get_current_job_by_id(self, job_id):
        query = "SELECT * FROM current_jobs WHERE job_id = %s"
        val = (job_id, )
        self.cursor.execute(query, val)

        for jobs in self.cursor:
            job = Current_job(jobs[0], jobs[1], jobs[2], jobs[3], jobs[4], jobs[5], jobs[6], jobs[7], jobs[8], jobs[9])

        return job

    def add_job(self, shipper_name, user_name, date, time, pay_type, rate, origin, destination, comments):
        query = "INSERT INTO current_jobs (`shipper_name`, `user_name`, `start_date`, `start_time`, `pay_type`, `rate`, `origin`, `destination`, `comments`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (shipper_name, user_name, date, time, pay_type, rate, origin, destination, comments)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def edit_job(self, shipper_name, user_name, date, time, pay_type, rate, origin, destination, comments, job_id):
        query = "UPDATE current_jobs SET `shipper_name`=%s, `user_name`=%s, `start_date`=%s, `start_time`=%s, `pay_type`=%s, `rate`=%s, `origin`=%s, `destination`=%s, `comments`=%s WHERE job_id =%s "
        val = (shipper_name, user_name, date, time, pay_type, rate, origin, destination, comments, job_id)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def delete_job(self, job_id):
        query = "DELETE FROM current_jobs WHERE job_id = %s"
        val = (job_id,)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def get_bols(self):
        query = "SELECT * FROM bill_of_ladings ORDER BY bill_id DESC"
        self.cursor.execute(query)
        bols = []

        for bill in self.cursor:
            bol = BOL(bill[0], bill[1], bill[2], bill[3], bill[4], bill[5], bill[6], bill[7], bill[8], bill[9], bill[10], bill[11], bill[12])
            bols.append(bol)

        return bols

    def edit_bol(self, bill_id, date, bill_number, shipper_name, user_name, rate, rate_type, origin, destination, loads, start_time, end_time, hours_worked):
        query = "UPDATE bill_of_ladings SET `date`=%s, `bill_number`=%s, `shipper_name`=%s, `user_name`=%s, `rate`=%s, `rate_type`=%s, `origin`=%s, `destination`=%s, `loads`=%s, `start_time`=%s, `end_time`=%s, `hours_worked`=%s WHERE bill_id =%s"
        val = (date, bill_number, shipper_name, user_name, rate, rate_type, origin, destination, loads, start_time, end_time, hours_worked, bill_id)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def add_bol(self, date, bill_number, shipper_name, user_name, rate, rate_type, origin, destination, loads, start_time, end_time, hours_worked):

        user_id = self.get_user_id(user_name)

        query = "INSERT INTO bill_of_ladings (`date`, `bill_number`, `shipper_name`, `user_name`, `rate`, `rate_type`, `origin`, `destination`, `loads`, `start_time`, `end_time`, `hours_worked`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (date, bill_number, shipper_name, user_name, rate, rate_type, origin, destination, loads, start_time, end_time, hours_worked)
        self.cursor.execute(query, val)
        self.cnx.commit()

        bill_id = self.get_last_bill_id()

        query = "INSERT INTO job_link (`user_id`, `bill_id`) VALUES (%s, %s)"
        val = (user_id, bill_id)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def get_last_bill_id(self):
        query = "SELECT MAX(bill_id) FROM bill_of_ladings"
        self.cursor.execute(query)

        for id in self.cursor:
            bill_id = id[0]
            return bill_id

    def get_user_id(self, username):
        query = "SELECT user_id FROM users WHERE username = %s"
        val = (username, )
        self.cursor.execute(query, val)

        for id in self.cursor:
            user_id = id[0]
            return user_id

    def delete_bol(self, bill_id):
        query = "DELETE FROM job_link WHERE bill_id = %s"
        val = (bill_id,)
        self.cursor.execute(query, val)
        self.cnx.commit()

        query = "DELETE FROM bill_of_ladings WHERE bill_id = %s"
        val = (bill_id,)
        self.cursor.execute(query, val)
        self.cnx.commit()
        return

    def get_bol_invoiced(self, shipper_name, from_date, to_date):
        query = "SELECT * FROM bill_of_ladings WHERE shipper_name = %s AND (date >= %s AND date <=%s) ORDER BY date ASC"
        val = (shipper_name, from_date, to_date)
        self.cursor.execute(query, val)
        bols = []

        for bill in self.cursor:
            bol = BOL(bill[0], bill[1], bill[2], bill[3], bill[4], bill[5], bill[6], bill[7], bill[8], bill[9],
                      bill[10], bill[11], bill[12])
            bols.append(bol)

        return bols

    def get_driver_logs(self, driver_username, from_date, to_date):
        query = "SELECT * FROM bill_of_ladings WHERE user_name = %s AND (date >= %s AND date <=%s) ORDER BY date ASC"
        val = (driver_username, from_date, to_date)
        self.cursor.execute(query, val)
        bols = []

        for bill in self.cursor:
            bol = BOL(bill[0], bill[1], bill[2], bill[3], bill[4], bill[5], bill[6], bill[7], bill[8], bill[9],
                      bill[10], bill[11], bill[12])
            bols.append(bol)

        return bols