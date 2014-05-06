from flask import Flask
from flaskext.googlemaps import GoogleMaps
from flaskext.googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def mapview():
    # creating a map in the view
    mymap = Map(
            identifier="view-side",
            lat=37.4419,
            lng=-122.1419,
            markers=[(37.4419, -122.1419)]
            )
    return render_template('example.html', mymap=mymap)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
