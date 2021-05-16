## Digital - Senior Engineer test

Deliverables:

* A way to import the contents of DSRs to the DB.
   ```bash
   http://localhost:8000/ingest/
   ```
* Complete the API according to the OpenAPI specification.
   ```bash
   http://localhost:8000/dsrs/
   ```
   ```bash
   http://localhost:8000/dsrs/{id}
   ```
   ```bash
   http://localhost:8000/resources/percentile/{number}
   ```

* A form in the admin page to delete DSRs and it's contents.
   ```bash
   http://localhost:8000/admin/dsrs/dsr/
   ```
* Tests for each api endpoint, using any preferred testing framework.
   ```bash
   python manage.py test
   ```
* Dockerfile
  ```bash
   docker build -t digital:v0 .
   docker run -it -p 8001:8000 digital:v0
   http://localhost:8001/
   ```

Extra questions:

* DSPs report DSRs containing hundreds of millions of usages. If you were to
  deploy this solution to production, would you do any change in the database
  or process, in order to import the usages? Which ones?

Answer:


1. postgreSQL (Database)

    Choose the best performance DB engine.The response speed of an endpoint
    depends on how fast your database query is processed. proven architecture,
    reliability,data integrity and performance.

    Deploy on fast storage and CPU cores

2. Indexing (Use standard DB optimization techniques)

    Create all the necessary Indexes for all queries.
    Retrieve individual objects using a unique, indexed column like id,
    because id is indexed by the database and is guaranteed to be unique.

    Too many indexes are bad — delete unused or redundant ones.
    Each created index might increase search metrics on that column (SELECT)
    but will reduce write speeds (INSERT, UPDATE).

3. Caching (Use standard DB optimization techniques)
    Understand cached attributes. Caching is one strategy that can help to improve
    application’s read performance. Caching involves temporarily storing data
    that has already been requested in memory, allowing you to access it much
    more quickly later on.

4. Bulk query (Use standard DB optimization techniques)

    Use bulk queries to efficiently query large data sets and reduce the number of
    database requests. Django ORM can perform several inserts or update operations
    in a single SQL query. Create, Update, Insert, Remove using bulk.

5. Essential info (Use standard DB optimization techniques)

    Retrieve everything at once if you know you will need it
    Don’t retrieve things you don’t need.
    Reduce the size by excluding fields that are not used by the app client.

    Use keys like JOIN, WHERE etc in SQL and functions like only(), defer() etc in
    Django ORM QuerySet function to return to essential information from the API.

6. Deactivate Unused apps and middleware

    By default, the framework has several applications activated that can be useless,
    especially if you use Django as a REST API. reduce processing speeds.
    The fewer middleware you have declared, the faster each request
    will be processed.


8. Persistant connection

    Maintain persistent connections to the database if the application needs to
    process a large number of requests. Django closes the connection by default
    at the end of each request and persistent connections avoid overloading the
    database for each request.

9. Remove unnecessary queries.

    check the number of queries you're running using django debug toolbar and
    remove unnecessary queries.

10. sharding

    django can handle sharding,postgres offers an in-db way to do this.

    Pros:

    speed up query response times.
    When you submit a query on a database that hasn’t been sharded, it may have
    to search every row in the table you’re querying before it can find the
    result set. By sharding, queries have to go over fewer rows and their
    result sets are returned much more quickly.

    Sharding make an application more reliable by mitigating the impact of outages.
    With a sharded database, though, an outage is likely to affect only a single shard.
    Even though this might make some parts of the application or website unavailable
    to some users, the overall impact would still be less than if the entire database crashed.

    cons

    Sharding can be a great solution for those looking to scale their database horizontally.
    However, it also adds a great deal of complexity and creates more potential failure points.

    Sharding may be necessary for some, but the time and resources needed to create
    and maintain a sharded architecture could outweigh the benefits for others.
