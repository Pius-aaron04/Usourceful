# Data Endpoints
This dir contains endpoints definitions for Related data. Below is
the list of endpoints and their methods and purposes

## User
GET 		/api/v1/users					fetches all users
POST		/api/vi/users					creates a user with json data
GET 		/api/v1/users/<user_id>				fetches a user with id specified
DELETE		/api/v1/users/<user_id>				deletes a user
GET 		/api/v1/users/<user_id>/library			fetches a user's library data
GET 		/api/v1/users/<user_id>/library/racks		fetches data of the racks in a user library
POST		/api/v1/users/<user_id>/library/racks		creates a new rack in the user library
GET 		/api/v1/users/recommendations			fetches the recommendations available to user

## Racks

GET 		/api/v1/racks					fetches racks data
GET 		/api/v1/racks/<rack_id>				fetches a rack
GET 		/api/v1/rack/<rack_id>/resources		fetches the resources in a rack
GET 		/api/v1/rack/<rack_id>/subracks			fetches all subracks in a rack
POST		/api/v1/racks					creates a new rack
UPDATE		/api/v1/racks/<rack_id>				updates an existing rack
DELETE		/api/v1/racks/<rack_id>				deletes a rack

## Resource 

GET 		/api/v1/resources/<resource_id>			fetches a resource (added)
POST 		/api/v1/resources/				creates a new resource (added)
UPDATE 		/api/v1/resources/<resource_id>			updates an existing resource (added)
DELETE 		/api/v1/resources/<resource_id> 		deletes a resource
