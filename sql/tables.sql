CREATE TABLE IF NOT EXISTS account (
    id serial PRIMARY KEY,
    username VARCHAR (20) UNIQUE NOT NULL,
    password VARCHAR (20) NOT NULL,
    email VARCHAR (50) UNIQUE NOT NULL,
    created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS result(
    id serial PRIMARY KEY,
    description VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS game(
    id bigserial PRIMARY KEY,
    start_time timestamp NOT NULL,
    end_time timestamp,
    player_one_id int NOT NULL,
    player_two_id int NOT NULL,
    result_id int,
    FOREIGN KEY (player_one_id) REFERENCES account (id),
    FOREIGN KEY (player_two_id) REFERENCES account (id),
    FOREIGN KEY (result_id) REFERENCES result (id) 
);

CREATE TABLE IF NOT EXISTS player(
    id serial PRIMARY KEY,
    player_id int NOT NULL,
    game_id int NOT NULL,
    FOREIGN KEY (player_id) REFERENCES account (id),
    FOREIGN KEY (game_id) REFERENCES game (id)
);