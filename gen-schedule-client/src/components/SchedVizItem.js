import React from 'react';
import '../css/SchedVizItem.css';

class SchedVizItem extends React.Component {
    render() {
        return (
            <div className="item-wrapper p-5 rounded my-3">
                <div className={"rounded-top priority-strip-" + this.props.priority}></div>
                <h1>{this.props.title}</h1>
                {
                    this.props.fixed &&
                    <h5 className='font-med'>Start Time: {this.props.start} &#8594; End Time: {this.props.end}</h5> 
                }
                {
                    !this.props.fixed &&
                    <h5 className='font-med'>Expected Duration: {this.props.duration} hour{(this.props.duration !== 1) ? 's' : ''}</h5>
                }
            </div>
        );
    }
}

export default SchedVizItem;