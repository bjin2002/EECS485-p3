import React from "react";
import PropTypes from "prop-types";

// Implement Like component similar to Post component.
// It should display the number of likes
// and a button to like the post if the logged in user liked the post.
// If the logged in user didn't like the post, it should be a dislike button.
class Like extends React.Component {
    constructor(props) {
        super(props);
        this.state = { buttonText: "" };
        this.handleClick.bind(this);
    }

    componentDidMount() {
        const { lognameLikesThis, numLikes, url } = this.props;
        fetch(url, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .catch((error) => console.log(error));
    }

    handleClick() {
        // if lognamLikesThis is true, then set buttonText to unlike
        const { lognameLikesThis, numLikes, url } = this.props;
        if (lognameLikesThis) {
            this.setState({ buttonText: "Unlike" });
            this.props.likeHandlerSetStateofParent(!this.props.lognameLikesThis,
                numLikes - 1,
                this.props.url);
        }
        // if lognameLikesThis is false, then like
        else {
            this.setState({ buttonText: "Like" });
            this.props.likeHandlerSetStateofParent(this.props.lognameLikesThis, this.props.numLikes, this.props.url);
        }


    }

    render() {
        return (

            <button onClick={this.handleClick} className="like-unlike-button" type="submit">
                {buttonText}
            </button>
        );
    }
};

Like.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Like;