import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import HiddenFile as HF
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def get_suggsested_tracks(playlist_id, user_id, user_secret):
    #setup and get the playlist
    sp = HF.setup(user_id, user_secret)
    playlist_tracks = sp.playlist_items(playlist_id=playlist_id)
    track_ids = []

    #find the track ids and find the dataset 
    for item in playlist_tracks['items']:
        track_ids.append(item['track']['id'])
        
    #creating the data set where we have the available data and remove from current dataframe
    df=pd.read_csv('cleaned_data.csv')
    user_songs_df = df[df['id'].isin(track_ids)]
    df=df[~df['id'].isin(track_ids)]

    #create one average vector
    df_for_vector_user = user_songs_df.drop(columns=['Unnamed: 0', 'track_name', 'id', 'track_artist'], axis=1)
    df_for_vector_total = df.drop(columns=['Unnamed: 0', 'track_name', 'id', 'track_artist'], axis=1)

    vector_means_user = df_for_vector_user.mean().values.reshape(1,-1)
    vector_means_total = df_for_vector_total.values

    #scale 
    scaler = StandardScaler()
    vector_means_total_scaled = scaler.fit_transform(vector_means_total)
    vector_means_user_scaled = scaler.transform(vector_means_user)

    #create model
    model = NearestNeighbors(n_neighbors=5, metric='euclidean')
    model.fit(vector_means_total_scaled)
    distances, indices = model.kneighbors(vector_means_user_scaled)

    indices = indices.flatten()

    suggested_tracks = df.iloc[indices]['track_name'].tolist()
    print("Suggested tracks:", suggested_tracks)
    return suggested_tracks

#'5esPzusJY3hdg61SwtlZAN'
#'eb766e4c568d4a568eb4dcbf5d282086'
#'45d4a12be955461fbcd66da0c267c274'