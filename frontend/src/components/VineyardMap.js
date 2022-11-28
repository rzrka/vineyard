import React from 'react'
import axios from 'axios';
import { YMaps, Map, Polygon } from "react-yandex-maps";
import PolygonDetail from './PolygonDetail';


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
            "curPolygon": ''
        }
    }

    setData(data){
        this.setState(
            {
              "polygons": data,
              "center": this.getCenter(data),
            }
          )
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
    
    polyginDetailBtn(polygon) {
        this.setState(
            {
                "curPolygon": polygon
            }
        )
        console.log(this.state.curPolygon)
    }

    render() {
        return (
            <div className="row">
                {this.state.polygons.length != 0 &&
                <YMaps>
                    <div className="col-md-8 offset-md-2">
                    <Map defaultState={{ 
                        center: [this.state.polygons[0].y1, this.state.polygons[0].x1], zoom: 18}} 
                        style={{width: "100%", height: "1200px", margin: "auto"}}
                        onClick={() => this.setState({"curPolygon": ''})}
                    >
                        {/* <Polygon
                                geometry={[[
                                    [this.state.polygons[0].y1, this.state.polygons[0].x1],
                                    [this.state.polygons[0].y3, this.state.polygons[0].x3],
                                    [this.state.polygons[0].y4, this.state.polygons[0].x4],
                                    [this.state.polygons[0].y2, this.state.polygons[0].x2],
                                ]]} 
                                options={{
                                fillColor: '#46ff00', // цвет квадрата
                                strokeColor: '#000000', // цвет границы квадрата
                                opacity: 0.6, // прозрачность квадрата
                                strokeWidth: 5, // толщина границы квадрата
                                strokeStyle: 'solid' // тип границы квадрата
                                }}
                                onClick={() => this.polyginDetailBtn(this.state.polygons[0])}
                            /> */}
                        
                        {this.state.polygons.map(polygon =>
                            <div key={polygon.id}>
                            {polygon.score == 100 ?
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
                                opacity: 0.2, // прозрачность квадрата
                                strokeWidth: 5, // толщина границы квадрата
                                strokeStyle: 'solid' // тип границы квадрата
                                }}
                                onClick={() => this.polyginDetailBtn(polygon)}
                            />
                            :
                            <Polygon
                                geometry={[[
                                    [polygon.y1, polygon.x1],
                                    [polygon.y3, polygon.x3],
                                    [polygon.y4, polygon.x4],
                                    [polygon.y2, polygon.x2],
                                ]]} 
                                options={{
                                fillColor: '#ff0000', // цвет квадрата
                                strokeColor: '#000000', // цвет границы квадрата
                                opacity: 0.2, // прозрачность квадрата
                                strokeWidth: 5, // толщина границы квадрата
                                strokeStyle: 'solid' // тип границы квадрата
                                }}
                                onClick={() => this.polyginDetailBtn(polygon)}
                            />
                            }
                            </div>
                        )}
                    </Map>
                    </div>
                </YMaps>
                }
            <PolygonDetail polygon={this.state.curPolygon}/>
            </div>
        )
    }
}

export default VineyardMap