import {backendLookup} from '../lookup'


export function apiPostCreate(newPost, callback) {
    backendLookup("POST", "/posts/create/", callback, {content: newPost})
  }

export function apiPostAction(postId, action, callback) {
    const data = {id: postId, action: action}
    backendLookup("POST", "/posts/action/", callback, data)
  }
  
export function apiPostList(callback) {
    backendLookup("GET", "/posts/", callback)
  }