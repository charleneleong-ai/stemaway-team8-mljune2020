# Stemaway NLP ML Project - Building a forum classifier for Discourse forum posts with BERT


##  **The High Level Overview:**

1. Webscrape data from at least 3 [public Discourse forums](https://www.discoursehub.com/communities/) to get text from posts and their
associated metadata. 
2. Use a transformer based neural architecture (BERT) as a feature extractor to
create a sequence level embedding for each post.
3. Use similarity scores on the
embeddings to determine topic similarity for any given set of posts using dimensionality reduction techniques.
4. Build a forum classifier to predict the forum for any given post. 

Extension - 
- Build a recommendation engine to recommend similar posts for any given post.
- Use clustering with nearest neighbour search engine to explore alternative means to classify which forum a given post came from and recommend posts. 


### Requirements for running locally
- [Anaconda](https://docs.anaconda.com/anaconda/install/)

    ```bash
      $ conda env create -f environment.yml
      $ conda activate nlp-webscraper-bert
    ```



  
