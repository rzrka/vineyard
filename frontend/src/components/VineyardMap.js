import React from 'react'
import axios from 'axios';
import { YMaps, Map, Polygon } from "react-yandex-maps";
import PolygonDetail from './PolygonDetail';


class VineyardMap extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            // набор полигонов
            "polygons": [],
            // центральный полигон
            "center": [],
            // выбранный полигон
            "curPolygon": ''
        }
    }

    getCenter(data) {
        // определение центрального полигона
        let center = data[data.length/2]
        // возвращает долготу и широту
        return [center.lat, center.lng]
    }
    
    setData(data){
        // сохранения данных от бэкенда на фронтенд
        this.setState(
            {
              "polygons": data,
              "center": this.getCenter(data),
            }
          )
    }

    componentToHex(c) {
        // парсинг строки hex
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
      }
      
    rgbToHex(r, g, b) {
        // преобразование значения rgb в значения hex для цветного отображения полигона
        return "#" + this.componentToHex(r) + this.componentToHex(g) + this.componentToHex(b);
      }

    getColor(score) {
        // получение значения красного в цвета в зависимости от скоринга
        let r = Math.ceil(255 * (1 - score / 100))
        // получение значения зеленого в цвета в зависимости от скоринга
        let g = Math.ceil(255 * score / 100)
        // преобразование цвета rgb в hex
        let color = this.rgbToHex(r,g,0)
        return color
    }

    load_data() {
        // отправка гет запрос на бэкенд приложения
        axios.get('http://127.0.0.1:8000/polygons/')
        .then(response => {
            // при успешном запросе, ответ отправляется в метод для сохранения наборов
            this.setData(response.data)
          }).catch(error => console.log(error))
    }

    componentDidMount() {
        // метод выполняется каждый раз при загрузке страницы
        this.load_data()
    }
    
    polyginDetailBtn(polygon) {
        // сохранения выбранного полигона в состояние страницы
        this.setState(
            {
                "curPolygon": polygon
            }
        )
    }

    render() {
        return (
            <div className="row">
                {/* если в состояние загружены полигоны, то отрисовывается компонент карты */}
                {this.state.polygons.length != 0 &&
                <YMaps>
                    <div className="col-md-8 offset-md-2">
                        {/* комоненты карты для отображения карты на страницы с заданными настройками */}
                    <Map defaultState={{ 
                        center: [this.state.polygons[0].y1, this.state.polygons[0].x1], zoom: 18}} 
                        style={{width: "100%", height: "1200px", margin: "auto"}}
                        onClick={() => this.setState({"curPolygon": ''})}
                    >
                        {/* итерация по полигонам для отрисовки каждого из них */}
                        {this.state.polygons.map(polygon =>
                            <div key={polygon.id}>
                                {/* компонент полигона для отображения полигона на карте с заданнами настройками */}
                            <Polygon
                                geometry={[[
                                    [polygon.y1, polygon.x1],
                                    [polygon.y3, polygon.x3],
                                    [polygon.y4, polygon.x4],
                                    [polygon.y2, polygon.x2],
                                ]]} 
                                options={{
                                fillColor: this.getColor(polygon.score), // цвет квадрата
                                strokeColor: '#000000', // цвет границы квадрата
                                opacity: 0.2, // прозрачность квадрата
                                strokeWidth: 5, // толщина границы квадрата
                                strokeStyle: 'solid' // тип границы квадрата
                                }}
                                onClick={() => this.polyginDetailBtn(polygon)}
                            />
                            </div>
                        )}
                    </Map>
                    </div>
                </YMaps>
                }
                {/* загрузка компонента который отвечает за отрисовку бокового меню */}
            <PolygonDetail polygon={this.state.curPolygon}/>
            </div>
        )
    }
}

export default VineyardMap