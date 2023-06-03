"""
sql_queries.py

This module contains SQL queries used in the data pipeline for loading and transforming data in Redshift. The queries are defined as class variables in the 'SqlQueries' class.

SqlQueries Class:
- songplay_table_insert: SQL query to insert records into the 'songplays' fact table by joining data from 'staging_events' and 'staging_songs' tables.
- user_table_insert: SQL query to insert records into the 'users' dimension table by selecting distinct user-related information from the 'staging_events' table.
- song_table_insert: SQL query to insert records into the 'songs' dimension table by selecting distinct song-related information from the 'staging_songs' table.
- artist_table_insert: SQL query to insert records into the 'artists' dimension table by selecting distinct artist-related information from the 'staging_songs' table.
- time_table_insert: SQL query to insert records into the 'time' dimension table by extracting various time-related components from the 'songplays' table.

Usage: Import the 'SqlQueries' class from this module to access the SQL queries used in the Redshift data pipeline.
"""

class SqlQueries:
    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)