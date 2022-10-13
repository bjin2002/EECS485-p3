import React from "react";
import PropTypes from "prop-types";
import moment from "moment";

class Post extends React.Component {
    /* Display image and post owner of a single post
     */

    // Runs when an instance is created.
    constructor(props) {
        // Initialize mutable state
        super(props);
        this.state = {
            comments: [],
            comments_url: "",
            created: "",
            imgUrl: "",
            owner: "",
            ownerImgUrl: "",
            ownerShowUrl: "",
            postShowUrl: "",
            postid: 0,
            lognameLikesThis: false,
            likesUrl: "",
            numLikes: 0,
            buttonText: "",

        };
        this.handleLikeButton = this.handleLikeButton.bind(this);
        this.handleCommentKeyPress = this.handleCommentKeyPress.bind(this);
    }


    // handleComments() {

    // }

    // Runs when an instance is added to the DOM
    componentDidMount() {
        // This line automatically assigns this.props.url to the const variable url
        const { url } = this.props;

        // Call REST API to get the post's information
        fetch(url, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                // Update state with the post's information
                this.setState({
                    comments: data.comments,
                    comments_url: data.comments_url,
                    created: moment(data.created).fromNow(),
                    imgUrl: data.imgUrl,
                    owner: data.owner,
                    ownerImgUrl: data.ownerImgUrl,
                    ownerShowUrl: data.ownerShowUrl,
                    postShowUrl: data.postShowUrl,
                    postid: data.postid,
                    lognameLikesThis: data.likes.lognameLikesThis,
                    buttonText: data.likes.lognameLikesThis ? 'Unlike' : 'Like',
                    numLikes: data.likes.numLikes,
                    likesUrl: data.likes.url,
                });
            })
            .catch((error) => console.log(error));
    }

    // Handles the like button when clicked
    handleLikeButton() {
        // event prevent default
        event.preventDefault();


        console.log('like button clicked');
        const { postid, lognameLikesThis, numLikes, likesUrl, } = this.state;

        // if lognameLikesThis is true, set lognameLikesThis to false and subtract 1 from numLikes
        // else set lognameLikesThis to true and add 1 to numLikes
        if (lognameLikesThis) {
            console.log("unlike");
            console.log(likesUrl);

            fetch(likesUrl, { method: "DELETE", credentials: "same-origin", })
                .then((response) => {
                    // if response is not ok, throw an error
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    return response.text();
                })
                .then((data) => {
                    console.log('settingState');
                    // Update data for state after the like is removed
                    this.setState((prevState) => ({
                        lognameLikesThis: false,
                        numLikes: prevState.numLikes - 1,
                        likesUrl: "",
                        buttonText: "Like",
                    }));
                })
                .catch((error) => console.log(error));

        }
        else {
            console.log("like");
            console.log(likesUrl);

            fetch(`/api/v1/likes/?postid=${postid}`, { method: "POST", credentials: "same-origin" })
                .then((response) => {
                    // if response is not ok, throw an error
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    return response.json();
                })
                .then((data) => {
                    console.log('settingState');
                    // Update data for state after the like is added 
                    this.setState((prevState) => ({
                        lognameLikesThis: true,
                        numLikes: prevState.numLikes + 1,
                        buttonText: "Unlike",
                        likesUrl: data.url,
                    }));
                })
                .catch((error) => console.log(error));
        }
    }


    handleCommentKeyPress(event) {
        // event prevent default
        event.preventDefault();
        console.log("Key pressed: " + event.key);

        if (event.key === 'Enter') {
            console.log('enter key pressed');
            this.handleCreateComment(event);
        }
    };


    handleCreateComment(event) {
        // event prevent default
        event.preventDefault();
        
        const commentValue = document.getElementById('commentId').value;
        console.log(commentValue);
        
        // turn text from commentValue into a json object
        const commentJson = JSON.stringify({ comment: commentValue });
        console.log(commentJson);

        const { comments_url } = this.state;
        // make a fetch call to the comments_url
        fetch(comments_url, { method: "POST", credentials: "same-origin", body: commentJson, headers: { "Content-Type": "application/json" } })
            .then((response) => {
                // if response is not ok, throw an error
                if (!response.ok) {
                    throw Error(response.statusText);
                }
                return response.json();
            })
            .then((data) => {
                console.log('settingState');
                // Update data for state after the comment is added 
                this.setState({
                    comments: data.comments,
                });
            })
            .catch((error) => console.log(error));
    }

    // Returns HTML representing this component
    render() {
        console.log("rendering post");

        // This line automatically assigns this.state.imgUrl to the const variable imgUrl
        // and this.state.owner to the const variable owner
        // set the state of all the variables from setState
        const { comments, comments_url, created, imgUrl, likes, owner, ownerImgUrl,
            ownerShowUrl, postShowUrl, postid, lognameLikesThis, buttonText, numLikes, likesUrl } = this.state;
        

        // Render post image and post owner
        return (
            <div className="post">

                <div className="profilePic">
                    <a href={ownerShowUrl}>
                        <img src={ownerImgUrl} alt="profilePic" />
                        <p>{owner}</p>
                    </a>
                </div>

                <div className="postTime">
                    <a href={postShowUrl}>
                        <p>{created}</p>
                    </a>
                </div>

                <div className="postImage">
                    <img src={imgUrl} alt="postImage" />
                </div>

                <div className="postLikes">
                    <button onClick={this.handleLikeButton} className="like-unlike-button" type="submit">
                        {buttonText}
                    </button>
                    {/* if numLikes is equal to 1 print the number of likes with like, else print likes */}
                    {numLikes === 1 ? (
                        <p>{numLikes} like</p>
                    ) : (
                        <p>{numLikes} likes</p>
                    )}
                </div>

                <div className="postComments">
                 {/* for each comment in comments, create an html div with the comment owner and text */}
                    {comments.map((comment) => (
                        <div className="comment" key={comment.id}>
                            <a href={comment.ownerShowUrl}>
                                {comment.owner}
                            </a>
                            {comment.text}
                        </div>
                    ))}
                </div>

                <div className="createComment">
                    {/* create an input field that is submitted with the enter key and handled by handleCreateComment */}
                    <input id= "commentInput" type="text" onChange={event => setMessage(event.target.value)} onKeyDown={this.handleCommentKeyPress} />
                </div>

            </div>

        );
    }
}

Post.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Post;