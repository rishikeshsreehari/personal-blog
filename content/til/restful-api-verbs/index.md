---
title: "RESTful API Endpoints Should Not Have Verbs"
date: 2025-11-03
tiltags: ["programming", "api", "rest", "web-development"]
summary: "RESTful API endpoints should use nouns, not verbs. The HTTP method itself is the verb."
url: "/til/restful-api-no-verbs"
---

Today I learned that RESTful API endpoints should only use nouns, not verbs. 

I was building some endpoints for a project and had things like `/getUsers` and `/createUser`. 

They worked fine, but it's not proper REST design and somebody pointed out this to me.

The HTTP method (GET, POST, PUT, DELETE) already acts as the verb. So it should just be `/users` with the appropriate method. `GET /users` fetches them, `POST /users` creates one.