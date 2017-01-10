# Revenge of the Nerds: examining student behavior on RateMyProfessors.com
Intended for an audience of mixed technical experience. Programmers will be condescended to.

## Background
Aside from internal, university-administered surveys with private data :confused:, RateMyProfessors is the primary resource for helping students choose their professors. It's the closest thing to a randomized survey we can get, with the slight caveat that it's not random. I wanted to understand the behavior of students who are so inspired that they take the time to fill out RMP's survey. I sure haven't done it. How do I know whether to trust the reviews?

## Collecting the data
This project began as an excuse to learn [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), a tool for Python that lets you scrape data off websites and store it in a way that makes it easier to process and analyze. It can save hours of time when you have no other good ways of collecting the data. I decided to extract reviews for all the professors in the Computer Science and Mathematics departments at Northeastern.

Here's how a review looks on RMP:

![](/rmppictures/olin.PNG "0 people did not find this useful")

BeautifulSoup made it easy to extract the overall rating, difficulty rating and the comments. It was going really well until I ran into BeautifulSoup's worst nightmare:

![](/rmppictures/bs4worstnightmare.PNG ""Don't Even Bother"")

When you click on a professor, RMP only shows you the first twenty reviews in case your connection is slow. This prevents your friend with dialup from slowing down their parents' Netflix to load hundreds of comments detailing how Noam Chomsky has "really changed." Good for your friend's parents, bad for me.

The problem is that at the moment that you click Load More, you're actually asking RMP for the next set of twenty reviews. That request goes to their computers and comes back through their website so you see it formatted all nice and readable. Ironically, the process that makes it nice and readable to humans also turns it into total garbage for computers. Hence why I needed BeautifulSoup to do my work for me. Unfortunately, BeautifulSoup can't simulate this mouse click.

There is a way to simulate it, but while working that out I found something better:

![](/rmppictures/thankfully.PNG "deus ex machina")

This is what I never knew I needed. This is the machete in the corn maze. When I visit the **Request URL** I get the review data in its raw form. I don't need BeautifulSoup anymore because the data comes back in JSON, a format which is very easy for Python to process. The **tid=95525** tells RMP's server which professor I am searching for, and **page=2** tells it which block of twenty reviews I want. Automating the data collection from this point was much, much easier (see [getprofessordata.py](/getprofessordata.py) for details).

## Asking too much
The discovery simplified data collection, but I had to be conscious of getting **rate-limited**. This is when [Il Mondo Pizzeria](http://www.ilmondopizza.com/index.php) tells you they can't make 500 pies for your meeting this afternoon, and *just because you asked*, they won't even sell you a slice until tomorrow. Jerks. You can either wait or go somewhere else. Joke's on them because [Penguin](http://www.thepenguinpizza.com) is better anyway.

Unfortunately there is no Penguin to my RMP. Because I automated the process of collecting data for a long list of professors, my requests were going in very fast and it was entirely possible that at a certain point RMP would tell me no more. If that happened, I'd have to an hour or a day until I could resume. Not a huge problem but it would have been a hassle. Anyway, moot point because it didn't happen.

## Analyzing the data
Now that I had full data (2620 reviews for 240 professors) for the Computer Science and Math departments, time to test some assumptions.

### Assumption 1: Difficulty ratings follow a normal distribution (bell curve)
I'd expect most professors to be of average difficulty, with rarest ratings being 1s (super easy) and 5s (super hard). The data seems to show that this is correct.

![](/rmppictures/difficultycounts.png "")

### Assumption 2: Overall ratings follow a normal distribution (bell curve)
Lol.

![](/rmppictures/overallcounts.png "")

This tells me one of two things: that students tend to fill out the survey when they loved or hated their professor, or that nine rating choices (1.0 through 5.0 by .5s) is too many.

If it's the first one, this reveals a self-selection bias that we should be aware of when we look at the results of any survey. Knowing this makes it a little harder to trust overwhelmingly positive or negative reviews--I'd expect to see fewer counterweights to those students.

It is also possible that nine rating choices is too many. What separates a 2.0 professor from a 1.5? Good hair? The lack of clear definitions of what a rating signifies coupled with self-selection bias can explain the distribution we see.

### Assumption 3: Easier professors get higher ratings, harder professors get lower ones
I think if the grading is lenient, students might be in a better mood when giving a review, and vice versa.

![](/rmppictures/ratingpairs.png "")

This seems to be a tendency. It could be explained by students wanting to be nicer to professors who give good grades, or it could happen the other way--professors who explain things poorly end up running a more difficult class just because students have a harder time learning the material.

### Assumption 4: Difficulty rating is a good proxy for Grade Received
In the real world, you have to deal with incomplete data. All the time. To me, the grade a student received from a professor is more telling than that student's perceived difficulty of the professor, since I can't put my "Difficulty Point Average" on my resume. Since Grade Received is optional, most students don't fill it out. I want to know how well reported difficulty correlates with Grade Received for those students who filled it out.

![](/rmppictures/gradevsdifficulty.png "")

Here r<sup>2</sup> is called the *coefficient of determination* and we can interpret it to mean "14% of the change in difficulty rating is caused by the linear relationship between grade received and difficulty." The line on the chart, called the regression line or line of best fit, indicates that linear relationship. As grades improve, difficulty decreases. 14% is fairly low, so there is a weak correlation between grade and difficulty. However, this subset of reviews is only around 15% of the total reviews submitted, so to get a more telling result I would need to collect a larger set of data from more departments or universities.

### Visualizing Northeastern's professors

![](/rmppictures/professorscatter.png "")

Sometimes visualizing data can help us understand it better. Here it seems like professors with more reviews tend to get push toward the middle, as we would expect. You can also see two groupings of professors; if we draw a diagonal line from the bottom-left to the top-right we can separate the groups into "take this professor" and "avoid this professor."
