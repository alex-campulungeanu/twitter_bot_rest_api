
# Social Media API

Simple API for social media platform(currently only twitter is supported)

  

## Installation

1. create and configure .env.production / .env.development files (cp .env.example)

2. configure database:

1. flask db init

2. flask db migrate -m initial

3. flask db upgrade

4. flask configure-db (all flask commands ar listed with : (venv) → <PROJECT_NAME>› flask)

  

## Deploy changes to production from local machine (if DB changes has been made)

1. change .flaskenv to production

2. changex in /migrations folder: folder versions_prod to version

3. check revisions to be added on production db with: <PROJECT_NAME>› flask db ...

4. flask db migrate -m <message>

5. flask db upgrade

6. flask configure-db (commands are located in <PROJECT_ROOT>\app\commands.py)

  

## Commands

  
  

## Flask Migrate changes

- \migrations\env.py

 . 
    
    schema = current_app.config['DB_SCHEMA']

    def include_object(object, name, type_, reflected, compare_to):
        if type_ == "table" and object.schema != schema:
            return False
        else:
            return True

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=schema,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )
