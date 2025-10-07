import requests
import plotly.graph_objects as go

def geocode(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json'}
    headers = {'User-Agent': 'GeoMapper'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def generate_tracking_map(package):
    # Step 1: Get locations
    locations = [
        package.sending_location,
        package.current_location,
        package.receiving_location
    ]

    # Step 2: Geocode each location
    coordinates = [geocode(loc) for loc in locations]
    
    # Create completed route (origin to current)
    completed_route = go.Scattermapbox(
        mode="markers+lines",
        lat=[coordinates[0][0], coordinates[1][0]],
        lon=[coordinates[0][1], coordinates[1][1]],
        text=[package.sending_location, package.current_location],
        marker=dict(
            size=12,
            color=['#4CAF50', '#FF9800']
        ),
        line=dict(
            width=3,
            color='blue'
        ),
        name="Our warehouse"
    )

    # Create pending route (current to destination)
    pending_route = go.Scattermapbox(
        mode="markers+lines",
        lat=[coordinates[1][0], coordinates[2][0]],
        lon=[coordinates[1][1], coordinates[2][1]],
        text=[package.current_location, package.receiving_location],
        marker=dict(
            size=12,
            color=['blue', 'red']
        ),
        line=dict(
            width=3,
            color='gray'
        ),
        name="On Route to Destination"
    )

    # Create figure and update layout
    fig = go.Figure(data=[completed_route, pending_route])

    # Calculate center point
    lats = [coord[0] for coord in coordinates if coord[0] is not None]
    lons = [coord[1] for coord in coordinates if coord[1] is not None]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)

    fig.update_layout(
        mapbox=dict(
            style='carto-positron',
            zoom=2,
            center=dict(lat=center_lat, lon=center_lon)
        ),
        mapbox_zoom=5,
        showlegend=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=400
    )

    return fig.to_html(full_html=False, config={'displayModeBar': False})
