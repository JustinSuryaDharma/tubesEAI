const admin = require('firebase-admin');
const serviceAccount = require('./key.json');

// Initialize the app with a service account, granting admin privileges
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://fir-login-24502-default-rtdb.firebaseio.com',
});

// Reference to the database
const db = admin.database();

// Function to add an attraction to the database
function addAttraction(
  id,
  name,
  description,
  imageUrl,
  location,
  rating,
  type
) {
  const ref = db.ref('attractions/' + id);
  ref.set(
    {
      name: name,
      description: description,
      imageUrl: imageUrl,
      location: location,
      rating: rating,
      type: type,
    },
    error => {
      if (error) {
        console.error('Error adding attraction: ', error);
      } else {
        console.log('Attraction added successfully!');
      }
    }
  );
}

// Adding Danau Podomoro
addAttraction(
  9,
  'Oox Guitar Maker',
  'Oox Guitar Maker adalah bengkel pembuat gitar terkenal di Afrika yang telah beroperasi selama lebih dari 20 tahun. Dikenal dengan keahliannya dalam menciptakan gitar akustik dan elektrik yang berkualitas tinggi, Oox Guitar Maker menarik musisi dari seluruh dunia. Setiap gitar dibuat dengan tangan menggunakan bahan-bahan terbaik dan melalui proses yang teliti untuk memastikan suara dan daya tahan yang sempurna. Pengunjung dapat melihat langsung proses pembuatan gitar dan bahkan memesan gitar kustom sesuai keinginan mereka.',
  'https://asset-2.tstatic.net/tribunnews/foto/bank/images/slamet-joko-43-alias-ook-pemilik-oox-guitarmaker.jpg',
  'Ambarawa',
  4.9,
  'Craftsmanship'
);
