import React from 'react'
import axios from 'axios';

class Map extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            "polygons": [],
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
          }).catch(error => console.log(error))
    }

    async componentDidMount() {
        this.load_data()
    }

    render() {
        return (
            <div>
                map
            </div>
        )
    }
}

export default Map