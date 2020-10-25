import React from 'react';
import '../css/SchedViz.css';
import SchedVizItem from './SchedVizItem';

class SchedViz extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let elements = [];
        let key = 0;
        
        for (const event of this.props.events)
            elements.push(<SchedVizItem key={key++} title={event.eventName} start={event.start} end={event.end} fixed={event.fixed} priority={event.priority} duration={event.duration} />);

        return (
            <div className="container-fluid mt-5">
                {elements}
            </div>
        );
    }
}

export default SchedViz;