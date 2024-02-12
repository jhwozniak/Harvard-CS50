# THE FAMILY CLINIC
## CS50
This was my final project to conlcude the Harvard's CS50 Introduction to Computer Science course.
The course consisted of 10 weeks of intensive training in CS basics such as algorithms, data structures and memory managament, followed by
programming in C, Python, SQL and web development (Flask). Each week was concluded with a lab and problem set, requiring students to
solve some programming problems. This is a final project, which is supposed to conclude the whole CS50 course and to present my
application of knowledge gained during this course.

## The project features
The Family Clinic is a web app facilitating work of an imigainary health clinic. It woks in patients' mode and doctors' mode.

As a patient, you can:
+ register as a new user
+ change your password
+ search available visits by doctor's specialisation
+ book a visit
+ cancel a visit
+ examine details of completed visits, including diagnosis made by your doctor and a proposed treatment

As a doctor, you can:
+ register as a new user
+ change your password
+ see pending visits booked with you by your patients
+ after finishing the real examination of patient, you are welcome to enter diagnosis and proposed treatment

## Techology used
+ Python as a high-level programming language
+ Flask and Jinja as web frameworks for Python
+ SQLite3 as a database engine
+ HTML, CSS, JavaScript, Bootstrap for front-end interface

## Explainig the project in detail
### Accessing the app
You can access the project in CS50 Codespace by entering the project catalogue and typing `flask run` in terminal. Then, you click on the link which will open the app in your browser. When you register as a new user, Flask will carry your `session["user_id"]` throughout the whole session. Various database calls will often refer to this session id, as a user's id in the database (whenever it you logged in a patient or as a doctor).

### App structure
The project folder contains **app.py** file, which is a main file with application's code written in Python. It contains a dozen of **@app.route** functions, which are managing the flow of the application. Any time the user follows specific route on a webiste, either by clicking on links buttons or using dropdown menus, the app calls a specific function defined below the **@app.route** decorator. The ***app.py** file is structured in such a way, that the first half of code contains the flow of commands for the "patient's mode" of the app, while the second half rules the behavior of the "doctor's mode". **Templates** folder contains more than a dozen of html pages, while **static** folder contains app's icon and css stylesheet.

### Available modes
The app runs in two modes: patient mode and doctors mode. The idea behing this was to simulate "real-world" application, which could facilitate interaction between patients and doctors in a simple general health clinic.

The patient mode is a default one when you access the homepage. You can access the "doctor's mode" by clicking on the link at the bottom of the page. The shift to "doctor's mode" will be indicated by the blue badge "doctors" in the upper-left corner. As a patient, apart from registering, changing passwords and logging in, you can search visits, book visits and cancel them. You can also monitor past visits by entering the "History" tab and see the diagnosis made by your doctor and proposed treatment.

As a doctor, you basically register and log in in order to see your pending visits. Then, ypu are expected to give input in form of diagnosis and treatment and confirm by clicking "Send" button.

### Database mechanics
All the data was saved in SQLite3 **clinic.db** database. All info about patients' and doctors' ids, names, surnames, usernames are stored in **patients** and **doctors** tables. Data is pulled from these tables any time the user logs in or changes password. New rows are added any time new user registers. The main flow of data happens among **visits**, **searched_visits** and **completed_visits** tables. For axample, new visits are added to **visits** table. Any change in status of a visit (which can be "free", ""booked" or "completed") impacts the whole three tables. **Visits** table is a core table containing all info about ids of visits, status of a visit, doctors, dates, diagnosis and treatments. The other two tables have temporary nature and their content changes dynamically. For instance, **searched_visits** is purposefully emptied any time a new patient logs in and follows the `"\search"` route.

### Front-end interface
The webiste looks and interface is managed by a dozen of html files and css stylesheet. In order to bolster the general looks and to concentrate on the back-end mechanics, we chose Bootstrap library.

## Where to see it
Video Demo:  <URL https://youtu.be/vnTr_Kie560>

## Where to get it
GitHub:
+ https://github.com/code50/118801378
+ https://github.com/me50/jhwozniak

Enjoy!

Jakub Wozniak


