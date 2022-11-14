import React from 'react'
import axios from 'axios';

class Map extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            "polygons": '',
        }
    }

    async load_data() {
        await axios.get('http://127.0.0.1:8000/polygons')
        .then(response => {
            console.log(response.data)
            this.setState(
              {
                "polygons": response.data,
              }
            )
            console.log(this.state)
          }).catch(error => console.log(error))
    }

    componentDidMount() {
        this.load_data()
        console.log(this.state)
    }

    render() {
        return (
            <div>
                map
                {this.state.polygons.map((polygon) =>
                <p>{polygon.id}</p>
                )} 
            </div>
        )
    }
}

export default Map