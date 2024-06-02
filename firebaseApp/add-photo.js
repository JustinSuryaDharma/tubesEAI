const admin = require("firebase-admin");
const serviceAccount = require("./key.json");

// Initialize the app with a service account, granting admin privileges
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://fir-login-24502-default-rtdb.firebaseio.com"
});

// Reference to the database
const db = admin.database();

// Function to add a photo to the database
function addPhoto(cityName, photoUrl) {
  const ref = db.ref('photos/' + cityName);
  ref.set({
    photo_url: photoUrl
  }, (error) => {
    if (error) {
      console.error("Error adding photo: ", error);
    } else {
      console.log("Photo added successfully!");
    }
  });
}

// Example usage
addPhoto('Salatiga', 'https://bobobox.com/blog/wp-content//uploads/2021/02/1-4YaszxcTRv74YB2leJfaGw.jpeg');
