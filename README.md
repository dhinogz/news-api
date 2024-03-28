# News Site Project
This is a programming coursework. You will use the Django web framework toimplement a RESTful web API for a news agency. The API should adhere toexact specifications set out in this document. You will also write a simple newsaggregator application for collecting news from all the APIs you and yourcolleagues in this module will have developed as part of this coursework.:wq

# Endpoints /api
## POST /login
  - request
    - application/x-www-form-urlencoded 
      - username
      - password
  - response
    - succesful
      - 200 OK 
      - text/plain payload with welcome message
    - failed
      - appropiate status code
      - explanation in text/plain
## POST /logout
  - request
    - no payload
  - response
    - succesful
      - 200 OK
      - text/plain with goodbye message
    - failed
      - appropiate status code
      - explanation in text/plain
## POST /stories
  - request
    - application/json
      - headline
      - category
      - region
      - details
    - user must be logged in
  - response
    - succesful
      - 201 CREATED
    - failed
      - 503 SERVICE UNAVAILABLE
      - explanation in text/plain
## GET /stories
  - request
    - application/x-www-form-urlencoded
      - story_cat
        - "*" is any
      - story_region
        - "*" is any
      - story_date
        - "*" is any
        - filters stories at or after date
  - response
    - success
      - 200 OK
      - application/json
        - stories array
          - key
          - headline
          - story_cat
          - story_region
          - author
          - story_date
          - story_details
    - fail (no stories found)
      - 404 NOT FOUND
      - explanation in text/plain
## DELETE /stories/:id
  - request
    - success
      - 200 OK
    - failed
      - 503 SERVICE UNAVAILABLE
      - explanation in text/plain
  - response
    
