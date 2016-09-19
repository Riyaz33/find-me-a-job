## find-me-a-job

> Find the perfect company _for you_.

Analyzes your resume and prepares a list of relevant companies based on your skillset. Company data is scraped via [StackShare](http://stackshare.io).

Built in under 24 hours during Hack the North 2016 at the University of Waterloo.

- [Devpost](http://devpost.com/software/find-a-tech-job)
- [Live](http://45.79.161.187/)

### Installation

- Prerequisites:
  
  + Python __2.7__ (some deps don't run on Python 3+)
  + MongoDB

- Clone repository.

  ```sh
  $ git clone https://github.com/kshvmdn/find-me-a-job.git && cd $_
  ```

- Install dependencies.

  ```sh
  $ pip install -r requirements.txt
  ```

### Usage

- You're going to want to populate the database before using the application (otherwise you'll have nothing to work with). You can do this by running the scraper. See [`scraper/endpoints.py`](scraper/endpoints.py) for the list of all endpoints (edit this as you will).

  ```sh
  python ./scraper/__init__.py
  ```

- Start the application, it'll be running at the provided host/port ([`http://localhost:3000`](http://localhost:3000) by default).

  ```sh
  $ HOST=<host> PORT=<port> DEBUG=<debug> ./app.py
  ```
