import React from "react";
import PropTypes from "prop-types";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

class feed extends React.Component {
    /* Display image and post owner of a single post
     */

    // Runs when an instance is created.
    constructor(props) {
        // Initialize mutable state
        super(props);
        this.state = { next: "", results: [], url: "/api/v1/posts/" };
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
                    next: data.next,
                    results: data.results,
                    url: data.url
                });
            })
            .catch((error) => console.log(error));
    }

    // Returns HTML representing this component
    render() {
        // This line automatically assigns this.state.imgUrl to the const variable imgUrl
        // and this.state.owner to the const variable owner
        // set the state of all the variables from setState
        const { next, results, url} = this.state;

        // Render post image and post owner
        return (
            <InfiniteScroll>
                // data length
                //next
                //has more posts (if next is blank)
                //loader
                //end message

            </InfiniteScroll>

            // For each post in results, render a post component
            <div className="pagination" >
                {/* {results.map((post) => (
                    <Post url={post.url} />
                ))} */}
                {next}
                {results}
                {url}
            </div>

            // Do something with infinite scroll and next (?).... TODO

        );
    }
}

feed.propTypes = {
    url: PropTypes.string.isRequired,
};

export default feed;