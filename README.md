# The Anatomy of The Simpsons: What Episodes Earn Good IMDb Ratings?
## Project 2 (Metis bootcamp)

# Description
For my first solo data science project, I sought to map in some way the instructional elements of an episode of *The Simpsons*. To narrow my scope I chose to use IMDb ratings as my metric and target variable, for these reasons:
- Accessibility: More than 350,000 ratings of *Simpsons* episodes are currently published on IMDb
- Time constraints: Related to the above and surely always a guiding force but noting here anyway

I collected data mostly through scraping (see "Tools Used" below), cleaned and combed through it, and used the processed dataset to build a linear regression model with IMDb rating as target. Early results (measured mostly by R2 scores) were underwhelming, with an R2 score around .5 and dozens much lower. With scaling and some inefficient feature engineering I eventually found my way to a simple linear regression model returning R2 scores (cross-validated) around .75.

# Features and Target Variables
- My **target variable** was IMDb rating
- My final **features** were:

# Data Used
I used data scraped and sourced from:
- IMDb
- TVDB
- Wikipedia
- Wikisimpsons
- Kaggle

Special thanks goes to Pierre Megret's ["Dialogue Lines of The Simpsons"](https://www.kaggle.com/pierremegret/dialogue-lines-of-the-simpsons) project and dataset on Kaggle.

# Tools Used
Additionally, I made use of the following Python modules in the course of this project:
- Scikit-learn
- Numpy
- Pandas
- BeautifulSoup
- Matplotlip
- Seaborn

# Possible impacts
I take away so far a belief that the early episodes of *The Simpsons*, and specifically those in season 2-8, are significantly more popular than episodes in the 20+ seasons that followed them. This is no surpise but nonetheless supported by the data. Diving a little deeper, I am struck that despite the intensity of this influence the relationship between season number/year and IMDb rating is not simply linear. It is right-skewed, bubbling up in score in the key early seasons from whose gravity my model could not escape. Interactions with my "Season score" feature powered another handful into relevance. I don't quite know my way around a time series yet and got to this idea a little late, so for now I can only say that I am intrigued by what might turn up with further deconstruction of time's influence.

Additionally, I saw that the pool of IMDb raters I made data of skews heavily male, noted in both the disparity in IMDb ratings contributed and most interestingly in the correlation (.41) between the *ratio* of male-contributed ratings/female-contributed ratings and an episode's overarching IMDb rating. That males contributed so many more ratings to the examined episodes is surely built into this relationship, but in the context of a show that appealed to Gen X men at its peak (in terms of IMDb rating here and also TV viewership), the male/female split is an area I'd like to push into more. The generational split, seen in the lower contributions of <18 users, is also of interest.

Other takeaways include the opaque and less-modelable nature of TV writing and production in this context, which frankly I'm not so sure is a bad thing (at least given how surface-level my exploration was). The collision of art and data is explosive and frightening. I come to data science from writing and for now I plan to approach with delicate steps.

It must also be noted that I am outright stunned that Milhouse's contributions to an episode, primarily measured as a percentage of an episode's spoken word count, didn't make my final model. "Homer at the Bat" meanwhile is a top 5 episode.

- Area of future focus: Time/"nostalgia" as an instrument of IMDb raters who are male, Gen Xers in middle age, IMDb's dominant userbase, and consumers in an industry many folds removed from the one from which they saw *The Simpsons* emerge
- Area of future focus: A more concentrated look at changes in the industry and content access, plus in-house stuff involving *Simpsons* cast and crew, alongside ratings changes
- Area of future focus: Plot/script themes like politics and warpings in character personality, both examined with language processing tools
- Area of future focus: IMDb's rating system, which includes a "weighted" mean formula supposedly designed to battle troll activity
