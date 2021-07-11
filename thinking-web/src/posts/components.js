import React, {useState} from 'react'
import {PostsList} from './list'
import {PostCreate} from './create'


export function PostsComponent(props) {
  const [newPosts, setNewPosts] = useState([])
  const canPost = props.canPost === "false" ? false : true
  const handleNewPost = (newPost) =>{
    let tempNewPosts = [...newPosts]
    tempNewPosts.unshift(newPost)
    setNewPosts(tempNewPosts)
  }
  return <div className={props.className}>
    {canPost === true && <PostCreate didPost={handleNewPost} className='col-12 mb-3' />}
    <PostsList newPosts={newPosts} {...props}/> 
  </div>
}
  
