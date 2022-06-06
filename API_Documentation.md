## Table of Contents
- [Registration](#registration)
- [Authentication - Login to get Token](#login)
- [Google Sign Up - Sign Google User](#google_user)
- [Change Password ](#ChangePassword)
- [Register Libarian User](#libarian_register)
- [View Details of Signed In User](#DetailsOfSignedInUser)
- [User Account Details](#UserAccountDetails)
- [View User Account List](#UsersList)
- [Delete User](#delete_user)
- [Activate and Deactivate Users By Admin or Staff](#activate_and_deactivate)
- [Create Book Category](#add_category)
- [List of Book Categories](#get_all_category)
- [Delete Book Category](#delete_category)
- [Create Book ](#add_book)
- [List of Books](#get_all_books)
- [Delete Book ](#delete_book)
- [Update of a Book ](#update_book)
- [User request book](#book_request)
- [Admin List of All Book Requests](#admin_view_book_request)
- [Admin Approve of Book Requests](#admin_approve_book_request)
- [Admin delete of Book Requests](#admin_delete_book_request)
- [User's view of all Book Requests](#user_all_books_request)
- [User return of a Book Approved](#user_return_books)
- [Admin View of Book Return Request](#admin_view_user_returned_books)
- [Admin Approve Book Return Request](#admin_approve_user_return_books)

<a name="registration"></a>

## Registration

The register API will accept user credentials:
username,email and password and saves it to the database.

### Request Information

| Type | URL             |
| ---- | --------------- |
| POST | /user/register/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                   |
| ------------- | ------ | -------- | ----------------------------- |
| username      | String | true     | The username of the user      |
| email_address | String | true     | email address of the user     |
| password      | String | true     | Password for the user account |

### Error Responses

| Code | Message                                   |
| ---- | ----------------------------------------- |
| 400  | "users with this username already exists" |
| 400  | "users with this email already exists."   |
| 400  | "This field may not be blank."            |


### Successful Response Example

```
{
    "status": "success",
    "details": "User created successfully",
    "data": {
        "email_address": "user@user.com"
        "username" : "user"
    }
}
```

<a name="login"></a>

## Authentication - Login

This Api endpoint accepts user's email and password
and authenticates the user and return a token.
The token can be used by the user to authenticate their
identity.

**Note** If an account was registered by an admin and a password was generated, this method will return a specific error Message "change password" and no token. Untill the generated password is changed.

### Request Information

| Type | URL          |
| ---- | ------------ |
| POST | /user/login/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |

### Get Parameter

| Property Name | type   | required | Description             |
| ------------- | ------ | -------- | ----------------------- |
| email_address | string | true     | email address for login |
| password      | string | true     | password for login      |

### JSON Body

| Property Name | type   | required | Description             |
| ------------- | ------ | -------- | ----------------------- |
| email_address | string | true     | email address for login |
| password      | string | true     | password for login      |

### Error Responses

| Code | Message                                |
| ---- | -------------------------------------- |
| 400  | email_address: This field is required. |
| 400  | password: This field is required.      |
| 401  | change password                        |

### Successful Response Example

```
{
   "status":"success",
   "details":"user logged in successfully",
   "data":{
            "email_address":"user@user.com,
            "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImVtbWFudWVsb2t5ZXJlZ3lhdGVuZyIsImVtYWlsIjoiZW9neWF0ZW5nQHN0LnVnLmVkdS5naCIsImV4cCI6MTY1NDM1MDkxOX0.NyIekhV7vOvewletV22mIplzO2dZrMqL0jf-S8VZioU",
            "libarian":True
         })
}
```

<a name="google_user"></a>

## Authentication Google Users

This Api endpoint accepts auth_token and authenticate users with google.

**Note** This endpoint accepts only auth_token from OAuth 2.0.

### Request Information

| Type | URL           |
| ---- | ------------- |
| POST | /user/google/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |

### Post Parameter

| Property Name | type   | required | Description                                         |
| ------------- | ------ | -------- | --------------------------------------------------- |
| auth_token    | string | true     | auuth token to be authenticated with google systems |


### JSON Body

| Property Name | type   | required | Description                                        |
| ------------- | ------ | -------- | -------------------------------------------------- |
| auth_token    | string | true     | auth token to be authenticated with google systems |


### Error Responses

| Code | Message             |
| ---- | ------------------- |
| 400  | auth_token:required |
| 400  | invalid token       |
| 400  | invalid expired     |
### Successful Response Example
```
{
      "status":"success",
      "detail":"User signup successful",
      "data":{
              "username": "user",
              "email_address":"user@user.com",
              "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImVtbWFudWVsb2t5ZXJlZ3lhdGVuZyIsImVtYWlsIjoiZW9neWF0ZW5nQHN0LnVnLmVkdS5naCIsImV4cCI6MTY1NDM1MDkxOX0.NyIekhV7vOvewletV22mIplzO2dZrMqL0jf-S8VZioU"}
}
```
<a name="ChangePassword"></a>

## Change Password - ChangePassword

The Reset Password API makes helps users
to create a new password after they have provided they have beign authenticated. User must login before accessing the change password endpoint.

### Request Information
| Type | URL                   |
| ---- | --------------------- |
| PUT  | /user/passwordchange/ |

### Header

| Type          | Property name         |
| ------------- | --------------------- |
| Allow         | PUT                   |
| Content-Type  | application/json      |
| Authorization | Bearer {TOKEN.access} |

### JSON Body

| Property Name | type   | required | Description       |
| ------------- | ------ | -------- | ----------------- |
| old_password  | string | true     | old user Password |
| new_password  | string | true     | new User Password |

### Error Responses

| Code | Message                               |
| ---- | ------------------------------------- |
| 400  | Wrong old password                    |
| 401  | UNAUTHORIZED                          |
| 400  | BAD REQUEST                           |
| 400  | new_password: This field is required. |
| 400  | old_password: This field is required. |

### Successful Response Example
```
{
  "status":"success",
  "details": "Password changed successfully",
  "data": {
     "username":"user",
     "email_address":"user@user.com",
     "libarian":False
    }
}
```
<a name="libarian_register"></a>

## Register Libarian User

This API endpoint is used to create libarians.
**Note** Only authenticated, is admin users can access this endpoint. Passwords are generated for registered libarians and required to change upon login.

### Request Information

| Type | URL         |
| ---- | ----------- |
| POST | /user/list/ |
### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | POST             |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type   | required | Description              |
| ------------- | ------ | -------- | ------------------------ |
| username      | string | false    | Should be Users username |
| email         | string | true     | Should be email address  |

### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | email required |
| 400  | BAD REQUEST    |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
{
    "status": "success",
    "details":"Libarian registered successfully",
    "data": {
              "username": "libarian",
              "email_address": "libarian@libarian.com",
              "password": "password"
            })
}
```

<a name="DetailsOfSignedInUser"></a>

## Details of Signed In User

This API endpoint provides account information a signed in user using tokens

**Note** Only authenticated user can access this endpoint

### Request Information

| Type | URL           |
| ---- | ------------- |
| GET  | /user/detail/ |

### Header

| Type          | Property name         |
| ------------- | --------------------- |
| Allow         | GET                   |
| Content-Type  | application/json      |
| Authorization | Bearer {TOKEN.access} |

### Error Responses

| Code | Message          |
| ---- | ---------------- |
| 401  | UNAUTHORIZED     |
| 404  | NOT FOUND        |
| 404  | Token is invalid |

### Successful Response Example

```
{
    "status": "success",
    "details": "User details found",
    "data": {
        "id": 1,
        "username": "user",
        "email_address": "user@user.com",
        "libarian": false
    }
}
```


<a name="UserAccountDetails"></a>

## User Account Details

This API endpoint provides a detail view of a user's account.
**Note** Only authenticated and libarians users can access this endpoint

### Request Information

| Type | URL                  |
| ---- | -------------------- |
| GET  | /user/list/{int:pk}/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message      |
| ---- | ------------ |
| 401  | UNAUTHORIZED |
| 404  | NOT FOUND    |


### Successful Response Example
```
{
    "id": 1,
    "username": "user",
    "email_address": "user@user.com",
    "is_active": true,
    "is_superuser": false
}
```


<a name="UsersList"></a>

## Users List
This API endpoint shows a complete list of all users.
**Note** Only authenticated and Libarian users can access this endpoint.

### Request Information

| Type | URL         |
| ---- | ----------- |
| GET  | /user/list/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message      |
| ---- | ------------ |
| 401  | UNAUTHORIZED |
| 401  | UNAUTHORIZED |


### Successful Response Example
```
[
    {
        "id": 1,
        "username": "admin",
        "email_address": "admin@admin.com",
        "is_active": true,
        "is_superuser": true
    },
    {
        "id": 2,
        "username": "user",
        "email_address": "user@user.com",
        "is_active": true,
        "is_superuser": false
    }
]
```

<a name="delete_user"></a>

## Delete User

This API endpoint is used for deleting users from the system.
**Note** Only authenticated and superuser users can access this endpoint

### Request Information

| Type   | URL                 |
| ------ | ------------------- |
| DELETE | /user/list/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | DELETE           |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message      |
| ---- | ------------ |
| 401  | UNAUTHORIZED |
| 403  | FORBIDDEN    |
| 404  | NOT FOUND    |

### Successful Response Example

```
{
      "status": "success",
      "details": "User deleted successfully",
}
```

<a name="activate_and_deactivate"></a>

## Activate and Deactivate Users By Admin or Staff

The Activate and Deactivate Users API enables libarians to
to either activate or deactivate users on the platform.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                 |
| ---- | ------------------- |
| PUT  | /user/list/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | PUT              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type    | required | Description                                        |
| ------------- | ------- | -------- | -------------------------------------------------- |
| is_active     | boolean | true     | False, if admin want to deactivate. otherwise True |

### Error Responses

| Code | Message                     |
| ---- | --------------------------- |
| code | message                     |
| 400  | is_active field is required |
| 401  | UNAUTHORIZED                |
| 400  | BAD REQUEST                 |
| 403  | FORBIDDEN                   |

### Successful Response Example
```
{
    "status": "success",
    "details": "user status changed",
    "data": {
        "id": 1,
        "username": "user@user.com",
        "is_active": true,
        "libarian": false
    }
}
```
<a name="add_category"></a>

## Create Book Category

This API endpoint is used to create book category.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL           |
| ---- | ------------- |
| POST | /api/catalog/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | POST             |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type   | required | Description            |
| ------------- | ------ | -------- | ---------------------- |
| name          | string | true     | Title of book category |

### Error Responses

| Code | Message             |
| ---- | ------------------- |
| 400  | BAD REQUEST         |
| 400  | name field required |
| 401  | UNAUTHORIZED        |
| 403  | FORBIDDEN           |

### Successful Response Example

```
{
      "status": "success",
      "details": "catalogue created",
      "data": {
              "id": 1,
              "name": "Artificial Inteligence",
      }
}
```

<a name="get_all_category"></a>

## Get Book Category

This API endpoint is used to create book category.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL           |
| ---- | ------------- |
| GET  | /api/catalog/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message      |
| ---- | ------------ |
| 400  | BAD REQUEST  |
| 401  | UNAUTHORIZED |
| 403  | FORBIDDEN    |

### Successful Response Example

```
[
    {
        "id": 1,
        "name": "History"
    },
    {
        "id": 2,
        "name": "Social Science"
    }
]

```

<a name="delete_category"></a>

## Delete Book Category

This API endpoint is used to delete a book category.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type   | URL                   |
| ------ | --------------------- |
| DELETE | /api/catalog/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | DELETE           |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | BAD REQUEST    |
| 400  | Does not exits |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
{
      "status": "success",
      "details":"category deleted"
}
```

<a name="add_book"></a>

## Create Book

This API endpoint is used to create book to a category.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL               |
| ---- | ----------------- |
| POST | /api/admin/books/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | POST             |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type    | required | Description          |
| ------------- | ------- | -------- | -------------------- |
| category      | string  | true     | Id of book category  |
| title         | string  | true     | Title of book        |
| description   | string  | true     | Description of book  |
| is_available  | boolean | true     | Availability of book |
| image         | image   | true     | Image of book        |



### Error Responses

| Code | Message         |
| ---- | --------------- |
| 400  | BAD REQUEST     |
| 400  | feilds required |
| 401  | UNAUTHORIZED    |
| 403  | FORBIDDEN       |

### Successful Response Example

```
{
    "status": "success",
    "details": "book added successfully",
    "data": {
        "category_id": 2,
        "title": "Robotics for all",
        "description": "I am testing this",
        "is_available": true,
        "image": "/media/images/2022/06/05/57065066.png"
    }
}
```

<a name="get_all_books"></a>

## Get all Books

This API endpoint is used to view all book.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL         |
| ---- | ----------- |
| GET  | /api/books/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message      |
| ---- | ------------ |
| 400  | BAD REQUEST  |
| 401  | UNAUTHORIZED |
| 403  | FORBIDDEN    |

### Successful Response Example

```
[
    {
        "id": 1,
        "name": "History"
    },
    {
        "id": 2,
        "name": "Social Science"
    }
]

```

<a name="delete_book"></a>

## Delete Book

This API endpoint is used to delete a book.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type   | URL                 |
| ------ | ------------------- |
| DELETE | /api/books/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | DELETE           |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | BAD REQUEST    |
| 400  | Does not exits |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
{
      "status": "success",
      "details":"book deleted"
}
```



<a name="update_book"></a>

## Update a Book

This API endpoint is used to update a book.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                 |
| ---- | ------------------- |
| PUT  | /api/books/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | PUT              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type    | required | Description          |
| ------------- | ------- | -------- | -------------------- |
| category      | string  | true     | Id of book category  |
| title         | string  | true     | Title of book        |
| description   | string  | true     | Description of book  |
| is_available  | boolean | true     | Availability of book |
| image         | image   | true     | Image of book        |

**note** Either field will update.
### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | BAD REQUEST    |
| 400  | Does not exist |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
{
    "status": "success",
    "details": "Book updated successfully",
    "data": {
        "category_id": 2,
        "title": "Robotics for all",
        "description": "This is a updated description",
        "is_available": false,
        "image": "/media/images/2022/06/05/57065066.png"
      }
}
```

<a name="book_request"></a>

## User make  a book request

This API endpoint is used by the user to request for a book.
**Note** Only authenticated users can access this endpoint.

### Request Information

| Type | URL                  |
| ---- | -------------------- |
| POST | /users/request/book/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | POST             |
| Content-Type  | application/json |
| Authorization | Token            |

### JSON Body

| Property Name | type    | required | Description |
| ------------- | ------- | -------- | ----------- |
| book          | integer | true     | Id of book  |


### Error Responses

| Code | Message                |
| ---- | ---------------------- |
| 400  | book field is required |
| 400  | BAD REQUEST            |
| 400  | Does not exist         |
| 401  | UNAUTHORIZED           |
| 403  | FORBIDDEN              |

### Successful Response Example
```
{
    "status": "success",
    "details": "book requested",
    "data": {
        "id": 3,
        "title": "Robotics for all"
    }
}
```

<a name="admin_view_book_request"></a>

## Admin View all book requests

This API endpoint is used by the libarian to view all book requests.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                      |
| ---- | ------------------------ |
| GET  | /users/request/booklist/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |


### Error Responses

| Code | Message      |
| ---- | ------------ |
| 400  | BAD REQUEST  |
| 401  | UNAUTHORIZED |
| 403  | FORBIDDEN    |

### Successful Response Example
```
[
    {
        "id": 1,
        "user": "admin@admin.com",
        "book": "Robotics for all",
        "is_requested": true,
        "is_approved": false,
        "is_returned": false
    }
]
```
<a name="admin_approve_book_request"></a>

## Admin Approve book requests

This API endpoint is used by the libarian to approve all book requests.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                              |
| ---- | -------------------------------- |
| PUT  | /users/request/booklist/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | PUT              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type    | required | Description                                    |
| ------------- | ------- | -------- | ---------------------------------------------- |
| is_approved   | boolean | true     | True is the book is approveed. False otherwise |

### Error Responses

| Code | Message                       |
| ---- | ----------------------------- |
| 400  | BAD REQUEST                   |
| 400  | is_approved field is required |
| 400  | does not exist                |
| 401  | UNAUTHORIZED                  |
| 403  | FORBIDDEN                     |

### Successful Response Example
```
{
    "status": "success",
    "details": "request approved",
    "data": {
        "id": 1,
        "book": "Robotics for all",
        "is_approved": true
    }
}
```

<a name="admin_delete_book_request"></a>

## Delete Request

This API endpoint is used to delete a request.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type   | URL                             |
| ------ | ------------------------------- |
| DELETE | /users/request/booklist{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | DELETE           |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | BAD REQUEST    |
| 400  | Does not exits |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
{
      "status": "success",
      "details":"request deleted"
}
```

<a name="user_all_books_request"></a>

## User View all book requests

This API endpoint is used by the user to view all their book requests.
**Note** Only authenticated users can access this endpoint.

### Request Information

| Type | URL                  |
| ---- | -------------------- |
| GET  | /users/request/list/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |


### Error Responses

| Code | Message      |
| ---- | ------------ |
| 400  | BAD REQUEST  |
| 401  | UNAUTHORIZED |
| 403  | FORBIDDEN    |

### Successful Response Example
```
[
    {
        "id": 1,
        "book": "Robotics for all",
        "is_approved": true,
        "is_returned": false
    }
]


```
<a name="user_return_books"></a>


## User return Approved book

This API endpoint is used by the libarian to approve all book requests.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                          |
| ---- | ---------------------------- |
| PUT  | /users/request/list/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | PUT              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name | type    | required | Description                                             |
| ------------- | ------- | -------- | ------------------------------------------------------- |
| is_returned   | boolean | true     | True if the user is returning the book. False otherwise |

### Error Responses

| Code | Message                       |
| ---- | ----------------------------- |
| 400  | BAD REQUEST                   |
| 400  | is_returned field is required |
| 400  | does not exist                |
| 401  | UNAUTHORIZED                  |
| 403  | FORBIDDEN                     |

### Successful Response Example
```
{
    "status": "success",
    "details": "book returned, waiting approval",
    "data": {
        "book": "Robotics for all",
        "is_returned": true
    }
}
```

<a name="admin_view_user_returned_books"></a>


## Admin list of returned books

This API endpoint is used by the libarian to view all books returned by borrowers.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                          |
| ---- | ---------------------------- |
| GET  | /users/request/admin/return/ |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | GET              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |


### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | BAD REQUEST    |
| 400  | does not exist |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
[
    {
        "id": 1,
        "user": "admin@admin.com",
        "book": "Robotics for all",
        "is_approved": true,
        "is_returned": true,
        "is_approved_return": false
    }
]
```

<a name="admin_approve_user_return_books"></a>


## Admin approve of returned book

This API endpoint is used by the libarian to approve of all books returned by borrowers.
**Note** Only authenticated, libarian users can access this endpoint.

### Request Information

| Type | URL                                  |
| ---- | ------------------------------------ |
| PUT  | /users/request/admin/return/{int:pk} |

### Header

| Type          | Property name    |
| ------------- | ---------------- |
| Allow         | PUT              |
| Content-Type  | application/json |
| Authorization | IsSuperUser      |

### JSON Body

| Property Name      | type    | required | Description                                                    |
| ------------------ | ------- | -------- | -------------------------------------------------------------- |
| is_approved_return | boolean | true     | True if the admin approves return of the book. False otherwise |

### Error Responses

| Code | Message                              |
| ---- | ------------------------------------ |
| 400  | BAD REQUEST                          |
| 400  | is_approved_return field is required |
| 400  | does not exist                       |
| 401  | UNAUTHORIZED                         |
| 403  | FORBIDDEN                            |

### Successful Response Example

```
{
    "status": "success",
    "details": "book return approved",
    "data": {
        "id": 1,
        "is_approved": true,
        "is_returned": true,
        "is_approved_return": true
    }
}
```

