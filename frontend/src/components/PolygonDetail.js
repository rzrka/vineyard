import React from 'react';
import '../styles/css/PolygonDetail.css';

const PolygonDetail = ({polygon}) => {

    return (
        <div className={polygon.id ? 'polygon-detail active' : 'polygon-detail'}>
            <div className='menu__content' onClick={e => e.stopPropagation()}>
                <ul className='polygon-ul'>
                    {Object.keys(polygon).map(key => 
                        <li className='polygon-li'>{key} --- {polygon[key]}</li>
                    )}
                </ul>
            </div>
        </div>
    )
}

export default PolygonDetail;