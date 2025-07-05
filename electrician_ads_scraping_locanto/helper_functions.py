import folium
from folium.plugins import HeatMap


def build_heatmap(df, lat_col="latitude", lon_col="longitude", radius=15):
    """
    Builds a Folium map with a heatmap and a custom legend."""
    fmap = folium.Map(location=[-25.2744, 133.7751], zoom_start=20)
    heat_data = df[["latitude", "longitude"]].values.tolist()
    HeatMap(
        heat_data,
        radius=15,
        gradient={0.2: "blue", 0.4: "cyan", 0.6: "lime", 0.8: "orange", 1.0: "red"},
    ).add_to(fmap)

    # Define legend HTML
    legend_html = """
     <div style="
     position: fixed;
     bottom: 50px; left: 50px; width: 160px; height: 120px;
     background-color: white;
     border:2px solid grey; z-index:9999; font-size:12px;
     padding: 10px;
     ">
     <b>Heatmap Legend</b><br>
     <i style="background: #00f; width: 10px; height: 10px; display: inline-block;"></i> Low Density<br>
     <i style="background: #0ff; width: 10px; height: 10px; display: inline-block;"></i> Moderate<br>
     <i style="background: #0f0; width: 10px; height: 10px; display: inline-block;"></i> High<br>
     <i style="background: #ff0; width: 10px; height: 10px; display: inline-block;"></i> Very High<br>
     <i style="background: #f00; width: 10px; height: 10px; display: inline-block;"></i> Peak<br>
     </div>
    """

    # Add legend once
    fmap.get_root().html.add_child(folium.Element(legend_html))

    return fmap
