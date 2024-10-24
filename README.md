# Stroll BE Task 1

This task was implemented using FastAPI, a python backend library.

## Installation
After cloning the repo, run:
```bash
pip install -r requirements.txt
```

## Running locally
```bash
fastapi dev main.py
```
OR if you have Uvicorn installed:
```bash
uvicorn main:app --reload
```
Note: A local SQL database is created and seeded with sample data to aid illustration.

## Routes
GET `/question/{user_id}` - Assigns a question to a user for a given cycle.
Response:
```json
{
    "question_for_cycle": "question_text"
}
```

GET `/questions/{cycle_id}/{region_name}` - Fetches all questions for a given cycle and region.
Response:
```json
{
    "questions_for_this_cycle": [
        {
            "region_id": 1,
            "cycle_id": 2,
            "id": 3,
            "question_text": "Question 3"
        }
    ]
}
```

## Database Schema

| Table Name         | Columns                                                                 |
|--------------------|-------------------------------------------------------------------------|
| `regions`          | `id` (PK), `name` (VARCHAR, UNIQUE)   `users` are associated with a region |
| `questions`        | `id` (PK), `question_text` (TEXT), `region_id` (FK)   `questions are associated with a region |
| `question_cycles`           | `id` (PK), `start_date` (TIMESTAMP), `duration` (INTEGER)   `cycles are associated with a duration` |
| `assignments` | `id` (PK), `question_id` (FK), `cycle_id` (FK), `region_id` (FK)    |
| `users`            | `id` (PK), `username` (VARCHAR, UNIQUE), `region_id` (FK)               |

## Strategy
The main idea is to rotate questions based on the cycle duration, configurable at the region level. Each region follows its own cycle schedule, and the questions rotate every 7 days (or whatever the cycle configuration specifies). 

First step includes getting the cycle config for a given region, and then calculating which question to assign based on the current date and the cycle start date.

## Scalability considerations
Key considerations for scalability for thousands to millions of users included efficient caching using Redis. A mock implementation is included in the codebase.

Potential improvements to the system will include: 
- Cache the current question per region and cycle in memory (e.g., Redis). Instead of querying the database every time a user needs a question, the system can check the cache first.
- Using Loadbalancers to distribute requests
- Using a message queue to handle requests asynchronously

## Pros of the approach
- Easy to implement
- Flexible to change the cycle duration and question assignment logic based on API calls
- By leveraging caching, we minimize frequent database hits.
- Users always get region-specific questions based on the cycle, ensuring a streamlined experience.

## Cons of the approach
- Overhead of maintaining another layer of caching
- Complexity of the codebase increases due to additional layers of caching and database queries. Technical know-how of the architecture is then required.
