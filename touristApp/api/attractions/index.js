const express = require('express');
const app = express();
const PORT = 3000;
var admin = require('firebase-admin');
const serviceAccount = require('./key.json');

// init app and credential
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://fir-login-24502-default-rtdb.firebaseio.com',
});

const db = admin.database();

// middleware json
app.use(express.json());

// get all
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

// post and put
app.post('/attractions/:id', (req, res) => {
  const { id } = req.params;
  const { name, description, type, location, rating, imageUrl } = req.body;

  const attractionRef = db.ref(`/attractions/${id}`);

  attractionRef.update(
    {
      name: name,
      description: description,
      type: type,
      location: location,
      rating: rating,
      imageUrl: imageUrl,
    },
    error => {
      if (error) {
        console.error('Error updating attraction:', error);
        res.status(500).json({ error: 'Error updating attraction' });
      } else {
        console.log('Attraction updated successfully');
        res.status(200).json({ message: 'Attraction updated successfully' });
      }
    }
  );
});

// delete
app.delete('/attractions/:id', (req, res) => {
  const { id } = req.params;

  const attractionRef = db.ref(`/attractions/${id}`);

  attractionRef
    .remove()
    .then(() => {
      console.log('Attraction deleted successfully');
      res.status(200).json({ message: 'Attraction deleted successfully' });
    })
    .catch(error => {
      console.error('Error deleting attraction:', error);
      res.status(500).json({ error: 'Error deleting attraction' });
    });
});

// filtered get
app.get('/filterattractions', (req, res) => {
  const location = req.query.location;

  if (location) {
    db.ref('/attractions')
      .orderByChild('location')
      .equalTo(location)
      .once('value', snapshot => {
        const attractions = [];
        snapshot.forEach(childSnapshot => {
          const attractionId = childSnapshot.key;
          const attractionData = childSnapshot.val();
          attractions.push({ id: attractionId, ...attractionData });
        });
        res.status(200).json(attractions);
      });
  } else {
    db.ref('/attractions').once('value', snapshot => {
      const attractions = [];
      snapshot.forEach(childSnapshot => {
        const attractionId = childSnapshot.key;
        const attractionData = childSnapshot.val();
        attractions.push({ id: attractionId, ...attractionData });
      });
      res.status(200).json(attractions);
    });
  }
});

// filtered get by name
app.get('/nameattractions', (req, res) => {
  const name = req.query.name;

  if (name) {
    db.ref('/attractions')
      .orderByChild('name')
      .equalTo(name)
      .once('value', snapshot => {
        const attractions = [];
        snapshot.forEach(childSnapshot => {
          const attractionId = childSnapshot.key;
          const attractionData = childSnapshot.val();
          attractions.push({ id: attractionId, ...attractionData });
        });
        res.status(200).json(attractions);
      });
  } else {
    // If no name query parameter is provided, return all attractions
    db.ref('/attractions').once('value', snapshot => {
      const attractions = [];
      snapshot.forEach(childSnapshot => {
        const attractionId = childSnapshot.key;
        const attractionData = childSnapshot.val();
        attractions.push({ id: attractionId, ...attractionData });
      });
      res.status(200).json(attractions);
    });
  }
});

// app server
app.listen(PORT, () => console.log(`It's alive on http://localhost:${PORT}`));
