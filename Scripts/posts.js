/**
 * This file will be a general class to build post elements and add them to the DOM
 */

//Define constants needed

//this will be the spot to append all posts to
//there will probably end up being a sub-container of main-content, which will allow us to
//add a column of other stuff off to the side, like making a post
const POSTS_CONTAINER = document.getElementsByClassName("main-content")[0]

//this hopefully will not remain a constant
//eventually I'd like to have this set dynamically by the user, and the page would follow that value
const POSTS_PER_PAGE = 5

/**
 * A class to handle posts that will appear in the feed
 */
class Post {
    //post stuff will go here
    image = "../Images/eat-up-high-resolution-logo-white-transparent.png"
    comments = {1: "this", 2: "is", 3: "Sparta"};

    /**
     * Creates a post element, based off of data passed in from the database
     */
    createPost() {
        //this will be the element that will be appended to POST_CONTAINER
        let postContainer = document.createElement("div");

        //if the image is not empty, create an image element and append it.
        //eventually we may do something completely different with posts with no images,
        //but for now, it will just be a post with no images
        if (this.image) {
            let imageEl = document.createElement("img");
            imageEl.src = this.image //this is probably wrong, but I need to do something
            imageEl.width = 300;
            imageEl.height = 300;
            postContainer.append(imageEl)
        }

        //check if there are comments, if so, create and append the comment element
        if (this.image) {
            for (const property in this.comments) {
                let commentEl = document.createElement("p");
                let curComment = this.comments[property]
                commentEl.innerHTML = curComment;
                postContainer.append(commentEl)
            }
        }

        postContainer.classList.add("post")

        //add the post to the DOM
        POSTS_CONTAINER.append(postContainer)
    }
}

//here I'll be using the Post class to create and append Post elements to the DOM
const onMounted = () => {
    //attempt to create a tag and add it to the container
    for (let i = 0; i < POSTS_PER_PAGE; i++) {
        let post = new Post();
        post.createPost();
    }
};

window.addEventListener("DOMContentLoaded", onMounted)