import React from "react";
import PropTypes from "prop-types";

class Comment extends React.Component {
    constructor(props) {
        super(props);
        this.state = { };
    }

    componentDidMount() {
        const { url, text, lognameOwnsThis } = this.props;
        fetch(url, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            // .then((data) => {
            //     this.setState({
            //         likes: data.likes,
            //         liked: data.liked,
            //     });
            // })
            .catch((error) => console.log(error));
    }

    render() {
        const { } = this.state;
        return (
            <button className="like-unlike-button" type="submit">
                FIXME-button-text-here
            </button>
        );
    }
};

Comment.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Comment;