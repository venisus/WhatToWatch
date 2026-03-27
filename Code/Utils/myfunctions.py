import json
import requests

def parse_movie_title(title_json):
    """
    This function takes the response string from a movie/s request
    and parses it to keep only relevant keys and relevant subkeys.

    inputs:
        title_json (str): a string with the following format -> '{"titles":[{"id":string,"type":string,"primaryTitle":string,...]}'
    
    returns:
        dict: dictionary of all movies with only necessary columns in json format -> {"movies":[{"id_1":string, "type":string...},{"id_2":string, "type":string...}]}
    """
        
    title_full_dict = json.loads(title_json)['titles']
    filtered_keys = ['id', 'type', 'primaryTitle', 'startYear', 'runtimeSeconds', 'genres', 'rating', 'plot', 'directors', 'writers', 'stars', 'originCountries', 'spokenLanguages', 'interests']
    title_filtered_list = [{key:(item[key] if key in item.keys() else None) for key in filtered_keys} for item in title_full_dict]

    final_list = []
    for title in title_filtered_list:
        title['directors'] = [{key:item[key] for key in ['id', 'displayName']} for item in title['directors']]
        title['writers'] = [{key:item[key] for key in ['id', 'displayName']} for item in title['writers']]
        title['stars'] = [{key:item[key] for key in ['id', 'displayName']} for item in title['stars']]
        title['originCountries'] = [{key:item[key] for key in ['name']} for item in title['originCountries']]
        title['spokenLanguages'] = [{key:item[key] for key in ['name']} for item in title['spokenLanguages']]
        title['interests'] = [{key:item[key] for key in ['id', 'name']} for item in title['interests']]

        final_list.append(title)

    return {'movies':final_list}

def get_id_from_title(movie_name, year=None):
    
    base_url = 'https://api.imdbapi.dev'
    response = requests.get(base_url + f'/search/titles?query={movie_name}').text
    response = json.loads(response)
    ids = []
    for movie in response['titles']:
        if year:
            if 'startYear' in movie.keys():
                if movie['startYear'] == year and movie['primaryTitle'] == movie_name:
                    ids.append(movie['id'])
        elif movie['primaryTitle'] == movie_name:
            ids.append(movie['id'])
    return ids
