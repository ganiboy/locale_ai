**Backend-end Task:**

XRides, delivers about a 200 rides per minute or 288,000 rides per day. Now, they want to send
this data to your system via an API. Your task is to create this API and save the data into
PostgreSQL.

The API should be designed, keeping in mind the real-time streaming nature of data and the
burst of requests at peak times of the day. The user of this API expects an acknowledgment that
the data is accepted and a way to track if the request fails.

**Brownie Points:**
1. Write a query DSL of how you would want this data to be queried and how someone
would be able to run analytics operations on top of it.
2. Write up on the ideal system architecture and the design of API given enough time and
resources.

**Technologies:**

Our ideal stack is Python/Go. But feel free to use the language of your choice.

**Solution:**

As I go through the task, this is the one of the problem statement and there are much more
about to come so I came up with micro-service architecture. Because micro-services are easy to maintain,
light weight as well as independently deployable.  

Tech stack: Python

Web Framework: Flask

When it comes to deploying flask application I would say we can deploy in AWS Lamda which is serverless 
or else we could deploy in EC2 instance. I would prefer deploying in EC2 instances along with load balancer 
because if I create lambda functions then migrating our applications from AWS services to any other 
cloud service would take bit large time. 

Deployment: EC2 instance (along with load-balancer), AWS - RDS for PosgreSQL 

Postgresql Tables: 

cab_drivers: 

This schema contains driver information such as driver_id, vehicle_model_id etc (We can have much 
more details related to driver such as "active")

customers:

This schema contains customers information such as user_id (We can have other information 
such as Phone, Address, Pincode, etc)

cab_rides:

This schema contains all other booking details.

**Code Walk-Through:**

1. **confg.ini**: All of the posgresql configuration are mentioned here.

2. **connections.py**: Returns PosgreSQL connection object.

3. **global_exception_handler.py**: Defined my custom exception (ValidationError, FunctionalError)

4. **validate_request_body.py**: Responsible for validating all the request parameters keys as well as their 
expected datatype and datetime format. If there is any mismatch it would throw  ValidationError with detailed error 
message for that particular parameter.

5. **app.py**: This contains the view function which is responsible for sending a resposne.

Few Unit Test Results:

End Point: /xride_data

Header: {"Content-Type": "application/json"}

Positive Test Case:

body: {"booking_id": 132512,"user_id": 22177,"vehicle_model_id": 28,"package_id": null,"travel_type_id": 2,
"from_area_id": 83,"to_area_id": 448,"from_city_id": null,"to_city_id": null,"from_date": "1/1/2013 2:00:00",
"to_date": null,"online_booking": 0,"mobile_site_booking": 0,"booking_created": "1/1/2013 1:39:00",
"from_lat": 12.92415,"from_long": 77.67229,"to_lat": 12.92732,"to_long":77.63575,"driver_id":0}

Response: {"booking_id": 132512, "status": "Success"}

Negative Test Case:

Test Case 1:

body: {"booking_id": 132512,"user_id": 22177,**"vehicle_model_id": "28"**,"package_id": null,"travel_type_id": 2,
"from_area_id": 83,"to_area_id": 448,"from_city_id": null,"to_city_id": null,"from_date": "1/1/2013 2:00:00",
"to_date": null,"online_booking": 0,"mobile_site_booking": 0,"booking_created": "1/1/2013 1:39:00","from_lat": 12.92415,
"from_long": 77.67229,"to_lat": 12.92732,"to_long":77.63575,"driver_id":0}

Response: {"error_message": "**vehicle_model_id data type mismatch, vehicle_model_id expected to be <class 'int'>**", 
"status": "Failed"}

Test Case 2:
body: {"booking_id": 132512,"user_id": 22177,"vehicle_model_id": "28","package_id": null,"travel_type_id": 2,
"from_area_id": 83,"to_area_id": 448,"from_city_id": null,"to_city_id": null,"from_date": "1/1/2013 2:00:00",
"to_date": null,"online_booking": 0,"mobile_site_booking": 0,**"booking_created": "1/1-2013 1:39:00"**,"from_lat": 12.92415,
"from_long": 77.67229,"to_lat": 12.92732,"to_long":77.63575,"driver_id":0}

Response: {"error_message": "booking_created format mismatch, please send month/date/year hour:minute:seconds ", 
"status": "Failed"}

Design if enough source and time were given:

1. Would have created swagger document.
2. Added efficient logs and would have created a real time data ingestion to Elasticsearch.
3. Slice and dice with the data present in elasticsearch using Kibana dashboards.

Design of Real time data ingestion:

1. I have created a pip package called **clod-kafka-handler** https://pypi.org/project/Cloud-Kafka-Logger/ which will 
push all the log data to specific Kafka topic.

2. I would write a flink job which will subscribe to a topic and consumes all the data and perform some tranformation 
if required as well as push the data to Elasticsearch.

3. I would store last 60 days of data in Elasticsearch and archive the other data and store it in S3 bucket.

![Design](/design.png) 
 

# locale_ai
