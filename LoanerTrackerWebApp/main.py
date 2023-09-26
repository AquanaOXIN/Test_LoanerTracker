from website import create_app # website is a Python package because having __init__.py

app = create_app()

if __name__ == '__main__': # only run the web server when running it from this current file
    app.run(debug=True) # run the web server