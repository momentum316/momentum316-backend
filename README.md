# Congregate Server Side API

This application is an API built with Django REST Framework (DRF) that lets users join groups of users who can vote on event activities that for the group. When the voting time expires, the winning activity is assigned to the event and a google calendar invitation is sent to each user of the group.

# Link to Production Application

https://congregate.onrender.com

Documentation starts here:

### API ENDPOINTS

| HTTP Verbs | Endpoints                          | Action                                     |
| ---------- | ---------------------------------- | ------------------------------------------ |
| POST       | /register                          | Register new user                          |
| POST       | /login                             | Login or create new user                   |
| GET        | /\<username\>/home                 | User home page                             |
| PATCH      | /\<username\>/home                 | User edits own attributes                  |
| GET        | /\<username\>/profile              | View another user's profile                |
| GET        | /\<username\>/groups               | List user's groups                         |
| GET        | /\<username\>/open-votes           | List user's events with open voting        |
| POST       | /new/group                         | Create a new group                         |
| GET        | /group/\<group_id\>                | Group home page                            |
| PATCH      | /group/\<group_id\>                | Edit group home page, add user to group    |
| POST       | /new/event                         | Create a new event for the group           |
| GET        | /event/\<event_id\>                | Event home page                            |
| PATCH      | /event/\<event_id\>                | Update an event                            |
| DELETE     | /event/\<event_id\>                | Delete an event                            |
| POST       | /new/activity                      | Create a new activity for the event        |
| GET        | /activity/\<activity_id\>          | Activity home page                         |
| PATCH      | /activity/\<activity_id\>          | Update an activity                         |
| DELETE     | /activity/\<activity_id\>          | Delete an activity                         |
| PATCH      | /vote/\<vote_id\>                  | User can change vote                       |
| POST       | /submit-vote/                      | User submits votes for an event            |
| POST       | /new/pending-activity              | Create a new pending activity for the user |
| GET        | /pending/<int:pending_activity_id> | Get pending activity                       |
| PATCH      | /pending/<int:pending_activity_id> | Update a pending activity                  |
| DELETE     | /pending/<int:pending_activity_id> | Delete a pending activity                  |

## Register a new user

### request

Username, first name, last name, and email are required.

```txt
POST /register
```

```json
{
  "username": "bobuser",
  "first_name": "Bob",
  "last_name": "User",
  "email": "fakeemail@gmail.com"
}
```

### response

```json
200 OK

{
	"id": 6,
	"username": "bobuser",
	"first_name": "Bob",
	"last_name": "User",
	"email": "fakeemail@gmail.com",
	"avatar": null
}
```

## Login

###

```txt
POST /login
```

```json
{
  "email": "fakeemail@gmail.com",
  "username": "fakeyfake",
  "first_name": "Fake",
  "last_name": "Email"
}
```

### response

```json
200 OK

{
	"user": {
		"id": "6",
		"email": "fakeemail@gmail.com",
		"username": "fakeyfake",
		"first_name": "Fake",
		"last_name": "Email",
		"avatar": null
	},
	"token": "y22833c083d494b7c2683f53457376d7d8379a40"
}
```

## User home page

### request

```txt
GET /<username>/home
```

### response

```json
200 OK

{
	"id": 1,
	"username": "bobuser",
	"first_name": "Bob",
	"last_name": "User",
	"email": "fakeemail@gmail.com",
	"avatar": null,
	"group_list": [],
}
```

## List all of the user's groups

### request

```txt
GET /<username>/groups
```

### response

```json
200 OK
[
	{
		"id": 2,
		"title": "Boring Group",
		"members": [
			"bjenkins",
			"congreg8",
			"testuser"
		],
		"admin": "bjenkins",
		"event_list": []
	},
	{
		"id": 1,
		"title": "Party Group",
		"members": [
			"jcox",
			"bjenkins",
			"congreg8",
			"testuser",
			"testuser1",
			"justcapel"
		],
		"admin": "jcox",
		"event_list": [
			{
				"id": 1,
				"title": "Friday night hang",
				"group": "Party Group",
				"voting": false,
				"start_time": "2023-02-23T02:20:22.450430Z",
				"vote_closing_time": "2023-02-23T02:20:22.450447Z",
				"activity_list": [
					{
						"id": 2,
						"title": "test new activity",
						"description": "I want this to work.",
						"start_time": "2023-02-23T16:28:11.784924Z",
						"end_time": "2023-02-23T16:28:11.784939Z",
						"event": 1
					}
				]
			},
			{
				"id": 2,
				"title": "Girls' Night Out!!",
				"group": "Party Group",
				"voting": false,
				"start_time": "2023-02-23T02:20:58.050376Z",
				"vote_closing_time": "2023-02-23T02:20:58.050393Z",
				"activity_list": []
			}
		]
	}
]
```

## List a user's events that are still open for voting

### request

```txt
GET /<username>/open-votes
```

### response

