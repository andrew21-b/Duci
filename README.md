
# Visual Change Detection MVP

This is my solution, it consists of a PostgreSQL database and a FastAPI backend, using Alembic for database migrations, SQLAlchemy for models, and Pydantic for data validation. I am using Poetry as my package manager and for virtual environment management.

For the frontend, I am using React with Vite and Tailwind CSS for styling.

## Setup Instructions

The setup assumes some prerequisites are met before running both apps.
The database needs to be initialised on your machine. PostgreSQL must be installed, and the database `duku` must exist.

### Prerequisites

1. Clone the repository:
    ```powershell
    git pull https://github.com/andrew21-b/Duci.git
    ```

2. Change to the repository directory:
    ```powershell
    cd Duci
    ```

3. Change to the API directory:
    ```powershell
    cd api
    ```

4. Activate the virtual environment:
    ```powershell
    poetry env activate
    ```

5. Install dependencies:
    ```powershell
    poetry install
    ```

### Install PostgreSQL

1. Go to [PostgreSQL](https://www.postgresql.org/download/) and download it for your operating system.
    - Follow the setup wizard.

2. Create the database:
    ```powershell
    psql -h localhost -U postgres -d duku
    ```
    - Follow the terminal instructions; you will need the password you set during PostgreSQL installation.

3. Add tables to the database:
    ```powershell
    alembic upgrade head
    ```

4. Create a `.env` file in `api\src\api`:
    - In the `.env` file, add this line:
      ```
      DATABASE_PASSWORD=<your_database_password>
      ```
      Replace `<your_database_password>` with the password you set for the user during PostgreSQL setup.

### Starting the API

To run the API, execute this command in the `api` folder:
```powershell
poetry run fastapi dev src\api\main.py
```

### Starting the React App

Open a new terminal.

1. Change to the `frontend` directory:
    ```powershell
    cd frontend
    ```

2. Run the app:
    ```powershell
    npm run dev
    ```

## Assumptions made

The main assumption is that users will upload screenshots of the app or website with the same dimensions. The comparison expects the images to be the same size. If not, as you can see with `test_images`, any difference in size or spacing will be counted as a difference.

## What I'd improve in the future

There are many things I would improve if I had more time, from the system architecture to the build systems. Here are some:

- Use temporary files or cloud storage for image uploads.
  - Currently, images are written to disk for simplicity. Storing images elsewhere would make the system more secure and scalable, and reduce memory and storage usage.
- Add tests.
  - I would add unit and endpoint tests for the backend, and integration tests for the frontend.
- Add response models.
  - This would improve the OpenAPI documentation and make the API more maintainable.
- Add error handling for the frontend.
  - Currently, errors are logged to the console or ignored. I would add popups or cards to inform users of errors or invalid input.
- Spend more time on accessibility.
  - I would ensure components are accessible, with proper descriptions and alt text, and that the design is consistent across different screen sizes.
- Add a theme.
  - A consistent theme would improve the design and allow for light/dark mode, enhancing accessibility.

## Challenges Faced

The main challenge was ensuring the frontend could convert API responses into the correct format. Since images are saved in the API directory, converting them into links usable by React took some time.

Another challenge was implementing the image comparison change boxes. As I am still learning OpenCV, finding the right method to detect changes and draw boxes took time to complete and test.
