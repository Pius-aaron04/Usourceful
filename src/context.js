// context.js
import React, { createContext, useState } from 'react';

const UserContext = createContext({
  count: 0,
  user: { name: '', email: '' }, // Example data object
  isLoggedIn: false,
  // racks: [],
  setValue: () => {}, // Update function
});

export default UserContext;