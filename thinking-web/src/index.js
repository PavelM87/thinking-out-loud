import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { ProfileBadgeComponent } from './profiles/badge';
import {FeedComponent, PostsComponent, PostDetailComponent} from './posts';
import reportWebVitals from './reportWebVitals';


const appElement = document.getElementById('root')
if (appElement) {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    appElement
  );
}
const e = React.createElement

const postsEl = document.getElementById("thinking")
if (postsEl) { 
  ReactDOM.render(e(PostsComponent, postsEl.dataset), postsEl);
}

const postsFeedEl = document.getElementById("thinking-feed")
if (postsFeedEl) { 
  ReactDOM.render(e(FeedComponent, postsFeedEl.dataset), postsFeedEl);
}

const postDetailElements = document.querySelectorAll(".thinking-detail")

postDetailElements.forEach(container=> {
  ReactDOM.render(
    e(PostDetailComponent, container.dataset), container);
})

const userProfileBadgeElements = document.querySelectorAll(".thinking-profile-badge")

userProfileBadgeElements.forEach(container=> {
  ReactDOM.render(
    e(ProfileBadgeComponent, container.dataset), container);
})


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
