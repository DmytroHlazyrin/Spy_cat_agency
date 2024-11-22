# Spy Cat Agency (SCA) - Management System

## Project Overview

The **Spy Cat Agency (SCA)** management system is designed to streamline the operations of an espionage organization by managing spy cats, missions, and targets. The system allows SCA to:
- Register and manage spy cats.
- Create, update, and assign missions to available cats.
- Track and manage targets for each mission.
- Update and finalize mission statuses and notes.

This system leverages FastAPI for building a RESTful API with asynchronous support, SQLAlchemy for database interaction, and PostgreSQL as the database.

## Features

- **Spy Cats**:
    - Register new spy cats with details (Name, Experience, Breed, Salary).
    - Remove and update spy cat information.
    - View spy cat list and single spy cat details.
    
- **Missions and Targets**:
    - Create missions with targets.
    - Assign available spy cats to missions.
    - Update target status, notes, and mark them as complete.
    - Missions are marked as completed when all targets are finished.

- **Validation**:
    - Cat breeds are validated using [TheCatAPI](https://api.thecatapi.com/v1/breeds).

## Requirements

- Python 3.10+
- PostgreSQL

## Installation

### Step 1: Clone the repository

```shell
git clone https://github.com/DmytroHlazyrin/Spy_cat_agency.git
cd Spy_cat_agency
```

### Step 2: Create a virtual environment and install dependencies

```shell
python -m venv venv
source venv/bin/activate  # For Unix-based systems
# or
venv\Scripts\activate  # For Windows

pip install -r requirements.txt
```

### Step 3: Configure the database
Set up PostgreSQL and create a database. Configure your DATABASE_URL in the .env file:
```text
DATABASE_URL=postgresql+asyncpg://user:password@localhost/spycats_db
```

### Step 4: Apply migrations
Run Alembic migrations to set up the database schema:
```shell
alembic upgrade head
```

### Step 5: Start the FastAPI app
To run the development server:
```shell
uvicorn app.main:app --reload
```
The application will be available at http://127.0.0.1:8000.

### API Endpoints
Docs for API will be accessible at http://127.0.0.1:8000/docs.

The following API routes are available:

* Spy Cats
    * POST /cat/ - Create a new spy cat
    * GET /cats/ - Get a list of all spy cats
    * GET /cat/{cat_id} - Get details of a specific spy cat
    * PUT /cat/{cat_id} - Update spy cat information
    * DELETE /cat/{cat_id} - Delete a spy cat
* Missions
    * POST /mission/ - Create a new mission with targets
    * GET /missions/ - Get a list of all missions
    * GET /mission/{mission_id} - Get details of a specific mission
    * POST /mission/{mission_id}/assign_cat - Assign cat to existing mission
    * POST /mission/{mission_id}/mark_as_completed - Mark mission as completed
    * POST /mission/{mission_id}/add_target - Add target to mission
    * DELETE /mission/{mission_id} - Delete a mission
* Targets
    * PUT /mission/{mission_id}/target/{target_id} - Update a target's information (e.g., notes, completion status)

# Future Enhancements
1. #### Docker Integration
In the future, we plan to containerize the application using Docker. This will simplify the deployment process and make it easier to run the application in different environments (development, staging, production).

Docker image for the FastAPI app.
PostgreSQL container.
Redis container for task queuing.
2. #### Redis Integration with Celery
For background task processing (e.g., for scheduling missions or sending notifications), we plan to integrate Celery with Redis as the message broker. This will allow us to offload time-consuming tasks from the main application.

Example Future Tasks:
Scheduled mission reminders.
Mission report generation.
Cat availability tracking and notifications.
3. #### Advanced User Roles and Authentication
As the system grows, we plan to introduce an authentication and authorization layer:

Admin users for managing cats, missions, and targets.
Regular users with limited permissions to view missions and targets.
We will use OAuth2 and JWT tokens for secure user management.

4. #### Enhanced Validation
We will continue to improve data validation:

Extend validation for the cat breed using the external API to check more attributes (e.g., character traits).
Implement more robust input validation for mission targets, ensuring that incorrect data is rejected early.
5. #### API Rate Limiting
To prevent abuse of the API and ensure smooth performance, we may implement rate limiting using tools like FastAPI Limiter or an external service.
6. #### Tests 

### Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request. All contributions are welcome!