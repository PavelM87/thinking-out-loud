import React, {useState} from 'react'
import {ActionBtn} from './buttons'

export function ParentPost(props) {
    const {post} = props
    return post.parent ? <Post isRepost reposter={props.reposter} hideActions className={' '} post={post.parent} /> : null
  }
  export function Post(props) {
      const {post, didRepost, hideActions, isRepost, reposter} = props
      const [actionPost, setActionPost] = useState(props.post ? props.post : null)
      let className = props.className ? props.className : 'col-10 mx-auto, col-md-6'
      className = isRepost === true ? `${className} p-2 border rounded` : className
      const path = window.location.pathname
      const match = path.match(/(?<postid>\d+)/)
      const urlPostId = match ? match.groups.postid : -1
      const isDetail = `${post.id}` === `${urlPostId}`
      const handleLink = (event) => {
          event.preventDefault()
          window.location.href = `/${post.id}`
      }
      const handlePerformAction = (newActionPost, status) => {
        if (status === 200) {
        setActionPost(newActionPost)
        } else if (status === 201) {
          if (didRepost) {
            didRepost(newActionPost)
          }
        }
      }
  
      return <div className={className}>
        {isRepost === true && <div className='mb-2'><span className='small text-muted'>Repost via @{reposter.username}</span></div>}
        <div className='d-flex'>
        <div className=''>
          <span className='mx-1 px-3 py-2 rounded-circle bg-warning text-white'>
            {post.user.username[0]}
          </span>
        </div>
        <div className='col-11'>
        <div>
          <p>{post.user.first_name}{" "}
              {post.user.last_name}{" "}
              @{post.user.username}</p>
          <p>{post.id} - {post.content}</p>
          <ParentPost post={post} reposter={post.user}/>
        </div>
        <div className='btn btn-group px-0'>
        {(actionPost && hideActions !== true) && <React.Fragment>
          <ActionBtn post={actionPost} didPerformAction={handlePerformAction} action={{type: "like", display:"Нравится"}}/>
          <ActionBtn post={actionPost} didPerformAction={handlePerformAction} action={{type: "unlike", display:"Ненравится"}}/>
          <ActionBtn post={actionPost} didPerformAction={handlePerformAction} action={{type: "repost", display:"Поделиться"}}/>
        </React.Fragment>}
          {isDetail === true ? null : <button className="btn btn-outline-primary btn-sm" onClick={handleLink}>Просмотр</button>}
        </div>
        </div>
        </div>
      </div>
  }