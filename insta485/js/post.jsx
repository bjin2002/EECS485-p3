import React from "react";
import PropTypes from "prop-types";
import Like from "./like";
import Comment from "./comment"

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
            likes: [],
            owner: "",
            ownerImgUrl: "",
            ownerShowUrl: "",
            postShowUrl: "",
            postid: 0
        };
    }

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
                    created: data.created,
                    imgUrl: data.imgUrl,
                    likes: data.likes,
                    owner: data.owner,
                    ownerImgUrl: data.ownerImgUrl,
                    ownerShowUrl: data.ownerShowUrl,
                    postShowUrl: data.postShowUrl,
                    postid: data.postid
                });
            })
            .catch((error) => console.log(error));
    }

    // Returns HTML representing this component
    render() {
        // This line automatically assigns this.state.imgUrl to the const variable imgUrl
        // and this.state.owner to the const variable owner
        // set the state of all the variables from setState
        const { comments, comments_url, created, imgUrl, likes, owner, ownerImgUrl,
            ownerShowUrl, postShowUrl, postid } = this.state;

        // Render post image and post owner
        return (
            <div className="post">
                <img src={imgUrl} alt="post_image" />
                <p>{owner}</p>

                {/* Make a call to the like component */}
                <Like likes={likes} />

                {/* for each comment in comments, render a comment component, passing in comment.url, comment.text, and comment.lognameOwnsThis */}
                {comments.map((comment) => (
                    <Comment url={comment.url} text={comment.text} lognameOwnsThis={comment.lognameOwnsThis} />
                ))}


            </div>
        );
    }
}

Post.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Post;