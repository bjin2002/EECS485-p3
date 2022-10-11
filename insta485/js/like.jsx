import React from "react";
import PropTypes from "prop-types";

// Implement Like component similar to Post component.
// It should display the number of likes
// and a button to like the post if the logged in user liked the post.
// If the logged in user didn't like the post, it should be a dislike button.
class Like extends React.Component {
    constructor(props) {
        super(props);
        this.state = { };
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

    render() {
        return (
            <button className="like-unlike-button" type="submit">
                FIXME-button-text-here
            </button>
        );
    }
};

Like.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Like;