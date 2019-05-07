A simple Markov Babbler rehashing the AWS Blog from my [Vienna](https://www.vienna-rss.com/) feed.

You'll need [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and
Python 3.6+ installed. It's usually cleanest to do this in a virtual environment:

```
% virtualenv venv
% source venv/bin/activate
(venv)% pip install bs4
(venv)% python ./awsbabbler.py --parse
(venv)% python ./awsbabbler.py --babble
```

The parse step ingests the blog posts and creates a `chain.pickle` file, containing the word chain.
Babble ingests the `chain.pickle` and randomly selects 100 words from the chain.

