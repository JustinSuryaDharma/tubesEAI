const express = require('express');
const app = express();
const PORT = 5000;
var admin = require("firebase-admin");
const serviceAccount = require("./key.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://fir-login-24502-default-rtdb.firebaseio.com",
});

const db = admin.database();

app.use(express.json())

app.get('/attractions', (req, res) => {
  db.ref('/attractions').once('value', snapshot => {
    const attractions = [];
    snapshot.forEach(childSnapshot => {
      const attractionId = childSnapshot.key;
      const attractionData = childSnapshot.val();
      attractions.push({ id: attractionId, ...attractionData });
    });
    res.status(200).json(attractions);
  });
});

app.post('/attractions/:id', (req, res) => {
  const { id } = req.params;
  const { name, description, type, location, rating, imageUrl } = req.body;

  const attractionRef = db.ref(`/attractions/${id}`);

  attractionRef.update({
    name: name,
    description: description,
    type: type,
    location: location,
    rating: rating,
    imageUrl: imageUrl
  }, (error) => {
    if (error) {
      console.error("Error updating attraction:", error);
      res.status(500).json({ error: "Error updating attraction" });
    } else {
      console.log("Attraction updated successfully");
      res.status(200).json({ message: "Attraction updated successfully" });
    }
  });
});




app.listen(
  PORT,
  () => console.log(`It's alive on http://localhost:${PORT}`)
)