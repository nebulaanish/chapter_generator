## Get started : Setup Locally
1. Clone repository. <br>
    ```$ git clone <link-to-repository>```
2. Create vitural environment inside the backend folder. <br>
    ```$ python -m venv .venv```
3. Activate the virtual environment 
    - On Linux/Mac: ```$ source .venv/bin/activate```
    - On Windows: ```$ venv\Scripts\activate```
4. Install required dependencies. <br>
    ```$ pip install -r requirements.txt```
5. Create `.env` at same level as `manage.py`.
6. Add the required credentials.
7. Run server and access the apis. <br>
    `$ python manage.py runserver`