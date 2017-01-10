# Revenge of the Nerds: examining student behavior on RateMyProfessors.com
Intended for an audience of mixed technical experience. Programmers will be condescended to.

## Background
Aside from internal, university-administered surveys with private data :confused:, RateMyProfessors is the primary resource for helping students choose their professors. It's the closest thing to a randomized survey we can get, with the slight caveat that it's not random. I wanted to understand the behavior of students who are so inspired that they take the time to fill out RMP's survey. I sure haven't done it. How do I know whether to trust the reviews?

## Collecting the data
This project began as an excuse to learn ![BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), a tool for Python that lets you scrape data off websites and store it in a way that makes it easier to process and analyze. It can save hours of time when you have no other good ways of collecting the data.

Here's how a review looks on RMP:

![](/rmppictures/olin.PNG "0 people did not find this useful")

BeautifulSoup made it easy to extract the overall rating, difficulty rating and the comments. It was going really well until I ran into BeautifulSoup's worst nightmare:

![](/rmppictures/bs4worstnightmare.PNG ""Don't Even Bother"")

When you click on a professor, RMP only shows you the first twenty reviews in case your connection is slow. This prevents your friend with dialup from slowing down their parents' Netflix to load hundreds of comments detailing how Noam Chomsky has "really changed." Good for your friend, bad for me.

The problem is that at the moment that you click Load More, you're actually asking RMP for the next set of twenty reviews. That request goes to their computers and comes back through their website so you see it formatted all nice and readable. Ironically, the process that makes it nice and readable to humans also turns it into total garbage for computers. Hence why I needed BeautifulSoup to do my work for me. Unfortunately, BeautifulSoup can't simulate this mouse click.

There is a way to simulate it, but while working that out I found something better:

![](/rmppictures/thankfully.PNG "deus ex machina")

This is what I never knew I needed. This is the machete in the corn maze. When I visit the **Request URL** I get the review data in its raw form. I don't need BeautifulSoup anymore because the data comes back in JSON, a format which is very easy for Python to read. The **tid=95525** tells RMP's server which professor I am searching for, and **page=2** tells it which block of twenty reviews I want. Automating the data collection from this point was much, much easier (see ![getprofessordata.py](/getprofessordata.py) for details).

## Asking too much

This discovery made data collection easier, but I had to be conscious of getting **rate-limited**. This is when ![Il Mondo](http://www.ilmondopizza.com/index.php) tells you they can't make 500 pizzas for your meeting this afternoon and, *just because you asked*, they won't even sell you a slice until tomorrow. Jerks. So you have to either wait or go somewhere else. Joke's on them because ![Penguin Pizza](http://www.thepenguinpizza.com) is better anyway.

Unfortunately there is no Penguin to my RMP. Because I automated the process of collecting data for a long list of professors, my requests were going in very fast and it was entirely possible that at a certain point RMP would tell me no more. If that happened, I'd have to an hour or a day until I could resume. Not a huge problem but it would have been a hassle. Anyway, moot point because it didn't happen.

## Analyzing the data
coming soon!
