from models import Game, Year
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


engine = create_engine("sqlite:///data/game_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()


def string_to_date(str_date):
    return datetime.strptime(str_date, "%Y-%m-%d")

def new_entry(name, time_spent, review, image,  dlc, achievements, date):
    image_data = None
    if image:
        with open(image, "rb") as image_file:
            image_data = image_file.read()
    if type(date) is str:
        date = string_to_date(date)

    new_game = Game(
        name=name,
        image=image_data,
        time_spent=time_spent,
        dlc=dlc,
        achievements=achievements,
        date=date,
        review=review
    )
    session.add(new_game)
    session.commit()

    new_year = Year(
        year=new_game.date.year,
        game_id=new_game.id,
        game_name=new_game.name
    )
    session.add(new_year)
    session.commit()


def edit_entry(entry, name, time_spent, review, image,  dlc, achievements, date):
    if type(image) is str:
        with open(image, "rb") as image_file:
            image_data = image_file.read()
            entry.image = image_data
    elif image is None:
        pass
    if type(date) is str:
        date = string_to_date(date)
    entry.name = name
    entry.time_spent = time_spent
    entry.dlc = dlc
    entry.achievements = achievements
    entry.date = date
    entry.review = review
    session.commit()

    year_entry = session.query(Year).filter(Year.game_id == entry.id).first()
    year_entry.year = entry.date.year
    year_entry.game_name = entry.name
    session.commit()

def delete_entry(entry):
    session.delete(entry)
    session.commit()

def delete_all_data():
    session.query(Game).delete()
    session.query(Year).delete()
    session.commit()

def get_names():
    games = session.query(Game).order_by(Game.id.desc()).all()
    names = [game.name for game in games]
    return names

def get_years():
    entries = session.query(Year.year).distinct().all()
    years = sorted([year[0] for year in entries])
    formatted_years = [str(year) for year in years]
    formatted_years.insert(0, "All Time")
    return formatted_years

def get_games_by_year(selected_year):
    games = session.query(Year.game_name).order_by(Year.game_id.desc()).filter_by(year=selected_year).all()
    list_of_games = [game[0] for game in games]
    return list_of_games

def get_game_by_name(game_name):
    game = session.query(Game).filter(Game.name == game_name).first()
    return game
