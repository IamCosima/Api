import textwrap
from turtle import title
from urllib import request, response
import requests
import json
from rich import _console
from tabulate import tabulate
import typer
import pprint

app = typer.Typer()
table_length = 0

@app.command()
def search(keyword: str):
    global table_length
    """ Section A
In this section, you will extract a list of movie reviews from the New York Times (NYT) API.
The user should be able to filter movies based on a specified keyword in the review
headlines. Write the results to a sheet in the spreadsheet.
Requirements:
● Extract a list of movie reviews from the NYT API.
● The user must be able to specify a keyword (filter_word) to filter the reviews based on
their headline.
● The section_name should be "Movies" and type_of_material should be "Review".
● Choose and return a total of 8 fields from the reviews.
● Write all results to a Google Sheet """

    key = '&api-key=w9G84lJKsxdCMBVRkYQKAfkHiEwiz7Uw'
    base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    query = keyword
    fq = 'fq=typeOfMaterials%3AReview%20AND%20section.name%3AMovies%20AND%20headline.default%3A'+ query + '&sort=relevance'

    api_request = base_url + fq + key

    response = requests.get(api_request)
    

    data = response.json()
    dataset = data['response']['docs']
    #pprint.pprint(dataset)
    nytimesmovieData = []
    movies = []
    nytimesmovieData_headers = ['Headline','Author','Publication Date','Source','Movie Title','Web Url','Word Count']
    for item in dataset:
        movie_title = None
        #print(item.get('keywords',[]))
        for word in item.get('keywords',[]):
            #print(word.get('name'))
            if ( word.get('name') == 'Title'):
                movie_title = word.get('value');
                #print(movie_title)
                
                
            if (movie_title == None):
                #print("Title not found")
                movie_title = 'No Title'
                
                
        headline = "\n".join(textwrap.wrap(item.get('headline',{}).get('main'),width=40))
        #Abstract too long so will be ommited
        #abstract = "\n".join(textwrap.wrap(item.get('abstract'),width=50))
        
        #remove (Movie) from title
        string = '(Movie)'
        string2 = 'No Title'
       # print(movie_title)
        if movie_title.find(string) != -1:
            movie_title = movie_title.replace(string,'')
        elif movie_title.find(string.upper()) != -1:
            movie_title = movie_title.replace(string.upper(),'')
        elif movie_title.find(string2) != -1:
            print("Skipped")
            
        #print(movie_title + 'After')
                        
            
        details = {
            'title' : movie_title,
            'url' :item.get('web_url')
            
        }
        
        
        movie_title = "\n".join(textwrap.wrap(movie_title,width=20))
        
        movie = [
            headline,
            #abstract,
            item.get('byline',{}).get('original'),
            item.get('pub_date'),
            item.get('source'),
            movie_title,
            item.get('web_url'),
            item.get('word_count')
        ] 
        nytimesmovieData.append(movie)    
        movies.append(details) 
        
    print(tabulate(nytimesmovieData,headers=nytimesmovieData_headers,tablefmt='fancy_grid'))
    table_length = len(nytimesmovieData)
    return movies
    
@app.command()
def detailed(keyword: str):
    movies = search(keyword)
    #print(movies)
    tmdbkey = 'api_key=2a5f41d5ac3266aae57fdf6515833b8b'
    tmdbbase_url = 'https://api.themoviedb.org/3/search/movie?'
    table = table_length
    #print(table)
    tmdbmovieData = []
    tmbmovieHeadings = []
    tmbmovieHeadings = ['Title','Overview','Recent Popularity /100','Budget($)','Revenue($)','Release Date','Duration (Mins)','Review']
    
    for movie in range(table):
       # print(movies[movie]['title'])
        request = tmdbbase_url + 'query='+ movies[movie]['title'] + '&' + tmdbkey

        response = requests.get(request)
        data = response.json()
        dataset = data['results']
        
        movieid = dataset[0]['id']
        
        new_url = 'https://api.themoviedb.org/3/movie/'
        detail_movie_request = new_url + str(movieid) +'?'+ tmdbkey
        detail_movie_response = requests.get(detail_movie_request)
        detail_data = detail_movie_response.json()
        detailed_dataset = detail_data
        
        overview = "\n".join(textwrap.wrap(detailed_dataset['overview'],width=30))
        
        tmdbmovieData.append(
            [
                detailed_dataset['title'],
                overview,
                #detailed_dataset['overview'],
                detailed_dataset['popularity'],
                detailed_dataset['budget'],
                detailed_dataset['revenue'],
                detailed_dataset['release_date'],
                detailed_dataset['runtime'],
                movies[movie]['url']
                
            ]
        )
    print(tabulate(tmdbmovieData,headers=tmbmovieHeadings,tablefmt='fancy_grid'))
    
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    




if __name__ == "__main__":
    app()
