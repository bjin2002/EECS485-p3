import React from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

class feed extends React.Component {
  /* Display image and post owner of a single post
   */

  // Runs when an instance is created.
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { next: "", results: [] };

    this.handleInfinteScroll = this.handleInfinteScroll.bind(this);
  }

  // Runs when an instance is added to the DOM
  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const url = "/api/v1/posts/";

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
        });
      })
      .catch((error) => console.log(error));
  }

  handleInfinteScroll() {
    // event.preventDefault();

    console.log("handleInfinteScroll");

    // This line automatically assigns this.props.url to the const variable url
    const { next } = this.state;

    // Call REST API to get the post's information
    fetch(next, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // Update state with the post's information
        this.setState((prevState) => ({
          next: data.next,
          results: prevState.results.concat(data.results),
        }));
      })
      .catch((error) => console.log(error));
  }

  // Returns HTML representing this component
  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    // set the state of all the variables from setState
    const { next, results } = this.state;

    // Render post image and post owner
    return (
      <InfiniteScroll
        dataLength={results.length}
        next={this.handleInfinteScroll}
        hasMore={next !== null}
        loader={<h4>Loading...</h4>}
        endMessage={
          <p style={{ textAlign: "center" }}>
            <b>Yay! You have seen all of the posts</b>
          </p>
        }
      >
        {/* 1. For each post in results, render a post component
                This is where infinite scroll componenet will go */}
        <div className="pagination">
          {results.map((post) => (
            <Post url={post.url} key={post.postid} />
          ))}
        </div>
      </InfiniteScroll>
    );
  }
}

export default feed;
