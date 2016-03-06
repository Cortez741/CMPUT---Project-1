#---Auto Transaction---------------------------------------------------------------------------------------------------#
# Authors: Victor Frunza & Ian Oltuszyk
# Instructor: Li-Yan Yuan
# TA: Kriti Khare
# Filename: AT.py
#---Description--------------------------------------------------------------------------------------------------------#
# This component is used to complete an auto transaction. Your program shall allow the officer to enter all
# necessary information to complete this task, including, but not limiting to, the details about the seller, the buyer,
# the date, and the price. The component shall also remove the relevant information of the previous ownership.

#---Interface----------------------------------------------------------------------------------------------------------#
# Input: transaction_id, seller_id, buyer_id, vehicle_id, s_date, price
# Ouput: RESULT CODE

#---Function Start-----------------------------------------------------------------------------------------------------#
def AT(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price):

    sale_SQL = 'INSERT INTO vehicle VALUES ('+transaction_id+', '+seller_id+', '+buyer_id+', '+vehicle_id+', '+s_date+', '+price+');'
