import React from 'react';

const UserContext = React.createContext({user: {}, events: [], updateSch: () => {}, updateProp: () => {}});
export default UserContext;