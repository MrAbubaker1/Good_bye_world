// script.js

document.addEventListener('DOMContentLoaded', function () {
    const restaurantList = document.getElementById('restaurant-list');
    const selectedRestaurantName = document.getElementById('selected-restaurant-name');
    const selectedRestaurantDescription = document.getElementById('selected-restaurant-description');

   // Elements for the profile section
   const profileImage = document.getElementById('profile-image');
   const profileOptions = document.getElementById('profile-options');

   // ... (previous code)

   // Toggle profile options visibility on profile image click
   profileImage.addEventListener('click', () => {
       profileOptions.style.display = profileOptions.style.display === 'none' ? 'block' : 'none';
   });

    // Elements for the exploring options section
    const exploreBtn = document.getElementById('explore-btn');
    const exploringResult = document.getElementById('exploring-result');

    // Elements for the popular foods section
    const popularFoodsList = document.getElementById('popular-foods-list');

    // Selected restaurant data
    let selectedRestaurant = null;

    // Display selected restaurant
    function displaySelectedRestaurant(restaurant) {
        selectedRestaurant = restaurant;
        selectedRestaurantName.textContent = restaurant.name;
        selectedRestaurantDescription.textContent = restaurant.description;

        // Display profile information
        currentProfile.textContent = `Current Profile: ${restaurant.profile}`;

        // Display exploring options
        exploringResult.textContent = ''; // Clear previous results
        exploreBtn.addEventListener('click', exploreOptions);

        // Display popular foods
        popularFoodsList.innerHTML = restaurant.popularFoods.map(food => `<li>${food}</li>`).join('');
        popularFoodsList.addEventListener('click', viewPopularFoodDetails);
    }

    // Function to change the profile
    changeProfileBtn.addEventListener('click', () => {
        const newProfile = profileInput.value.trim();
        if (newProfile !== '') {
            selectedRestaurant.profile = newProfile;
            currentProfile.textContent = `Current Profile: ${newProfile}`;
            profileInput.value = ''; // Clear the input field
        }
    });

    // Function to explore options
    function exploreOptions() {
        // Add your logic for exploring options here
        const result = 'Exploration result goes here.';
        exploringResult.textContent = result;
    }

    // Function to view popular food details
    function viewPopularFoodDetails(event) {
        const clickedFood = event.target.textContent;
        // Add your logic to display details or perform other actions for the clicked food
        console.log(`User clicked on: ${clickedFood}`);
    }
});


    // Sample data (replace with your API call)
    const restaurants = [
        { id: 1, name: 'Restaurant 1', description: 'Description for Restaurant 1' },
        { id: 2, name: 'Restaurant 2', description: 'Description for Restaurant 2' },
        // Add more restaurants as needed
    ];

    // Populate restaurant list
    restaurants.forEach(restaurant => {
        const li = document.createElement('li');
        li.textContent = restaurant.name;
        li.addEventListener('click', () => displaySelectedRestaurant(restaurant));
        restaurantList.appendChild(li);
    });


    
// explore-script.js

document.addEventListener('DOMContentLoaded', function () {
    const foodList = document.getElementById('food-list');

    // Sample data (replace with your API call)
    const foodItems = [
        { id: 1, name: 'Food Item 1' },
        { id: 2, name: 'Food Item 2' },
        { id: 3, name: 'Food Item 3' },
        // Add more food items as needed
    ];

    // Populate food list
    foodItems.forEach(food => {
        const li = document.createElement('li');
        li.textContent = food.name;
        foodList.appendChild(li);
    });

    // Update link to Explore page
    const exploringOptionsSection = document.getElementById('exploring-options-section');
    exploringOptionsSection.innerHTML = `
        <h3>Exploring Options</h3>
        <a href="explore.html">Explore All Food Items</a>
    `;
});
