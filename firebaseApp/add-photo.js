const admin = require('firebase-admin');
const serviceAccount = require('./key.json');

// Initialize the app with a service account, granting admin privileges
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://fir-login-24502-default-rtdb.firebaseio.com',
});

// Reference to the database
const db = admin.database();

// Function to add a photo to the database
function addPhoto(cityName, photoUrl) {
  const ref = db.ref('photos/' + cityName);
  ref.set(
    {
      photo_url: photoUrl,
    },
    error => {
      if (error) {
        console.error('Error adding photo: ', error);
      } else {
        console.log('Photo added successfully!');
      }
    }
  );
}

// Example usage
addPhoto(
  'Bandung',
  'https://api2.kemenparekraf.go.id/storage/app/uploads/public/65e/534/608/65e5346086f1a976234330.jpg'
);
addPhoto(
  'Africa',
  'https://awsimages.detik.net.id/community/media/visual/2022/01/31/samara-private-game-reserve-3.jpeg?w=1200'
);
