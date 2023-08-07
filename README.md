# Academic Matchmaking: Find Your Academic Advisor!
by Team Jake_Yan

## 1. Purpose
### *Application Scenario*: 
This application is intended to help students choose their ideal advisors when applying for graduate school based on their research interests.

### *Target Users*: 
Students who are applying for graduate schools and looking for potential advisors whose works are related to their interested areas.

### *Objectives*:
- Let students quickly narrowdown pubications, universities and scholars in a specific academic area.

- Feasibilities of saving a list of favorite professors to explore later.

- Graphic representation to show how close the student is to their favorite professors through co-authorship.

- Allowing the students to have access to a large and centralized database without concern about the connection intricacies and can directly query the database by clicking, adding, and deleting dropdown menu items. 

- Simple, clean, and clear delivering manners in the user interface to render a straightforward menu of options for the students’ matching experiments.

## 2. Demo
Please check [this link] for a demo. 

[this link]: http://python.land

## 3. Installation
Before using this application, you need to have the academicworld database populated and running on MySQL, MongoDB and Neo4j. The following libraries are also needed:
- dash
- pandas
- mysql
- pymongo
- Neo4j
- pyvis
- plotly
- pillow

If your username, password or port number is different from the default for the databases, specify them in app.py when initializing each database class.

## 4. Usage
To run the application, first run app.py, then click on the link in the output. This should open up a webpage in your browser and display the dashboard.
Then you can interact with the dashboard by choosing keywords, adding favorite faculties, etc.

## 5. Design
The dashboard has six widgets in total.

### *The First Three Widgets: Top Publications, Universities and Faculties*
The first three tell users what are the top publications, faculties and universities most relevant to the keyword they are interested in.
The user can choose a keyword from the “Choose Keyword” dropdown menu on top of the page. 
They can also narrow down the year range using the slider bar if they don’t want all-time data.
The basic information about top publications, universities and faculties are then displayed in tables in the first, second and third widget respectively.

### *The Fourth Widget: Faculty Info on a Particular Professor*
If users want to get more information about a particular faculty they are interested in, they can choose a faculty from the dropdown menu on top of the fourth widget, 
then it will display information about the faculty such as affiliations and position/title, along with their photo.

### *The Fifth Widget: Add/Delete User’s Favorite Professors in a Table*
The fifth widget allows the users to add and delete their favorite faculties in a temperate table. Duplicated ones are not allowed. Then they can see how close they are related
to these faculties through co-authorship in the sixth widget. 

### *The Sixth Widget: A Node Graph Showing the Students’ “Distance” to their Favorite Professors*
In order to see how close the students’ current advisors are to the ones they have interest in, they need to choose their current advisor (or any faculty who can recommend them) from
the dropdown menu in the sixth widget, then it will display a graph showing how their advisor is connected to their favorite faculties through co-authorship.
If the advisor is close to one of the favorite faculties, the user might have a better chance of getting into the favorite faculty’s lab.

## 6. Implementation
The application is written in python. The backend uses respective python clients to query and update mySQL, MongoDB and Neo4j databases and the frontend uses Dash to
generate a dashboard to interact with users and display query results.

We used Dash to write the frontend of the application. There are dropdown menus and slider bars that receive user input
and callback functions that update data displayed whenever the input changes.

### *The First Three Widgets:*
They query and update the mySQL database to get top publications, faculties and universities. To speedup querying, we added indexing on the year attribute of the publication table.
The publications are first filtered by their publication year, and then their keyword-relevant citation (KRC) scores are calculated as S*C. S is the relevance score of the publication
with the keyword specified, and C is the number of citations this publication received.

The calculated KRC scores are saved in a view called publication_score along with publication id, title and year
for later use. The publications with the highest KRC are then selected from the view and displayed in a table in the first widget. We then calculate the faculty KRC by summing up the KRC of all their publications
saved in the publication_score view. Faculty KRC and their basic information are also saved in a view for later use.

Then faculties with the highest KRC are selected from the view and displayed in the third widget.
Similarly, university KRC is the sum of all its faculties’ KRCs. Top universities are displayed in the second widget. 

### *The Fourth Widget:*
It queries MongoDB and outputs a dictionary of documents from the faculty collection to get more information on a particular faculty.
It also displays the faculty’s photo if the url is available and not corrupted.

### *The Fifth Widget:*
To realize the functionality of adding and deleting favorite faculties, we created a new node label in Neo4j called fav_faculty. Whenever the user adds a new favorite faculty, the database creates
a fav_faculty node with the faculty name. Similarly, when a user deletes a favorite faculty, the fav_faculty node with matching name is deleted from the database. To avoid duplicated favorite faculties,
we added a UNIQUE constraint on fav_faculty’s “name” property. If a user tries to add a faculty that’s already been favorited, the database will simply ignore the request.

### *The Sixth Widget:*
Neo4j is also used to generate the co-authorship graph. It is a shortest path graph with paths starting from a user selected faculty and ending with faculties in the favorite list.
The paths consist of alternating faculty and publication nodes connected by the relationship “PUBLISH”. An interactive graph is built using pyvis and users can drag and highlight the nodes as well as zoom and pan.

## 7. Database Techniques
The three database techniques used are indexing, view and constraint.

### *Indexing:*
We added indexing on the year attribute in the publication table in mySQL to speed up querying publications within a year range. 

### *View:*
We also created three views in mySQL to store the KRC of all publications, faculties and universities, respectively, to avoid repeated calculations. 

### *Constraint:*
We added a UNIQUE constraint on the Neo4j database requiring that each fav_faculty node has a unique name to avoid having duplicate favorite faculties.
If the constraint is violated when adding a new favorite faculty, the application will simply ignore the request.

## 8. Contributions
### *Yan*: 
Most backend utilities, frontend of widgets 5 and 6, README. Total time spent is about 40 hours.

