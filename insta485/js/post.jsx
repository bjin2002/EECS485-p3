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

    handleLikeButton() {
        // event prevent default
        event.preventDefault();

        const { postid, lognameLikesThis, numLikes, likesUrl } = this.state;

        // if lognameLikesThis is true, set lognameLikesThis to false and subtract 1 from numLikes
        // else set lognameLikesThis to true and add 1 to numLikes
        if (lognameLikesThis) {
            console.log("unlike");

            fetch(likesUrl, { credentials: "same-origin" })
                .then((response) => {
                    // if response is not ok, throw an error
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    return response;
                })
                .then(() => {
                    // Update data for state after the like is removed
                    this.setState({
                        lognameLikesThis: false,
                        numLikes: numLikes - 1,
                        likesUrl: "",
                        buttonText: "Like"
                    });
                })
                
        }
        else {
            console.log("like");

            fetch(likesUrl, { credentials: "same-origin" })
                .then((response) => {
                    // if response is not ok, throw an error
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    return response;
                })
                .then(() => {
                    // Update data for state after the like is added 
                    this.setState({
                        lognameLikesThis: true,
                        numLikes: numLikes + 1,
                        likesUrl: `/api/v1/likes/?postid=${postid}`,
                        buttonText: "Unlike"
                    });
                })

        }

        // fetch the likesUrl and set credentials to same-origin


    }

    // Returns HTML representing this component
    render() {
        // This line automatically assigns this.state.imgUrl to the const variable imgUrl
        // and this.state.owner to the const variable owner
        // set the state of all the variables from setState
        const { comments, comments_url, created, imgUrl, likes, owner, ownerImgUrl,
            ownerShowUrl, postShowUrl, postid, lognameLikesThis, buttonText, numLikes, likesUrl } = this.state;

        // Render post image and post owner
        return (

            // /* for each comment in comments, render a comment component, passing in
            //          comment.url, comment.text, and comment.lognameOwnsThis */


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

                {/* <div className="postComments">
                    {}
                </div> */}

            </div>
        );
    }
}

Post.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Post;