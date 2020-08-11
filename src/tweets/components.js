import React, {useState, useEffect} from 'react';
import {Button, Form, Container, Row, Col} from 'react-bootstrap';
import {loadTweets} from '../lookup';


export const TweetsComponent = (props) => {
  const formControlRef = React.createRef();
  const handleSubmit = (e) => {
      e.preventDefault();
      console.log(formControlRef.current.value)
      formControlRef.current.value = ''
  }
  return (
    <Container className='col-8 border row-6 h-100 my-5 py-5'>
      <Form onSubmit={handleSubmit} className='py-4'>
        <Form.Control ref={formControlRef} required style={{height: '10rem'}} size='lg' placeholder='Write a Tweet...' as='textarea' >

        </Form.Control>
        <Button className='my-2 w-25 mt-3 float-right flex-row' type='submit' variant='primary' size='md'> Tweet </Button>
      </Form>
    </Container>
  )
}

export const TweetList = (props) => {
  const [tweets, setTweets] = useState([])

  useEffect(()=>{
    loadTweets((response, status)=>{
      if(status === 200) {
        setTweets(response)
      }
    })
  },[])
  return tweets.map(items => {
    return(
      <Tweet key={items.id} tweet={items} />
    )
  })

}



export function ActionButton (props) {
  const {tweet, action} = props
  const [likes, setLikes] = useState(tweet.likes ? tweet.likes: 0)
  const [userLiked, setUserLiked] = useState(tweet.userLiked ? true : false)
  const className = props.className ? props.className : 'btn btn-primary btn-sm';
  const display = action.type === 'like' ? (`${likes} ${action.display}`) : action.display
  const variant = action.type === 'retweet' ? 'success' : action.type === 'like' ? 'primary' : 'danger'

  const handleClick = (event) => {
    event.preventDefault();
    switch (action.type) {
      case 'like':
        if(userLiked) {
          setUserLiked(false);
          setLikes(likes - 1)
        }
        else {
          setUserLiked(true);
          setLikes(likes + 1)
        }
      break;
      default: console.log("what"); break;

    }
  }
  return (
      <Button variant={variant} onClick={handleClick} className={className} style={{marginRight: '2px'}}>
      {display}
      </Button>
  )
}

export function Tweet (props) {
  const {tweet} = props

  return (
    <Container fluid
      className='col-8 mx-auto col-md-8'
    >
      <Row className='my-5 py-5 border bg-dark text-light'>
        <Col>
          <h6 style={{fontStyle: 'verdana'}}>{tweet.id} - {tweet.content}</h6>
          <div className='btn btn-group'>
            <ActionButton tweet={tweet} action={{type: 'like', display: 'Likes'}}/>
            <ActionButton tweet={tweet} action={{type: 'retweet', display: 'Retweet'}}/>
          </div>
        </Col>
      </Row>
      {(tweet.parent !== null ) && (
        <Row className='my-5 py-5 border bg-dark text-light'>
          <Col>
            <h6 style={{fontStyle: 'verdana'}}>{tweet.parent.id} - {tweet.parent.content}</h6>
          </Col>
        </Row>
      )}
    </Container>
  )
}
