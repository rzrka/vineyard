import React from 'react';
import '../styles/css/PolygonDetail.css';

const PolygonDetail = ({polygon}) => {

    return (
        <div className={polygon.id ? 'polygon-detail active' : 'polygon-detail'}>
            <div className='menu__content' onClick={e => e.stopPropagation()}>
                <ul className='polygon-ul'>
                    <li className='polygon-li'><b>Местность</b></li>
                    <li className='polygon-li'>{'Объемная плотность'} --- {polygon['bdod']}</li>
                    <li className='polygon-li'>{'Катионный обмен'} --- {polygon['cec']}</li>
                    <li className='polygon-li'>{'Крупные фрагменты'} --- {polygon['cfvo']}</li>
                    <li className='polygon-li'>{'Нитрогены'} --- {polygon['nitrogen']}</li>
                    <li className='polygon-li'>{'рН'} --- {polygon['phh2o']}</li>
                    <li className='polygon-li'>{'Концентрация органического углерода'} --- {polygon['soc']}</li>
                    <li className='polygon-li'>{'Кол-во ила'} --- {polygon['silt']}</li>
                    <li className='polygon-li'>{'Кол-во песка'} --- {polygon['sand']}</li>
                    <li className='polygon-li'>{'Кол-во глины'} --- {polygon['clay']}</li>
                    <li className='polygon-li'>{'Высота'} --- {polygon['elevation']}</li>
                    <li className='polygon-li'>{'Угол наклона'} --- {polygon['inclination']}</li>
                    <li className='polygon-li'><b>Погода</b></li>
                    <li className='polygon-li'>{'Температура'} --- {polygon["temp"]}</li>
                    <li className='polygon-li'>{'Атмосферное давление'} --- {polygon['pressure']}</li>
                    <li className='polygon-li'>{'Влажность'} --- {polygon['humidity']}</li>
                    <li className='polygon-li'>{'Скорость ветра'} --- {polygon['wind_speed']}</li>
                    <li className='polygon-li'>{'Облачность'} --- {polygon['clouds']}</li>
                    <li className='polygon-li'>{'Вариации погоды'} --- {polygon['weather']}</li>
                    <li className='polygon-li'><b>Качество</b></li>
                    <li className='polygon-li'>{'Скоринг'} --- {polygon['score']}</li>
                </ul>
            </div>
        </div>
    )
}

export default PolygonDetail;