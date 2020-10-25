import React from 'react';
import '../App.css';
import logo from '../assets/pyd-logo.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import Grid from '@material-ui/core/Grid';
import moment from 'moment';
import MomentUtils from '@date-io/moment';
import {
    TimePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import { Redirect } from 'react-router-dom';
import UserContext from '../context/UserContext';

class Bedtime extends React.Component {
    static contextType = UserContext;
    constructor(props) {
        super(props);

        this.state = {
            wakeTime: moment().hour(8).minute(0),
            bedTime: moment().hour(23).minute(0),
            continue: false
        }

        this.setWakeTime = this.setWakeTime.bind(this);
        this.setBedTime = this.setBedTime.bind(this);
        this.setContinue = this.setContinue.bind(this);
    }

    setWakeTime(date) {
        this.setState({ wakeTime: date.toDate() });
    }

    setBedTime(date) {
        this.setState({ bedTime: date.toDate() });
    }

    setContinue() {
        console.log(this.state.wakeTime);
        console.log(this.state.bedTime);

        this.context.updateProp('wakeTime', this.state.wakeTime);
        this.context.updateProp('bedTime', this.state.bedTime);
        this.setState({ continue: true });
    }

    render() {
        return (
            <UserContext.Consumer>
                {
                    ({ user, events, updateSch, updateProp }) => {
                        if (this.state.continue)
                            return <Redirect to='/event-manager' />
                        return (
                            <div className='container-fluid p-1'>
                                <img className='logo' src={logo} alt='Logo' />
                                <div className='container-fluid px-5 py-3'>
                                    <h3 className='my-3'>What does your sleep schedule look like?</h3>
                                    <MuiPickersUtilsProvider utils={MomentUtils}>
                                        <Grid container justify="space-around" align='center' direction='row' className='my-5'>
                                            <TimePicker value={this.state.wakeTime} onChange={this.setWakeTime} label='Wake Up' />
                                            <TimePicker value={this.state.bedTime} onChange={this.setBedTime} label='Bed Time' />
                                        </Grid>
                                    </MuiPickersUtilsProvider>
                                    <div className='text-center'>
                                        <Button variant='primary' onClick={this.setContinue}>Continue</Button>
                                    </div>
                                </div>
                            </div>
                        );
                    }
                }
            </UserContext.Consumer>
        );
    }
}

export default Bedtime;