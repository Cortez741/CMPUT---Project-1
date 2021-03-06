#---New Vehicle Registration-------------------------------------------------------------------------------------------#
# Authors: Victor Frunza & Ian Oltuszyk
# Instructor: Li-Yan Yuan
# TA: Kriti Khare
# Filename: NVR.py

#---Description--------------------------------------------------------------------------------------------------------#
# Description: This component is used to register a new vehicle by an auto registration officer. By a new vehicle, we
# mean a vehicle that has not been registered in the database. The component shall allow an officer to enter the
# detailed information about the vehicle and personal information about its new owners, if it is not in the database.
# You may assume that all the information about vehicle types has been loaded in the initial database.

#---Interface----------------------------------------------------------------------------------------------------------#
# Input: serial_no, maker, model, year, color, type_id, owner_id, is_primary_owner
# Ouput: RESULT CODE

#---Function Start-----------------------------------------------------------------------------------------------------#
def NVR(serial_no, maker, model, year, color, type_id, owner_id, is_primary_owner):

    vehicle_SQL = 'INSERT INTO vehicle VALUES ('+serial_no+', '+maker+', '+model+', '+year+', '+color+', '+type_id+');'
