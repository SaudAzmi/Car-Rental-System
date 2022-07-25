# Databricks notebook source
df= spark.read.csv("/FileStore/tables/CarRentalData_1-1.csv", header=True, inferSchema=True)

# COMMAND ----------

display(df)

# COMMAND ----------

df.createOrReplaceTempView("Car_Rental")

# COMMAND ----------

spark.sql("SELECT * FROM Car_Rental")

# COMMAND ----------

# MAGIC %sql
# MAGIC select* from`Car_Rental`

# COMMAND ----------

# MAGIC %sql
# MAGIC /* Top 3  states that uses the most cars :*/
# MAGIC select state,count(state) as Count from `Car_Rental` group by 1 order by Count desc
# MAGIC limit 3

# COMMAND ----------

# MAGIC %sql
# MAGIC /* Top 3 cities that uses the most cars :*/
# MAGIC select city,count(city) as Count from `Car_Rental` group by 1 order by Count desc
# MAGIC limit 3

# COMMAND ----------

# MAGIC 
# MAGIC %sql
# MAGIC /*Top states with max owners*/
# MAGIC select state,id,count(state) as Count from `Car_Rental` group by state,id   order by Count desc

# COMMAND ----------

# MAGIC %sql
# MAGIC /*different vehicle:*/
# MAGIC select vehicletype,count(vehicletype) as Count from `Car_Rental` group by vehicletype   order by Count desc

# COMMAND ----------

# MAGIC %sql
# MAGIC /* Top 5 vehicle makers who helped making most avg. daily rate*/
# MAGIC select vehiclemake ,avg(ratedaily) as avgrate from `Car_Rental` group by vehiclemake   order by avgrate desc
# MAGIC limit 5

# COMMAND ----------

# MAGIC %sql
# MAGIC /*different vehicle:*/
# MAGIC select fuelType,count(vehicletype) as Count from `Car_Rental` group by fuelType   order by Count desc

# COMMAND ----------

# MAGIC %sql
# MAGIC /* Top 5 vehicle makers who helped making most avg. daily rate*/
# MAGIC select fuelType,avg(renterTripsTaken) as avgtrip from `Car_Rental` group by fuelType   order by avgtrip desc
# MAGIC limit 5

# COMMAND ----------

# MAGIC %pip install matplotlib

# COMMAND ----------

#############Does renter trips affect review counts?############

df = sqlContext.sql("Select * from `Car_Rental`")
df = df.toPandas()
# df.set_index('rating').plot()
df.plot.scatter(x='renterTripsTaken',y='reviewCount')


# COMMAND ----------

############### car rating ################
df = sqlContext.sql("Select * from `Car_Rental`")
df = df.toPandas()
df.hist(column='rating',bins=15,grid=False, figsize=(12,8))