```json
200 OK

[
	{
		"id": 18,
		"title": "Weekend event",
		"voting": true,
		"date": "2023-02-24T00:00:00Z",
		"activity_list": [],
		"group": "Saturday night",
		"vote_closing_time": "2023-02-27T10:48:00Z",
		"decided": false
	},
	{
		"id": 20,
		"title": "Friday night hang?",
		"voting": true,
		"date": "2023-03-03T23:00:00Z",
		"activity_list": [],
		"group": "Saturday night",
		"vote_closing_time": "2023-03-03T23:00:00Z",
		"decided": false
	}
]
```

## Create a new group

Requires authentication token and group title in request body

### request

```txt
POST new/group/
```

```json
{
  "title": "Another awesome group"
}
```

### response

```json
200 OK

{
	"group": {
		"id": 9,
		"title": "Another awesome group",
		"admin": "jcox"
	}
}
```

## Group home page

### request

```txt
GET /group/<group_id>
```

### response

```json
200 OK

{
	"id": 1,
	"title": "Party Group",
	"members": [
		"jcox",
		"bjenkins",
		"congreg8",
		"testuser",
		"testuser1",
		"justcapel"
	],
	"admin": "jcox",
	"event_list": [
		{
			"id": 1,
			"title": "Friday night hang",
			"voting": false,
			"start_time": "2023-02-23T02:20:22.450430Z",
			"vote_closing_time": "2023-02-23T02:20:22.450447Z",
			"group": 1
		},
		{
			"id": 2,
			"title": "Girls' Night Out!!",
			"voting": false,
			"start_time": "2023-02-23T02:20:58.050376Z",
			"vote_closing_time": "2023-02-23T02:20:58.050393Z",
			"group": 1
		}
	]
}
```

## Edit a group

Requires authentication

### request

```txt
PATCH /group/<group_id>/
```

```json
{
  "title": "Edited Group Title"
}
```

### response

```json
200 OK

{
	"id": 3,
	"title": "Edited Group Title",
	"members": [
		"jcox",
		"testuser1",
		"justcapel"
	],
	"admin": "justcapel",
	"event_list": [
		{
			"id": 3,
			"title": "This weekend",
			"voting": true,
			"date": "2023-02-23",
			"activity_list": [],
			"group": "Edited Group Title",
			"vote_closing_time": "2023-02-23T06:14:53.955425Z"
		}
	]
}
```

## Join a user to the group

### request

Requires authentication as well as the username in the request body

```txt
PATCH /group/<group_id>/
```

```json
{
  "username": "sammy"
}
```

### response

```json
200 OK

{
	"id": 3,
	"title": "Edited Group Title",
	"members": [
		"jcox",
		"testuser1",
		"justcapel",
		"sammy"

	],
	"admin": "justcapel",
	"event_list": [
		{
			"id": 3,
			"title": "This weekend",
			"voting": true,
			"date": "2023-02-23",
			"activity_list": [],
			"group": "Edited Group Title",
			"vote_closing_time": "2023-02-23T06:14:53.955425Z"
		}
	]
}
```

### response if user is already a member of the group

```json
409 Conflict

{
  "error": "jcox is already a member of the group"
}
```

## Remove user from group

### request

Requires authentication as well as username in request

```txt
PATCH /leave/<group_id>
```

```json
{
  "username": "bobuser"
}
```

### response

```json
200 OK
{
	"message": "bobuser has left the group"
}
```

## Create a new event for the group

### request

Requires authentication as well as event title, group_id, voting (T/F), date, and vote_closing_time

```txt
POST /new/event
```

```json
{
  "title": "Girls' Night Out!!",
  "group_id": 1,
  "voting": true,
  "date": "2023-02-24",
  "vote_closing_time": "2023-02-25T20:02:13.000Z"
}
```

### response

```json
200 OK

{
	"event": {
		"id": 1,
		"title": "Girls' Night Out!!",
		"voting": true,
		"date": "2023-02-26T23:00:00:000Z",
		"activity_list": [],
		"group": "Those Girls",
		"vote_closing_time": "2023-02-25T20:02:13.000Z",
		"decided": false
	}
}
```

\*\*\* Please note that default values are null for certain parameters, may institute defaults in the future.

## Event home page

### request

```txt
GET /event/<event_id>
```

### response

```json
200 OK

{
	"id": 3,
	"title": "This weekend",
	"voting": true,
	"group": "Just OK Group",
	"start_time": "2023-02-23T06:14:53.955409Z",
	"vote_closing_time": "2023-02-23T06:14:53.955425Z",
	"activity_list": [],
	"decided": false
}
```

## Update an event

### request

Requires authentication

```txt
PATCH /event/<event_id>/
```

```json
{
  "title": "Change this title"
}
```

### response

```json
200 OK

{
	"id": 3,
	"title": "Change this title",
	"voting": true,
	"date": "2023-02-23",
	"activity_list": [],
	"group": "Edited Group Title",
	"vote_closing_time": "2023-02-23T06:14:53.955425Z",
	"decided": false
}
```

