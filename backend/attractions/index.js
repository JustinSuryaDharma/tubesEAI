const express = require('express');
const app = express();
const PORT = 5000;

app.listen(
  PORT,
  () => console.log(`It's alive on http://localhost:${PORT}`)
)

app.use(express.json())

app.get('/attractions', (req, res) => {
  res.status(200).send({
    "id": 1,
    "name": "Benteng Takeshi",
    "description": "Benteng Takeshi merupakan salah satu landmark sejarah yang mempesona di kota Salatiga. Bangunan ini menyimpan kekayaan sejarah dan memperkaya keindahan kota ini dengan keberadaannya. Dibangun pada era kolonial Jepang, Benteng Takeshi menjadi saksi bisu perjalanan waktu dan kejadian bersejarah. Melalui penjelajahan yang mendalam di dalamnya, pengunjung dapat merasakan aura sejarah yang kuat dan mendapatkan pemahaman yang lebih dalam tentang masa lalu kota ini.",
    "type": "Landmark Sejarah",
    "location": "Salatiga, Indonesia",
    "rating": 4.7,
    "imageUrl": "https://cdns.klimg.com/merdeka.com/i/w/news/2022/03/31/1422273/content_images/670x335/20220331155329-1-tayangan-penuh-kenangan-ini-fakta-program-benteng-takeshi-yang-akan-comeback-di-2023-001-denny-marhendri.jpg"
  })
});

app.post('/attractions/:id', (req, res) => {
  const { id } = req.params;
  const { name, description, type, location, rating, imageUrl } = req.body;

  console.log("Received data:");
  console.log("ID:", id);
  console.log("Name:", name);
  console.log("Description:", description);
  console.log("Type:", type);
  console.log("Location:", location);
  console.log("Rating:", rating);
  console.log("Image URL:", imageUrl);

  res.status(200).json({ message: "Attraction updated successfully" });
})