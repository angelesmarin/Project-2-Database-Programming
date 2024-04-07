import mysql.connector
from mysql.connector import Error

#function a:
def create_connection ():
    try:
        connection= mysql.connector.connect(
            user= 'studentdba',
            password= 'L;n9u(fV',
            host= 'csci-cs418-09.dhcp.bsu.edu',
            database= 'falcone_airlines_database'
        )
        print("Connection established")
        return connection 
    except mysql.connector.Error as error:
        print('Connection failed:', error)
        return None
   
   #function b: 
def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            Create table if not exists User (
                User_id int auto_increment not null primary key,
                Fname varchar(150) not null, 
                Lname varchar(150) not null, 
                Email varchar(200) not null 
            )
            """)
        cursor.execute("""
            Create table if not exists Booking (
                Booking_id int auto_increment not null primary key,
                User_id int,
                Foreign key(User_id) references User(User_id) on delete cascade on update cascade
            )
            """)
        
        connection.commit()
        print("Tables created")
    except mysql.connector.Error as error:
        print('Table creation failed:', error)

#function c:
def insert_booking(connection, user_info):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            Insert into User (Fname, Lname, Email) values (%s, %s, %s) 
            """, (user_info['fname'], user_info['lname'], user_info['email']))
        user_id = cursor.lastrowid
        
        cursor.execute("""
            Insert into Booking (User_id) values (%s) 
            """, (user_id,))
        connection.commit()
        
        cursor.execute("""
            Select Booking_id from Booking where User_id = %s 
        """, (user_id,))
        booking_id = cursor.fetchone()[0]
        print("Booking successful")
        
        return user_info, booking_id
    except mysql.connector.Error as error:
        print('Booking failed: ', error)
        return None
#function d:
def view_booking(connection, user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            Select Booking_id from Booking where User_id = %s
        """, (user_id,))
        bookings = cursor.fetchall()
        for i in bookings:
            print(i[0])
    except mysql.connector.Error as error:
        print('View booking failed: ', error)

##function e:
def delete_booking(connection, booking_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            delete from Booking where Booking_id = %s
        """, (booking_id,))
        connection.commit()
        print("\nBooking deleted")
    except mysql.connector.Error as error:
        print('\nBooking deletion failed: ', error)

def main():
    connection = create_connection()
    if connection:
        create_table(connection)
        while True:
            print("\nWelcome to Falcone Airlines\n" +
                  "Press 1 to Book\n" +
                   "Press 2 to View Reservation\n" +
                    "Press 3 to Cancel Reservation\n" +
                    "Press 4 to Exit\n")
            choice = input("Select an option: ")
            if choice == '1':
                print("To book we'll need your info: \n")
                fname = input("Enter your first name: ")
                lname = input("Enter your last name: ")
                email = input("Enter your email: ")
                user_info = {'fname': fname, 'lname': lname, 'email': email}
                user_info, booking_id = insert_booking(connection, user_info)
                if booking_id:
                    print("\nBooking Made, here are your details: \n *remember Booking Id number*")
                    print("First Name:", fname)
                    print("Last Name:", lname)
                    print("Email:", email)
                    print("Booking ID number: ", booking_id)
                else:
                    print("Booking Failed")
            elif choice == '2':
                booking_id = int(input("Enter Booking id number to view bookings: "))
                view_booking(connection, booking_id)
            elif choice == '3':
                booking_id = int(input("Enter Booking id number to cancel booking: "))
                delete_booking(connection, booking_id)
            elif choice == '4':
                break
            else:
                print("invalid, select 1-4")
                  
if __name__ == "__main__":
    main()