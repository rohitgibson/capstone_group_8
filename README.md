# AVS User Manual - Group 8

Capstone Group 8 (on GitHub): [https://github.com/rohitgibson/capstone_group_8](https://github.com/rohitgibson/capstone_group_8) 
Documentation: https://kennesawedu.sharepoint.com/:w:/s/Team-ISCapstone981/ESzbJcj0zDlPneQuHJ0YPIoBWcDXlSvJuSVgsMp-X7abzA?email=rgibso50%40students.kennesaw.edu&e=sP1Bkd

## Table of Contents

[Installation](#installation)

- [With Docker Compose](#with-docker-compose)

    - [Install Docker and Docker Compose](#install-docker-and-docker-compose)
    - [Download the Docker Compose File](#download-the-docker-compose-file)
    - [Install and Run API and Dependencies](#install-and-run-api-and-dependencies)

[Usage](#usage)

- [Authentication](#authentication)

    - [Basic User](#basic-user)
    - [Admin User](#admin-user)
    - [Root User](#root-user)

- [Endpoints](#endpoints)

    - [Address Endpoints](#address-endpoints)
    
        - [Add Address](#add-address)
        - [Verify Address](#verify-address)
        - [Update Address](#update-address)
        - [Delete Address](#delete-address)
    
    - [User Endpoints](#user-endpoints)

        - [Add User](#add-user)
        - [Update User](#update-user)
        - [Delete User](#delete-user)

    - [Demo Endpoint](#demo-endpoint)

        - [Reset Database](#reset-database)






## Installation

### With Docker Compose

Our API is available as a Docker container hosted on the GitHub Container Repository. This can be run alongside Redis, RediSearch, and other prepackaged containerized applications using our Docker Compose file.

#### Install Docker and Docker Compose

Follow the guides at [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) for platform-specific Docker installation instructions. 

#### Download the Docker Compose File

Enter the following command into a MacOS, Linux, or Windows Subsystem for Linux (WSL) terminal This downloads our Docker Compose file from GitHub as compose.yaml:

```
curl https://raw.githubusercontent.com/rohitgibson/capstone_group_8/main/compose.yaml -o compose.yaml
```

#### Install and Run API and Dependencies

In the same directory, run the following command to install and run our API and its dependencies in a Docker container:

```
docker compose up
```

An alternative way to start the Docker Compose file is with the ```--detach``` flag:
```
docker compose up --detach
```
which starts the container(s) independently of your current terminal instance. Otherwise, exiting the terminal in which the container is running will also terminate the containers.

## Usage

### Authentication

Our API endpoints require HTTP Basic Auth. When the API first starts, three sets of credentials (referred to throughout this document and our codebase as “Users”) are  are created by default and persisted with our SQLite auth database. Three tiers exist: Basic, Admin, and Root.  

#### Basic User

Basic users can read (verify) addresses using the **Search** endpoint but are unable to perform modifications (add, update, or delete) to the database. The authentication database is entirely inaccessible to this role.

##### Auth Credentials:

```
Username: basic
Password: basic
```

##### Accessible Endpoints:

```
http://{url}/api/address/search
```

#### Admin User

Admin users are able to perform CRUD (add, search/verify, update, and delete) operations on the address database. They are unable to access the `Demo` and `Users` endpoints and cannot access the authentication database.

##### Auth Credentials:

```
Username: admin
Password: admin
```

##### Accessible Endpoints:

```
http://{url}/api/address/modify/add
http://{url}/api/address/search
http://{url}/api/address/modify/update
http://{url}/api/address/modify/delete
```

#### Root User

The Root user was created to fulfill a need to have endpoints for quickly resetting our database for demos (removing all data and adding the addresses in the Excel file) and for managing users (adding, editing, and deleting them). While this could be done with a normal admin user, these endpoints are outside the scope of the requirements and have potentially serious consequences if in the wrong hands. **These default credentials will be changed for our in-class demo; these endpoints are solely for our use during the class demonstration.**

##### Auth Credentials:

```
Username: root
Password: root
```

##### Accessible Endpoints:

```
http://{url}/api/address/modify/add
http://{url}/api/address/search
http://{url}/api/address/modify/update
http://{url}/api/address/modify/delete
http://{url}/api/users/add
http://{url}/api/users/update
http://{url}/api/users/delete
http://{url}/api/demo/resetdb
```

### Endpoints

#### Address Endpoints

##### Add Address

###### Endpoint:

```
http://{url}/api/address/modify/add
```

###### Authorized Roles:

- Root
- Admin

###### Permitted Method(s):

- POST

###### Request Model (AddAddress):

```
{
    "address": {
        "addressLine1": String,
        "addressLine2": String,
        "city": String,
        "stateProv": String,
        "postalCode": String,
        "country": String
    }
}
```

###### Response Model (RequestResponse)

```
{
    "requestType": String,
    "requestData": {
        One of:  
            - AddAddress
            - SearchAddress
            - UpdateAddress
            - DeleteAddress
            - None
    },
    "requestSuccess": Boolean,
    "responseStatusMsg": String,
    "responseData": {}
}
```

###### HTTP Response Codes:

- **201 - Created:** The address was successfully added to the database.
- **400 - Bad Request:** The data you sent doesn't match the expected model (AddAddress) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

##### Verify Address

###### Endpoint:

```
http://{url}/api/address/search
```

###### Authorized Roles:

- Root
- Admin
- Basic

###### Permitted Method(s):

- GET

###### Request Model (SearchAddress):

```
{
    "address": {
        "addressLine1": String,
        "addressLine2": String,
        "city": String,
        "stateProv": String,
        "postalCode": String,
        "country": String
    }
}
```

###### Response Model (RequestResponse)

```
{
    "requestType": String,
    "requestData": {
        One of:  
            - AddAddress
            - SearchAddress
            - UpdateAddress
            - DeleteAddress
            - None
    },
    "requestSuccess": Boolean,
    "responseStatusMsg": String,
    "responseData": {
        "addressVerified": Boolean,
        "recommendedAddresses": [
            {
                "key": String
                "address": {
                    "addressLine1": String,
                    "addressLine2": String,
                    "city": String,
                    "stateProv": String,
                    "postalCode": String,
                    "country": String
                }
            }
        ]
    }
}
```

###### HTTP Response Codes:

- **200 - OK:** The search query went through successfully (though it hasn't necessarily returned any recommended addresses).
- **400 - Bad Request:** The data you sent doesn't match the expected model (SearchAddress) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

##### Update Address

###### Endpoint:

```
http://{url}/api/address/modify/update
```

###### Authorized Roles:

- Root
- Admin

###### Permitted Method(s):

- POST

###### Request Model (UpdateAddress):

```
{
    "key": String
    "address": {
        "addressLine1": String,
        "addressLine2": String,
        "city": String,
        "stateProv": String,
        "postalCode": String,
        "country": String
    }
}
```

###### Response Model (RequestResponse)

```
{
    "requestType": String,
    "requestData": {
        One of:  
            - AddAddress
            - SearchAddress
            - UpdateAddress
            - DeleteAddress
            - None
    },
    "requestSuccess": Boolean,
    "responseStatusMsg": String,
    "responseData": {}
}
```

###### HTTP Response Codes:

- **201 - Created:** The address was successfully updated.
- **400 - Bad Request:** The data you sent doesn't match the expected model (UpdateAddress) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **404 - Resource Not Found:** Applies to any request where the key provided does not exist in the database.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

##### Delete Address

###### Endpoint:

```
http://{url}/api/address/modify/delete
```

###### Authorized Roles:

- Root
- Admin

###### Permitted Method(s):

- POST

###### Request Model (SearchAddress):

```
{
    "key": String
}
```

###### Response Model (RequestResponse)

```
{
    "requestType": String,
    "requestData": {
        One of:  
            - AddAddress
            - SearchAddress
            - UpdateAddress
            - DeleteAddress
            - None
    },
    "requestSuccess": Boolean,
    "responseStatusMsg": String,
    "responseData": {}
}
```

###### HTTP Response Codes:

- **200 - Created:** The address was successfully deleted.
- **400 - Bad Request:** The data you sent doesn't match the expected model (DeleteAddress) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **404 - Resource Not Found:** Applies to any request where the key provided does not exist in the database.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

#### User Endpoints

##### Add User

###### Endpoint:

```
http://{url}/api/users/add
```

###### Authorized Roles:

- Root

###### Permitted Method(s):

- POST

###### Request Model (UserCheck):

```
{
    "username": String,
    "password": String,
    "role": String
}
```

###### Response Model:

None

###### HTTP Response Codes:

- **201 - Created:** The user was successfully created.
- **400 - Bad Request:** The data you sent doesn't match the expected model (UserCheck) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

##### Update User

###### Endpoint:

```
http://{url}/api/users/update
```

###### Authorized Roles:

- Root

###### Permitted Method(s):

- POST

###### Request Model (UserUpdate):

```
{
    "username": String
    "changes": {
        "username": String,
        "password": String,
        "role": String
    }
}
```

###### Response Model:

None

###### HTTP Response Codes:

- **201 - Created:** The user was successfully created.
- **400 - Bad Request:** The data you sent doesn't match the expected model (UserUpdate) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

##### Delete User

###### Endpoint:

```
http://{url}/api/users/delete
```

###### Authorized Roles:

- Root

###### Permitted Method(s):

- POST

###### Request Model (UserDelete):

```
{
    "username": String
}
```

###### Response Model:

None

###### HTTP Response Codes:

- **200 - Created:** The user was successfully created.
- **400 - Bad Request:** The data you sent doesn't match the expected model (UserDelete) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

#### Demo Endpoint

##### Reset Database

###### Explanation:

This endpoint exists for the sole purpose of being able to (1) drop all records from the address database, (2) add every (valid) address provided in D2L, and (3) re-establish the search index for address verification. While bulk address ingest is possible with the standard `Add Address` endpoint and bulk key deletion is available with the `Delete Address` endpoint, this streamlines these operations for our in-class API demo. 

###### Endpoint:

```
http://{url}/api/demo/resetdb
```

###### Authorized Roles:

- Root

###### Permitted Method(s):

- POST

###### Request Model:

None

###### Response Model:

None

###### HTTP Response Codes:

- **200 - Created:** The user was successfully created.
- **400 - Bad Request:** The data you sent doesn't match the expected model (UserDelete) for this endpoint.
- **403 - Forbidden:** Applies to any request that is either not authenticated or where the authenticated user's role is not permitted to access the endpoint.
- **500 - Internal Server Error:** A catchall miscellaneous response code for database problems or errors that have not previously been anticipated during development.

