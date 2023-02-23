# Congregate Server Side API

This application is an API built with Django REST Framework (DRF) that lets users join groups of users who can vote on event activities that for the group. When the voting time expires, the winning activity is assigned to the event and a google calendar invitation is sent to each user of the group.

# Link to Production Application

https://congregate.onrender.com

Documentation starts here:

### API ENDPOINTS

| HTTP Verbs | Endpoints            | Action                              |
| ---------- | -------------------- | ----------------------------------- |
| POST       | /register            | Register new user                   |
| GET        | /\<username\>/home   | User home page                      |
| GET        | /\<username\>/groups | List all of the user's groups       |
| GET        | /group/\<group_id\>  | Group home page                     |
| POST       | /add-user-group      | Join a user to the group            |
| POST       | /new/event           | Create a new event for the group    |
| GET        | /event/\<event_id\>  | Event home page                     |
| POST       | /new/activity        | Create a new activity for the event |

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

## Join a user to the group

### request

```txt
POST /add-user-group/
```

```json
{
  "username": "jcox",
  "group_id": 3
}
```

### response

```json
200 OK

{
	"id": 3,
	"title": "Just OK Group",
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
			"start_time": "2023-02-23T06:14:53.955409Z",
			"vote_closing_time": "2023-02-23T06:14:53.955425Z",
			"group": 3
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

## Create a new event for the group

### request

Requires event title, group_id, voting (T/F), date, and vote_closing_time

```txt
POST /new/event
```

```json
{
  "title": "Girls' Night Out!!",
  "group_id": 1,
  "voting": true,
  "date": "2023-02-24",
  "vote_closing_time": "2023-02-24T20:02:13.000Z"
}
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
	"admin": "jcox"
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
	"group": "Just OK Group",
	"voting": true,
	"start_time": "2023-02-23T06:14:53.955409Z",
	"vote_closing_time": "2023-02-23T06:14:53.955425Z",
	"activity_list": []
}
```

## Create a new activity for the event

### request

Requires title, event_id, start_time, end_time, and description

```txt
POST /new/activity/
```

### response

```json
{
  "title": "Fun activity!",
  "event_id": 1,
  "description": "We'll have so much fun!"
}
```