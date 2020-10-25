import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/EventManager.css';
import '../App.css';
import logo from '../assets/pyd-logo.png';
import CreateEvent from '../components/CreateEvent';
import SchedViz from '../components/SchedViz';
import UserContext from '../context/UserContext';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';
import _ from 'lodash';
import content from '../static.json';

function chronoSort(a, b) {
    let endA = a.end.split(':');
    let endB = b.end.split(':');

    let totalA = parseInt(endA[0]) * 60 + parseInt(endA[1]);
    let totalB = parseInt(endB[0]) * 60 + parseInt(endB[1]);

    if (totalA < totalB)
        return -1;
    if (totalA > totalB)
        return 1;
    return 0;
}

class EventManager extends React.Component {
    static contextType = UserContext;
    constructor(props) {
        super(props);

        this.state = {
            submit: false,
            inProgress: false,
        }

        this.submitSch = this.submitSch.bind(this);
    }

    componentDidMount() {
        console.log(this.context.user);
    }

    submitSch() {
        this.setState({ inProgress: true });

        console.log(this.context.events);
        axios.post(`${content.api}/event-manager`, { events: this.context.events, start: moment(this.context.user.wakeTime).format('HH:mm'), end: moment(this.context.user.bedTime).format('HH:mm') })
            .then(res => {
                console.log(res);
                console.log(res.data);
                if (res.status === 200) {
                    let bestSch = res.data;
                    let dispSch = [];

                    for (let i = 0; i < bestSch.length; i++) {
                        dispSch.push({ eventName: bestSch[i][0], start: bestSch[i][1], end: bestSch[i][2], fixed: true, priority: 4 });
                    }
                    
                    dispSch.sort(chronoSort);

                    this.context.updateProp('dispSch', dispSch);
                    this.setState({ submit: true, inProgress: false });
                }
            })
            .catch(err => {
                console.error(err);
            });
    }

    render() {
        return (
            <UserContext.Consumer>
                {
                    ({ user, events, updateSch, updateProp }) => {
                        if (this.state.submit)
                            return <Redirect to='/scheduler' />
                        return (
                            <div className='container-fluid p-1 spinner-wrapper'>
                                <img className='logo' src={logo} alt='Logo' />
                                <Modal
                                    size="lg"
                                    aria-labelledby="contained-modal-title-vcenter"
                                    centered
                                    show={this.state.inProgress}
                                    backdrop="static"
                                    keyboard={false}>
                                    <Modal.Body className='p-3 text-center'>
                                        <h5>Generating Optimal Schedule...</h5>
                                        <CircularProgress />
                                    </Modal.Body>
                                </Modal>

                                <div className="container-fluid p-3">
                                    <CreateEvent />

                                    <SchedViz events={events} />
                                    {
                                        !_.isEmpty(events) &&
                                        <div className='text-center py-3'>
                                            <Button variant="primary" onClick={this.submitSch}>Submit Schedule</Button>
                                        </div>
                                    }
                                </div>
                            </div>
                        );
                    }
                }
            </UserContext.Consumer>
        );
    }
}

export default EventManager;