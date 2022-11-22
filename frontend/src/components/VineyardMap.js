import React from 'react'
import axios from 'axios';
import { YMaps, Map, Rectangle, Polyline, Polygon } from "react-yandex-maps";


class VineyardMap extends React.Component {
    
    getCenter(data) {
        let center = data[data.length/2]
        return [center.lat, center.lng]
    }

    constructor(props) {
        super(props);
        this.state = {
            "polygons": [],
            "center": [],
            'data_loaded': false,
        }
    }

    setData(data){
        this.setState(
            {
              "polygons": data,
              "center": this.getCenter(data),
              "data_loaded": true,
            }
          )
        console.log(this.state.polygons[0])
    }

    load_data() {
        axios.get('http://127.0.0.1:8000/polygons')
        .then(response => {
            this.setData(response.data)
          }).catch(error => console.log(error))
    }

    componentDidMount() {
        this.load_data()
    }
    
    render() {
        return (
            <div class="row">
                {this.state.data_loaded &&
                <YMaps>
                    <div class="col-md-8 offset-md-2">
                    <Map defaultState={{ 
                        center: [this.state.polygons[0].y1, this.state.polygons[0].x1], zoom: 18}} 
                        style={{width: "600px", height: "400px", margin: "auto"}}
                    >
                        {this.state.polygons.map(polygon => 
                            <Polygon
                                geometry={[[
                                    [polygon.y1, polygon.x1],
                                    [polygon.y3, polygon.x3],
                                    [polygon.y4, polygon.x4],
                                    [polygon.y2, polygon.x2],
                                ]]} 
                                options={{
                                fillColor: '#46ff00', // цвет квадрата
                                strokeColor: '#000000', // цвет границы квадрата
                                opacity: 0.6, // прозрачность квадрата
                                strokeWidth: 5, // толщина границы квадрата
                                strokeStyle: 'solid' // тип границы квадрата
                                }}
                            />
                        )}
                    </Map>
                    </div>
                </YMaps>
                }
            </div>
        )
    }
}

export default VineyardMap