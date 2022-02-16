# importar librerias
from curses import reset_shell_mode
import pandas as pd
import requests
import json

# Pregunta 1
def pregunta_1():
    # Conseguimos el total de pokemones
    r = requests.get('https://pokeapi.co/api/v2/pokemon/').json()
    count = r["count"]
    
    # Pedimos el total
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit={count}').json()
    df = pd.DataFrame(r['results'])
    
    # Filtramos por lo especificado
    df_filtered = df[(df.name.str.contains('at')) & (df.name.str.count('a') == 2)]
    return f'Respuesta P1: {df_filtered.count()[0]}'

# Pregunta 2
def pregunta_2(pokemon='raichu'):
    # Pedimos el numero de grupos
    count = requests.get('https://pokeapi.co/api/v2/egg-group/').json()['count']
    
    # Para cada grupo vemos si raichu pertenece o no, y adjuntamos todos los pokemones que pertenezcan al mismo grupo
    df_egg_groups = pd.DataFrame()
    for i in range(1, count+1):
        r = requests.get(f'https://pokeapi.co/api/v2/egg-group/{i}').json()
        df_aux = pd.DataFrame(r['pokemon_species'])
        df_aux['group'] = r['name']
        df_egg_groups = df_egg_groups.append(df_aux, ignore_index = True)
    
    # Ordenamos el dataframe
    aux = df_egg_groups.loc[df_egg_groups['name'].str.lower() == pokemon, ['group']]
    df_egg = df_egg_groups[df_egg_groups['group'].isin(aux['group'].values)]
    df_egg = df_egg.drop(columns=['group', 'url'])
    
    # Eliminamos duplicados
    df_egg = df_egg.drop_duplicates()
    
    # Devolvemos la cuenta de los pokemon que cumplen
    return f'Respuesta P2: {df_egg.count()[0]}'

# Pregunta 3
def pregunta_3(tipo='fighting'):
    # Pedimos la lista de los fighting
    fighters = requests.get(f'https://pokeapi.co/api/v2/type/{tipo}').json()
    fighters = fighters['pokemon']
    fighters = pd.DataFrame(fighters)
    
    # Obtenemos sus números y filtramos los menores o iguales a 151
    fighters = pd.concat([fighters.drop(['pokemon'], axis=1), fighters['pokemon'].apply(pd.Series)], axis=1)
    fighters['num'] = fighters.apply(lambda x: int(x['url'].split('/')[6]), axis=1)
    fighters = fighters[fighters['num'] <= 151]
    
    # Iteramos buscando el mayor y menor peso guardandolos en variables
    pmin = 99999999
    pmax = 0
    for row in fighters.itertuples():
        r = requests.get(row[3]).json()
        if r['weight'] < pmin:
            pmin = r['weight']
        if r['weight'] > pmax:
            pmax = r['weight']

    # Finalmente creamos la lista final
    respuesta = [pmax, pmin]
    return f'Respuesta P3: {respuesta}'

print(pregunta_1())
print(pregunta_2())
print(pregunta_3())
