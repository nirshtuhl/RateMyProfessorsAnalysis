from math import ceil
import requests
import json

# let's get some professor names and IDs
# department name (e.g. 'Computer+Science') comes from this query
# http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&callback=noCB&q=*:*+AND+schoolid_s:{SCHOOLID}+AND+teacherdepartment_s:%22{DEPARTMENT}%22&defType=edismax&qf=teacherfirstname_t^2000+teacherlastname_t^2000+teacherfullname_t^2000+autosuggest&bf=pow(total_number_of_ratings_i,2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=200&start=1&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq=
def getProfessors(department, schoolID):
    with requests.Session() as session:
        response = session.get("http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&callback=noCB&q=*:*+AND+schoolid_s:{0}+AND+teacherdepartment_s:%22{1}%22&defType=edismax&qf=teacherfirstname_t^2000+teacherlastname_t^2000+teacherfullname_t^2000+autosuggest&bf=pow(total_number_of_ratings_i,2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=200&start=1&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq=".format(schoolID, department))
        # DIRTY HACK - there is some extra text that I need to strip
        data = response.text[5:len(response.text)-2]
        data = json.loads(data)
        data = data['response']['docs']
        # END DIRTY HACK

        professors = []
        for professor in data:
            # only get professors with reviews
            if professor['total_number_of_ratings_i'] > 0:
                fullName = professor['teacherfirstname_t'] + professor['teacherlastname_t']
                professorID = professor['pk_id']
                professors.append((professorID, fullName))
        return professors

# the site paginates reviews (20 per page)
# XHR request to http://www.ratemyprofessors.com/paginate/professors/ratings?tid={PROFESSORID}&page={PAGE}
# matthias is 95525
def getReviewsForProfessors(professors, department):
    for professor in professors:
        with requests.Session() as session:
            response = session.get("http://www.ratemyprofessors.com/paginate/professors/ratings?tid={0}&page=1".format(professor[0]))
            data = response.json()
            reviews = data.get('ratings')
            for review in reviews:
                review['professorID'] = professor[0]
                review['name'] = professor[1]
                review['department'] = department
            with open('RMPData.json', 'r') as outfile:
                savedReviews = json.load(outfile)
            with open('RMPData.json', 'w') as outfile:
                savedReviews += (reviews)
                json.dump(savedReviews, outfile, indent=4, sort_keys=True, separators=(',', ':'))
            pages_left = ceil(data.get('remaining') / 20)

            # pages_left + 2 because starting at 2 and range is right-exclusive
            for page in range(2, pages_left + 2):
                response = session.get("http://www.ratemyprofessors.com/paginate/professors/ratings?tid={0}&page={1}".format(professor[0], page))
                data = response.json()
                reviews = data.get('ratings')
                for review in reviews:
                    review['professorID'] = professor[0]
                    review['name'] = professor[1]
                    review['department'] = department
                with open('RMPData.json', 'r') as outfile:
                    savedReviews = json.load(outfile)
                with open('RMPData.json', 'w') as outfile:
                    savedReviews += (reviews)
                    json.dump(savedReviews, outfile, indent=4, sort_keys=True, separators=(',', ':'))


# get all of them
# for the first load, need to initialize a file with [] in it
# Northeastern's ID is 696
#professors = getProfessors('Mathematics', 696)
#getReviewsForProfessors(professors, 'Mathematics')