## Delete an event

### request

Requires authentication

```txt
DELETE /event/<event_id>/
```

### response

```json
204 No Content
```

## Create a new activity for the event

### request

Requires authentication and title, event_id, start_time, end_time, and description

```txt
POST /new/activity/
```

```json
{
  "title": "Left-handed bowling night",
  "event_id": 1,
  "description": "You must use your left hand to bowl!",
  "location": "Uptown Bowling",
  "start_time": "2023-02-24T06:14:53.955425Z",
  "end_time": "2023-02-24T09:14:53.955425Z"
}
```

### response

```json
201 Created

{
  "activity": {
    "id": 3,
    "title": "Left-handed bowling night",
		"creator": "jcox",
    "description": "You must use your left hand to bowl!",
		"location": "Uptown Bowling",
    "start_time": "2023-02-24T06:14:53.955425Z",
    "end_time": "2023-02-24T09:14:53.955425Z",
		"total_votes": 0,
		"attendees": []
  }
}
```

## Update an activity

### request

Requires authentication

```txt
PATCH /activity/<activity_id>
```

```json
{
  "title": "Bowling night!"
}
```

### response

```json
200 OK

{
  "activity": {
    "id": 3,
    "title": "Bowling night!",
		"creator": "jcox",
    "description": "You must use your left hand to bowl!",
    "start_time": "2023-02-24T06:14:53.955425Z",
    "end_time": "2023-02-24T09:14:53.955425Z",
		"total_votes": 0,
		"attendees": []
  }
}

```

## Add attendee to activity

### request

Requires authentication, username passed in request body

```txt
PATCH /activity/<activity_id>
```

```json
{
  "username": "bobuser"
}
```

### response

```json
200 OK

{
  "activity": {
    "id": 3,
    "title": "Bowling night!",
		"creator": "jcox",
    "description": "You must use your left hand to bowl!",
    "start_time": "2023-02-24T06:14:53.955425Z",
    "end_time": "2023-02-24T09:14:53.955425Z",
		"total_votes": 0,
		"attendees": ["bobuser"]
  }
}
```

## Delete an activity

### request

Requires authentication

```txt
DELETE /activity/<activity_id>/
```

### response

```json
204 No Content
```

## User updates vote

Requires authentication

### request

```txt
PATCH /vote/<vote_id>/
```

```json
{
  "vote": 1
}
```

### response

```json
200 OK

{
	"id": 1,
	"voter": "jcox",
	"activity": "Vote activity",
	"vote": 1
}
```

## User submits votes for event

```txt
POST /submit-vote/
```

### request

```json
{
  "username": "congregate",
  "event_id": 6
}
```

### response

```json
200 OK

{
	"id": 6,
	"title": "test",
	"voting": true,
	"date": "2023-02-24T00:00:00Z",
	"activity_list": [
		{
			"id": 10,
			"title": "Bowling night",
			"event": 6,
			"creator": "bjenkins",
			"description": "I just wanna break triple digits",
			"start_time": "2023-02-26T16:00:00Z",
			"end_time": "2023-02-26T18:00:00Z",
			"total_votes": -2
		},
		{
			"id": 9,
			"title": "Capel's concert",
			"event": 6,
			"creator": "congreg8",
			"description": "Capel's band is sick",
			"start_time": "2023-02-26T19:00:00Z",
			"end_time": "2023-02-26T21:00:00Z",
			"total_votes": 4
		},
		{
			"id": 8,
			"title": "Go to the movies",
			"event": 6,
			"creator": "jcox",
			"description": "Let's watch that new Power Rangers, yo",
			"start_time": "2023-02-26T15:00:00Z",
			"end_time": "2023-02-26T17:00:00Z",
			"total_votes": 1
		},
	],
	"group": "Friday night",
	"vote_closing_time": "2023-02-25T20:02:13Z",
	"decided": true
}
```

## Create a new pending activity for the user

### request

Requires authentication and title, description

```txt
POST /new/pending-activity/
```

```json
{
  "title": "Rock climbing",
  "description": "Want to do this eventually"
}
```

### response

```json
201 Created

{
	"id": 4,
	"creator": "bob",
	"title": "Rock climbing",
	"description": "Want to do this eventually",
	"location": null,
	"start_time": null,
	"end_time": null,
	"image": null
}
```

## Update a pending activity

### request

Requires authentication

```txt
POST /pending/<int:pending_activity_id>/
```

```json
{
  "location": "Them there mountains"
}
```

### response

```json
200 OK

{
	"id": 4,
	"creator": "bob",
	"title": "Rock climbing",
	"description": "Want to do this eventually",
	"location": "Them there mountains",
	"start_time": null,
	"end_time": null,
	"image": null
}
```

## Delete a pending activity

### request

Requires authentication

```txt
DELETE /pending/<pending_activity_id>/
```

### response

```json
204 No Content
```
