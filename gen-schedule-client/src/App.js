import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import Bedtime from './pages/Bedtime';
import EventManager from './pages/EventManager';
import Scheduler from './pages/Scheduler';
import UserContext from './context/UserContext';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.updateProp = (prop, value) => {
      this.setState(prevState => {
        let user = prevState.user;
        user[prop] = value;
        return { user: user };
      });
    }

    this.updateSch = (item) => {
      this.setState(prev => {
        const list = [...prev.events, item]
        return { events: list };
      });
    }

    this.state = { user: {}, events: [], updateSch: this.updateSch, updateProp: this.updateProp };
  }

  render() {
    return (
      <Router>
        <UserContext.Provider value={this.state}>
          <Switch>
            <Route path='/scheduler' component={Scheduler} />
            <Route path='/event-manager' component={EventManager} />
            <Route path='/' component={Bedtime} />
          </Switch>
        </UserContext.Provider>
      </Router>
    );
  };
}

export default App;
