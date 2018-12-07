With some redundant information from the technical writeup:

Project Structure:


Front end website: Runs on HTML, CSS, ReactJS, with additional jQuery to perform AJAX operations. Supported by a Django rest framework. Contained in the folder “FrontendReactJSDjango”. To host the frontend locally, go inside of this folder, cd into the project folder, run “python manage.py runserver”, and open 127.0.0.1:8000 in browser.

Inside of project/frontend/templates/frontend are the HTML templates with some jQuery sprinkled in for the website.

The project/migrations folder includes Django database migrations

project/src contains ReactJS components

project/static contains CSS and static image files



Web-scraping: Inside of the Crunchbase folder are 12,000 startup webpages. Inside of this folder, the Extract folder contains a file called startuplistcompiler.py . This takes a Crunchbase HTML file, and using BeautifulSoup scrapes its startup’s categories, location, external links, and description, and compiles it into a csv file.

Additionally, the LinkedIn scraper contains the files for logging into LinkedIn and retrieving data with a proxy crawler


Database: Contains scraped data from various sources on startups and investors. Data not only contains the profile of companies but also team member information, past funding information and so on. The file database.csv contains our database for startup features.


NLP: Contained in the NLP folder, for the NLP portion of our proof-of-concept, we decided to take advantage of recent advancements by Google’s TensorFlow Hub, namely through their Universal Sentence Encoder (USE). The USE is very useful in converting textual data into a numerical 512-dimensional vector and maintains semantics, meaning that the original context of the text is preserved. This encoder is used when we analyze any scraped data from the front-end—the program receives input text, encodes it, and then finds all relevant features that can be extracted from the text by calculating cosine similarity between all existing features (which can be seen in “cleaned_data.tsv”).

All the embedding data for the features is written to a text file, and to determine which features correspond greatest to the ones that are mentioned from the scraped input, we use the cosine similarity metric. These cosine similarities are then stored as objects in a max heap, which makes the retrieval of the feature with highest similarity run in constant time. To determine the confidence with which each feature is extracted, we make use of a modified logistic exponential, sandwiching any value into its adjusted position between 0 and 1.

Matching algorithm: Contained in 1-nearest-neighbor, uses 1-nearest-neighbor unsupervised learning, taking features from startups and investors and matches an investor to a list of ranked startups off of the basis of natural language features.


How it comes together: Data is first retrieved from Crunchbase and LinkedIn directly. From there, the data is cleaned for relevant information with BeautifulSoup and stored in a database csv (Ideally, we would have moved this CSV into our Django database as a fixture for our front-end). After the data has been cleaned for features, the description natural language features are structured for our NLP framework by our NLP cleaner, and our NLP feature extractor interpolates additional information from the natural text.

After all of these features have been aggregated, we run our 1-nearest-neighbor model to determine the cluster of startups most accurately matching any new input of data from the frontend website input for in index.html . After this has been submitted, the results of the model are displayed on the same page through AJAX operations. While our body of work doesn’t fully our Django database with our backend model since we were prioritizing our most important features for our time-constrained demo, we could do so simply by injecting our csv database as fixtures through our Django REST framework our frontend is built on.
