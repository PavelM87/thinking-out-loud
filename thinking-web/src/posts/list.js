import React, {useEffect, useState} from 'react'
import {apiPostList} from './lookup'
import {Post} from './detail'

export function PostsList(props) {
    const [postsInit, setPostsInit] = useState([])
    const [posts, setPosts] = useState([])
    const [postsDidSet, setPostsDidSet] = useState(false)
    useEffect(()=>{
      let final = [...props.newPosts].concat(postsInit)
      if (final.length !== posts.length) {
        setPosts(final)
      }
    }, [props.newPosts, posts, postsInit])

    useEffect(() => {
      if (postsDidSet === false) {
        const handlePostListLookup = (response, status) => {
          if (status === 200){
            setPostsInit(response)
            setPostsDidSet(true)
          } else {
            alert("Ошибка же")
          }
        }
        apiPostList(props.username, handlePostListLookup)
      }
      }, [postsInit, postsDidSet, setPostsDidSet, props.username])
      const handleDidRepost = (newPost) => {
        const updatePostsInit = [...postsInit]
        updatePostsInit.unshift(newPost)
        setPostsInit(updatePostsInit)
        const updateFinalPosts = [...posts]
        updateFinalPosts.unshift(posts)
        setPosts(updateFinalPosts)
      }
      return posts.map((post, index)=>{
        return <Post 
        post={post} 
        didRepost = {handleDidRepost}
        className='my-5 py-5 border bg-white text-dark' 
        key={`${index}-{item.id}`}/>
      })
  }