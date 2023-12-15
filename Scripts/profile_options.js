// script.js

const makeInteractive = () => {
    // Elements for the profile section
    const profileImage = document.getElementsByClassName('profile-image')[0];
    const profileOptions = document.getElementsByClassName('profile-options')[0];

    // ... (previous code)

    // Toggle profile options visibility on profile image click
    profileImage.addEventListener('click', () => {
       profileOptions.style.display = profileOptions.style.display === 'none' ? 'block' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', makeInteractive);

const sendToCreate = () => {
    //send the user to the create_account page
    window.location.assign("create_account.html")
}

const sendToLogin = () => {
    //send the user to the login page
    window.location.assign("login.html")
}