import React from 'react';
import './App.css';
import Layout from './components/Layout';

import {TweetList, TweetsComponent} from './tweets'


function App() {

  return (
    <div>
      <Layout>
        <TweetsComponent />
        <TweetList />
      </Layout>
    </div>
  );
}

export default App;
