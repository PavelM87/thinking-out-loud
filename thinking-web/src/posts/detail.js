import React, {useState} from 'react'
import {ActionBtn} from './buttons'

export function ParentPost(props) {
    const {post} = props
    return post.parent ? <div className='row'>
    <div className='col-11 mx-auto p-3 border rounded'>
    <p className='mb-0 text-muted small'>Repost</p>
    <Post hideActions className={' '} post={post.parent}/>
    </div>
    </div> : null
  }
  export function Post(props) {
      const {post, didRepost, hideActions} = props
      const [actionPost, setActionPost] = useState(props.post ? props.post : null)
      const className = props.className ? props.className : 'col-10 mx-auto, col-md-6'
  
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
        <div>
          <p>{post.id} - {post.content}</p>
          <ParentPost post={post} />
        </div>
        {(actionPost && hideActions !== true) && <div className='btn btn-group'>
          <ActionBtn post={actionPost} didPerformAction={handlePerformAction} action={{type: "like", display:"Likes"}}/>
          <ActionBtn post={actionPost} didPerformAction={handlePerformAction} action={{type: "unlike", display:"Unlikes"}}/>
          <ActionBtn post={actionPost} didPerformAction={handlePerformAction} action={{type: "repost", display:"Repost"}}/>
        </div>}
      </div>
  }