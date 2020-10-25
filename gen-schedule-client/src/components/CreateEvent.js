import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/CreateEvent.css';
import UserContext from '../context/UserContext';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Grid from '@material-ui/core/Grid';
import moment from 'moment';
import MomentUtils from '@date-io/moment';
import {
    TimePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';

class CreateEvent extends React.Component {
    static contextType = UserContext;
    constructor(props) {
        super(props);

        this.state = {
            user: {},
            events: [],
            expanded: false,
            fixed: false,
            validated: false,
            eventName: "",
            startTime: moment().toDate(),
            endTime: moment().add(30, 'm').toDate(),
            priority: 1,
            duration: 0.5,
        }

        this.handleChange = this.handleChange.bind(this);
        this.createEvent = this.createEvent.bind(this);
        this.clickCreate = this.clickCreate.bind(this);
        this.handleFixed = this.handleFixed.bind(this);
        this.setStartTime = this.setStartTime.bind(this);
        this.setEndTime = this.setEndTime.bind(this);
        this.setPriority = this.setPriority.bind(this);
        this.setDuration = this.setDuration.bind(this);
    }
    handleChange(e) {
        this.setState({ eventName: e.target.value });
    }

    createEvent(e) {
        const form = e.currentTarget;
        if (form.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            e.preventDefault();

            let event = { eventName: this.state.eventName, start: moment(this.state.startTime).format('HH:mm'), end: moment(this.state.endTime).format('HH:mm'), priority: this.state.priority, fixed: this.state.fixed, duration: this.state.duration };
            if (!event.fixed) {
                event.start = "";
                event.end = "";
            } else {
                event.priority = 4;
            }

            this.context.updateSch(event);

            this.setState({
                expanded: false,
                fixed: false,
                eventName: "",
                startTime: moment().toDate(),
                endTime: moment().add(30, 'm').toDate(),
                priority: 1,
                duration: 0.5,
            });
        }

        this.setState({ validated: true });
    }

    clickCreate() {
        this.setState({ expanded: true });
    }

    handleFixed() {
        this.setState(prev => ({ fixed: !prev.fixed }))
    }

    setStartTime(date) {
        this.setState({ startTime: date.toDate() });
    }

    setEndTime(date) {
        this.setState({ endTime: date.toDate() });
    }

    setPriority(e) {
        this.setState({ priority: e.target.value });
    }

    setDuration(e) {
        this.setState({ duration: e.target.value });
    }


    render() {
        return (
            <UserContext.Consumer>
                {
                    ({ user, events, updateSch, updateProp }) => {
                        return (
                            <div className="container-fluid">
                                <Form className="name-wrapper p-3 rounded text-left w-50 mx-auto create-event-wrapper m-0" onSubmit={this.createEvent}>
                                    <Form.Group controlId="validationCustom01" className="m-0">
                                        {
                                            this.state.expanded &&
                                            <Form.Label>New Event</Form.Label>
                                        }
                                        <InputGroup className={(this.state.expanded) ? "mb-3" : ""}>
                                            <Form.Control value={this.state.eventName} type="text" placeholder="Event" onChange={this.handleChange} onClick={this.clickCreate} />
                                        </InputGroup>
                                        {
                                            this.state.expanded &&
                                            <Grid container justify="space-evenly" align="center" direction="row" className='my-3'>
                                                <FormControlLabel
                                                    control={
                                                        <Checkbox
                                                            checked={this.state.fixed}
                                                            onChange={this.handleFixed}
                                                            name="fixed"
                                                            color="primary" />
                                                    }
                                                    label="Fixed" />
                                                <FormControl disabled={this.state.fixed}>
                                                    <InputLabel>Priority</InputLabel>
                                                    <Select
                                                        defaultValue={1}
                                                        value={this.state.priority}
                                                        onChange={this.setPriority}>
                                                        <MenuItem value={1}>Low</MenuItem>
                                                        <MenuItem value={2}>Medium</MenuItem>
                                                        <MenuItem value={3}>High</MenuItem>
                                                    </Select>
                                                </FormControl>
                                                <FormControl disabled={this.state.fixed}>
                                                    <InputLabel>Duration</InputLabel>
                                                    <Select
                                                        defaultValue={1}
                                                        value={this.state.duration}
                                                        onChange={this.setDuration}>
                                                        <MenuItem value={0.5}>30 minutes</MenuItem>
                                                        <MenuItem value={1}>1 hour</MenuItem>
                                                        <MenuItem value={1.5}>1.5 hours</MenuItem>
                                                        <MenuItem value={2}>2 hours</MenuItem>
                                                        <MenuItem value={2.5}>2.5 hours</MenuItem>
                                                        <MenuItem value={3}>3 hours</MenuItem>
                                                    </Select>
                                                </FormControl>
                                            </Grid>
                                        }
                                        {
                                            this.state.fixed &&
                                            <MuiPickersUtilsProvider utils={MomentUtils}>
                                                <Grid container justify="space-around">
                                                    <TimePicker value={this.state.startTime} onChange={this.setStartTime} label='Start Time' />
                                                    <TimePicker value={this.state.endTime} onChange={this.setEndTime} label='End Time' />
                                                </Grid>
                                            </MuiPickersUtilsProvider>
                                        }
                                        {
                                            this.state.expanded &&
                                            <div className='text-center'>
                                            <Button className='create-new-btn my-3' variant='primary' type='submit'>Create New Event</Button>
                                            </div>
                                        }
                                    </Form.Group>
                                </Form>
                            </div>
                        );
                    }
                }
            </UserContext.Consumer>
        );
    };
}

export default CreateEvent;