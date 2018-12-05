import pymysql
import NumberGenerator_V0 as csprng

GENERATOR = 2

username = input("Username: ")
password = input("Password: ")
user_number = csprng.username_processor(username)
print(user_number)
user_number_factors = csprng.factorizer(user_number,1)
print(user_number_factors)
user_number_factors_one, user_number_factors_two = user_number_factors[0: user_number_factors.find(',')], user_number_factors[user_number_factors.find(',')+1:len(user_number_factors)]
x, y = str(pow(GENERATOR, int(user_number_factors_one))), str(pow(GENERATOR, int(user_number_factors_two)))
pass_number = csprng.password_to_number(password)
public_key = str(pow(GENERATOR, pass_number))
print(pass_number, public_key)

connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="Akhilesh@1997", db="user_information")
cursor = connection.cursor()
print(connection.db.__getitem__)
insert_query = "insert into credentials values('"+x+"', '"+y+"', '"+public_key+"')"
select_query =  "select * from credentials"
cursor.execute(insert_query)
connection.commit()

# cursor.execute(select_query)
# print(cursor.fetchall()[0])
connection.close()
# client = MongoClient("mongodb://Akhilesh:<PASSWORD>@cluster0-shard-00-00-3kkvn.gcp.mongodb.net:27017,"
#                          "cluster0-shard-00-01-3kkvn.gcp.mongodb.net:27017,cluster0-shard-00-02-3kkvn.gcp."
#                          "mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
