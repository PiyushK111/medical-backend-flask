Issues and Resolutions

This document outlines the key issues encountered during development of the Medical Backend Flask application, along with the corresponding resolutions applied.

🔴 Critical Issues (System-Blocking)
1. Flask App Crashing Due to Name Shadowing

Issue
The Flask application instance was named app, which conflicted with the Python package named app.

Impact

Flask failed to initialize routes

Error encountered:

AttributeError: module 'app' has no attribute 'route'


API container exited immediately

Resolution

Renamed the Flask instance from app to flask_app

Eliminated namespace collision

Application routes initialized correctly

2. API Container Exiting Immediately on Startup

Issue
Unhandled exceptions during application startup caused the container to terminate.

Impact

Backend service unavailable

Database initialization never completed

Resolution

Inspected logs using:

podman logs medical-api


Fixed startup exceptions before server initialization

Container stabilized and remained running

3. Database Tables Not Created Using db.create_all()

Issue
db.create_all() was executed during container startup before PostgreSQL was ready.

Impact

Tables were not created

No visible error logs

Inconsistent schema state

Resolution

Removed db.create_all() from startup flow

Introduced Flask-Migrate (Alembic) for schema management

Database schema creation became deterministic and version-controlled

4. Flask CLI Not Detecting Application Factory

Issue
Flask CLI could not locate the application factory.

Impact

Migration commands unavailable

Error encountered:

Error: No such command 'db'


Resolution

Explicitly set:

FLASK_APP=run:create_app


Flask CLI successfully discovered the app

Migration commands became available

5. JWT Token Generation Failure

Issue
JWT token generation failed due to missing SECRET_KEY.

Impact

Login succeeded but token generation failed

Error:

Expected a string value


Resolution

Added SECRET_KEY to Flask configuration

Ensured PyJWT received a valid string secret

Authentication flow completed successfully

6. SQLAlchemy Mapper Initialization Error

Issue
ORM mapping failed due to missing reverse relationship.

Impact

Application crashed during import phase

Error:

Mapper 'User(users)' has no property 'availabilities'


Resolution

Added missing back_populates relationship to User model

Used string-based relationship references to avoid circular imports

ORM mappings initialized successfully

🟠 High-Impact Issues (Severe Development Blockers)
7. Flask-Migrate Not Installed or Wired

Issue
Flask-Migrate was missing or not registered.

Impact

Migration commands unavailable

Resolution

Installed Flask-Migrate inside container

Registered it within the application factory

8. Running Flask CLI on Host Instead of Container

Issue
Flask CLI commands were executed on Windows host.

Impact

Command not recognized:

'flask' is not recognized as an internal or external command


Resolution

Executed all Flask CLI commands inside the medical-api container using:

podman exec -it medical-api flask ...

9. Migration Files Not Visible on Host

Issue
Migration files were created only inside container filesystem.

Impact

migrations/ folder invisible in VS Code

Risk of losing migration history

Resolution

Mounted project directory as a volume in Podman Compose

Ensured filesystem synchronization between host and container

10. PostgreSQL Data Loss on Restart

Issue
Database data was lost after container restart.

Impact

All users and records deleted

Resolution

Added named volume for /var/lib/postgresql/data

Avoided destructive commands such as:

podman-compose down -v


Data persisted across restarts

🟡 Medium-Impact Issues (Workflow / Conceptual)
11. Host vs Container Context Confusion

Issue
Attempted to run Podman commands inside containers.

Impact

Error:

podman: not found


Resolution

Clearly separated host-level and container-level responsibilities

12. Misunderstanding Schema Creation Timing

Issue
Assumed database schema would be created on API requests.

Impact

Confusion about missing tables

Resolution

Learned schema creation is startup/migration-based

Adopted migration-driven schema management

13. PostgreSQL Pager Confusion

Issue
Pager output (less) was mistaken for a frozen terminal.

Impact

Difficulty exiting query output

Resolution

Used q to exit pager

Disabled pager when needed using:

\pset pager off

🟢 Low-Impact Issues (UX / Tooling)
14. Swagger UI Added Before Backend Stabilization

Issue
Swagger was introduced too early.

Impact

Required reconfiguration after backend fixes

Resolution

Deferred Swagger integration until core APIs were stable

15. Missing .flaskenv Configuration

Issue
Environment variables had to be set manually each time.

Impact

Reduced CLI ergonomics

Resolution

Added explicit environment configuration

16. Lack of Structured Logging Initially

Issue
Errors were difficult to diagnose.

Impact

Increased debugging time

Resolution

Added structured logging at application startup

Improved observability via Podman logs

✅ Final Outcome

After resolving these issues:

Application starts reliably

Database schema is version-controlled and persistent

Authentication and RBAC function correctly

ORM mappings are stable

Swagger documentation is accessible

System is production-ready and extensible