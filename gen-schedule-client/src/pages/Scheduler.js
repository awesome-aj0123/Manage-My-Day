import React from 'react';
import '../App.css';
import '../css/Scheduler.css';
import logo from '../assets/pyd-logo.png';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import SchedViz from '../components/SchedViz';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import moment from 'moment';
import MomentUtils from '@date-io/moment';
import {
    TimePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import Rating from '@material-ui/lab/Rating';
import { Alert, AlertTitle } from '@material-ui/lab';
import axios from 'axios';
import content from '../static.json';
import UserContext from '../context/UserContext';

function isBetween(src, t1, t2) {
    let srcSplit = src.split(':');
    let t1Split = t1.split(':');
    let t2Split = t2.split(':');

    let srcTot = parseInt(srcSplit[0]) * 60 + parseInt(srcSplit[1]);
    let t1Tot = parseInt(t1Split[0]) * 60 + parseInt(t1Split[1]);
    let t2Tot = parseInt(t2Split[0]) * 60 + parseInt(t2Split[1]);

    return (srcTot <= t2Tot && srcTot >= t1Tot);
}

function greater(t1, t2) {
    let t1Split = t1.split(':');
    let t2Split = t2.split(':');

    let t1Tot = parseInt(t1Split[0]) * 60 + parseInt(t1Split[1]);
    let t2Tot = parseInt(t2Split[0]) * 60 + parseInt(t2Split[1]);

    return t1Tot > t2Tot;
}

function diff(t1, t2) {
    let t1Split = t1.split(':');
    let t2Split = t2.split(':');

    let t1Tot = parseInt(t1Split[0]) * 60 + parseInt(t1Split[1]);
    let t2Tot = parseInt(t2Split[0]) * 60 + parseInt(t2Split[1]);

    return t2Tot - t1Tot;
}

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

class Scheduler extends React.Component {
    static contextType = UserContext;
    constructor(props) {
        super(props);

        this.state = {
            showOptions: false,
            delayTime: moment().add(15, 'm').toDate(),
            currIndex: -1,
            nextIndex: -1,
            progress: 0,
            generating: false,
            showToast: false,
            showRating: true,
            ratingVal: "",
        }

        this.toggleOptions = this.toggleOptions.bind(this);
        this.setDelayTime = this.setDelayTime.bind(this);
        this.submitDelay = this.submitDelay.bind(this);
        this.submitRating = this.submitRating.bind(this);
    }

    componentDidMount() {
        console.log(this.context.user);

        // this.setState({ currIndex: -1 });

        let i = 0;
        let currentTime = moment().format('HH:mm');
        let currDiff = -1;

        for (const event of this.context.user.dispSch) {
            if (isBetween(currentTime, event.start, event.end)) {
                this.setState({ currIndex: i, nextIndex: (i + 1 < this.context.user.dispSch.length) ? i + 1 : -1 });
                currDiff = diff(event.start, event.end);
                break;
            } else if (greater(event.start, currentTime)) {
                this.setState({ nextIndex: i });
                break;
            }
            i++;
        }

        let checker = setInterval(() => {
            currentTime = moment().format('HH:mm');
            if (this.state.currIndex === -1) {
                let j = 0;
                for (const event of this.context.user.dispSch) {
                    if (isBetween(currentTime, event.start, event.end)) {
                        this.setState({ currIndex: j, nextIndex: (j + 1 < this.context.user.dispSch.length) ? j + 1 : -1 });
                        currDiff = diff(event.start, event.end);
                        break;
                    } else if (greater(event.start, currentTime)) {
                        this.setState({ nextIndex: j });
                        break;
                    }
                    j++;
                }
            } else {
                console.log(diff(this.context.user.dispSch[this.state.currIndex].start, currentTime) / currDiff * 100);
                let progress = Math.round(diff(this.context.user.dispSch[this.state.currIndex].start, currentTime) / currDiff * 100);
                this.setState({ progress: progress });
            }
        }, 10000);

        this.setState({ checker: checker });
    }

    componentWillUnmount() {
        clearInterval(this.state.checker);
    }

    toggleOptions() {
        this.setState(prev => ({ showOptions: !prev.showOptions }));
    }

    setDelayTime(date) {
        this.setState({ delayTime: date.toDate() });
    }

    submitDelay() {
        this.setState({ generating: true });
        this.toggleOptions();

        axios.post(`${content.api}/shift`, { delay: moment(this.state.delayTime).format('HH:mm') })
            .then(res => {
                console.log(res);
                if (res.status === 200) {
                    let bestSch = res.data;
                    let dispSch = [];

                    for (let i = 0; i < bestSch.length; i++) {
                        dispSch.push({ eventName: bestSch[i][0], start: bestSch[i][1], end: bestSch[i][2], fixed: true, priority: 4 });
                    }

                    dispSch.sort(chronoSort);

                    this.context.updateProp('dispSch', dispSch);
                    this.setState({
                        currIndex: -1,
                        nextIndex: -1,
                        generating: false,
                    });
                }
            })
            .catch(err => {
                console.error(err);
            });
    }

    submitRating() {
        this.setState({ showToast: true });
    }

    render() {
        return (
            <UserContext.Consumer>
                {
                    ({ user, events, updateSch, updateProp }) => {
                        return (
                            <div className='container-fluid p-1'>
                                <Modal
                                    size="lg"
                                    aria-labelledby="contained-modal-title-vcenter"
                                    centered
                                    show={this.state.generating}
                                    backdrop="static"
                                    keyboard={false}>
                                    <Modal.Body className='p-3 text-center'>
                                        <h5>Regenerating Optimal Schedule...</h5>
                                        <CircularProgress />
                                    </Modal.Body>
                                </Modal>

                                <Modal
                                    size="lg"
                                    aria-labelledby="contained-modal-title-vcenter"
                                    centered
                                    show={this.state.showOptions}
                                    onHide={this.toggleOptions}>
                                    <Modal.Header closeButton>
                                        <Modal.Title>Need More Time?</Modal.Title>
                                    </Modal.Header>
                                    <Modal.Body className='p-3 text-center'>
                                        <MuiPickersUtilsProvider utils={MomentUtils}>
                                            <Grid container justify="space-around">
                                                <TimePicker value={this.state.delayTime} onChange={this.setDelayTime} label='Delay Upcoming Events' />
                                            </Grid>
                                        </MuiPickersUtilsProvider>
                                    </Modal.Body>
                                    <Modal.Footer className='text-left'>
                                        <Button variant="primary" onClick={this.submitDelay}>
                                            Delay
                                        </Button>
                                    </Modal.Footer>
                                </Modal>

                                {/* <Modal
                                    size="lg"
                                    aria-labelledby="contained-modal-title-vcenter"
                                    centered
                                    show={this.state.showRating}
                                    onHide={this.submitRating}>
                                    <Modal.Header closeButton>
                                        <Modal.Title>How was the schedule?</Modal.Title>
                                    </Modal.Header>
                                    <Modal.Body className='p-3 text-center'>
                                        Please tell us what you think!
                                        <Grid container justify="space-around">
                                            <Rating
                                                name="simple-controlled"
                                                value={this.state.ratingVal}
                                                onChange={(event, newValue) => {
                                                    this.setState({ratingVal: newValue});
                                                }} />
                                        </Grid>
                                    </Modal.Body>
                                    <Modal.Footer className='text-left'>
                                        <Button variant="primary" onClick={this.submitRating}>
                                            Rate Schedule
                                        </Button>
                                    </Modal.Footer>
                                </Modal> */}

                                <img className='logo' src={logo} alt='Logo' />
                                <div className="container-fluid p-3">
                                    <div className='row'>
                                        <div className='col'>
                                            <SchedViz events={user.dispSch} />
                                        </div>
                                        <div className='col'>
                                            <div className='container-fluid py-5'>
                                                <h3>Current Event</h3>
                                                {
                                                    (this.state.currIndex !== -1 && this.state.currIndex < user.dispSch.length) ?
                                                        <div className="progress-wrapper p-5 rounded my-3">
                                                            <h1>{user.dispSch[this.state.currIndex].eventName}</h1>
                                                            <h5 className='font-med'>Start Time: {user.dispSch[this.state.currIndex].start} &#8594; End Time: {user.dispSch[this.state.currIndex].end} </h5>
                                                            <div className="rounded-bottom progress-fill" style={{ height: this.state.progress + '%' }}></div>
                                                        </div>
                                                        :
                                                        <h5>Nothing happening right now!</h5>
                                                }
                                                <div className='text-center'>
                                                    <Button variant='primary' className='need-more-time-btn' onClick={this.toggleOptions}>Need more time?</Button>
                                                </div>
                                            </div>
                                            <h3>Upcoming Events</h3>
                                            {
                                                (this.state.nextIndex !== -1 && this.state.nextIndex < user.dispSch.length) ?
                                                    <div className="progress-wrapper p-5 rounded my-3">
                                                        <h1>{user.dispSch[this.state.nextIndex].eventName}</h1>
                                                        <h5 className='font-med'>Start Time: {user.dispSch[this.state.nextIndex].start} &#8594; End Time: {user.dispSch[this.state.nextIndex].end} </h5>
                                                    </div>
                                                    :
                                                    <h5>Nothing coming up!</h5>
                                            }

                                        </div>
                                    </div>
                                </div>
                                {/* {
                                    this.state.showToast &&
                                    <Alert severity="info">
                                        <AlertTitle>Schedule Rating</AlertTitle>
                                        Thanks for the feedback!
                                    </Alert>
                                } */}
                            </div>
                        )
                    }
                }
            </UserContext.Consumer>
        );
    }
}

export default Scheduler;