import customtkinter
from models import Game, Base
from db_management import session, get_games_by_year, get_years, get_names, engine
from app import App


# Base.metadata.create_all(engine)


customtkinter.set_appearance_mode("dark")
app = App()

def update_combobox():
    years = get_years()
    games = get_names()

    app.left_frame.list_of_years.configure(values=years)
    app.left_frame.list_of_games.configure(values=games)


def update():
    all_games = session.query(Game).order_by(Game.id.desc()).all()
    if all_games:
        recently_added_game = all_games[0]
    else:
        recently_added_game = None

    update_combobox()
    selected_year = app.left_frame.list_of_years.get()
    selected_game_name = app.left_frame.list_of_games.get()
    if selected_year != "Year":
        app.left_frame.list_of_games.configure(values=get_games_by_year(selected_year))
    if selected_year == "All Time":
        app.left_frame.list_of_games.configure(values=get_names())
    if selected_game_name != "Game":
        selected_game = session.query(Game).filter_by(name=selected_game_name).first()
        if selected_game is None:
            app.left_frame.list_of_games.set("Game")
            update_combobox()
        else:
            app.set_object(selected_game)
            app.change_review_color(app.right_frame.review, selected_game.review)
    else:
        if selected_game_name == "Game" and len(all_games) != 0:
            selected_game = recently_added_game
            app.set_object(selected_game)
            app.change_review_color(app.right_frame.review, selected_game.review)
        else:
            app.set_intro_object()

    app.after(1000, update)


update()
app.mainloop()
