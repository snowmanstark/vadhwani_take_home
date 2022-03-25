## Prequisites
1. Docker

## Deployment steps
1. Copy GCP translation key to the root folder and rename the file to `service-account.json`
2. Create `.env` file similar to `sample.env` file and change the username and password values to your preference
4. Ensure that port `8080` is not being used by any other application
3. Run the following commands
    ```
    $ docker-compose build
    $ docker-compose up -d
    ```
4. Use the app at http://localhost:8080
5. Destroy the containers 
    ```
    $ docker-compose down
    ```

## Assumptions
1. `phone_number` column exists and is unique for all users.


## Features 
1. Cache translations so that we don't call API repeatedly
2. The CSV file can contain even more columns than the `sample.csv` sent over email
3. Trendy UI