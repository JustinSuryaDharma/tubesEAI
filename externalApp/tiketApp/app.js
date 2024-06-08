const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const mysql = require('mysql');
const PORT = 3001;
const cors = require('cors');
app.use(cors());

// Menyiapkan koneksi ke database
const connection = mysql.createConnection({
  host: 'mysql-3cd749a3-student-243e.a.aivencloud.com',
  user: 'avnadmin',
  password: 'AVNS__5WPvHLIhgZcPkJKJI6',
  port: '24602',
  database: 'UTS_EAI',
  connectTimeout: 10000,
});

// Membuat koneksi ke database
connection.connect(err => {
  if (err) {
    console.error('Error connecting to database:', err);
    return;
  }
  console.log('Connected to database');
});

// Menyiapkan middleware untuk parsing body dari request
app.use(bodyParser.json());

// Mendapatkan semua tiket
app.get('/tiket', (req, res) => {
  connection.query('SELECT * FROM tiket', (error, results) => {
    if (error) {
      console.error('Error executing query:', error);
      res.status(500).send('Internal Server Error');
      return;
    }
    res.json(results);
  });
});

// Mendapatkan tiket berdasarkan ID
app.get('/tiket/:id', (req, res) => {
  const id = req.params.id;
  connection.query('SELECT * FROM tiket WHERE id = ?', id, (error, results) => {
    if (error) {
      console.error('Error executing query:', error);
      res.status(500).send('Internal Server Error');
      return;
    }
    if (results.length === 0) {
      res.status(404).send('Tiket tidak ditemukan');
    } else {
      res.json(results[0]);
    }
  });
});

// Membeli tiket berdasarkan ID
app.post('/tiket/beli/:id', (req, res) => {
  const id = req.params.id;
  const { jumlah, nama, nik, email } = req.body; // Menambahkan parameter tambahan

  connection.query(
    'SELECT stock FROM tiket WHERE id = ?',
    id,
    (error, results) => {
      if (error) {
        console.error('Error executing query:', error);
        res.status(500).send('Internal Server Error');
        return;
      }
      if (results.length === 0) {
        res.status(404).send('Tiket tidak ditemukan');
        return;
      }

      const stock = results[0].stock;
      if (stock < jumlah) {
        res.status(400).send('Stock tidak cukup');
        return;
      }

      const stockBaru = stock - jumlah;
      connection.query(
        'UPDATE tiket SET stock = ? WHERE id = ?',
        [stockBaru, id],
        (updateError, updateResults) => {
          if (updateError) {
            console.error('Error executing update query:', updateError);
            res.status(500).send('Internal Server Error');
            return;
          }

          // Menyimpan data pembelian ke tabel pembelian
          const insertQuery =
            'INSERT INTO pembelian (tiket_id, nama_pemesan, nik, email, jumlah) VALUES (?, ?, ?, ?, ?)';
          connection.query(
            insertQuery,
            [id, nama, nik, email, jumlah],
            (insertError, insertResults) => {
              if (insertError) {
                console.error('Error executing insert query:', insertError);
                res.status(500).send('Internal Server Error');
                return;
              }
              res.send('Pembelian tiket berhasil');
            }
          );
        }
      );
    }
  );
});

// Menambahkan tiket baru
app.post('/tiket', (req, res) => {
  const {
    nama_wisata,
    open,
    close,
    kota,
    provinsi,
    negara,
    harga,
    stock,
    image,
  } = req.body;
  const query =
    'INSERT INTO tiket (nama_wisata, open, close, kota, provinsi, negara, harga, stock, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)';
  connection.query(
    query,
    [nama_wisata, open, close, kota, provinsi, negara, harga, stock, image],
    (error, results) => {
      if (error) {
        console.error('Error executing insert query:', error);
        res.status(500).send('Internal Server Error');
        return;
      }
      res.status(201).send('Tiket berhasil ditambahkan');
    }
  );
});

// Mencari tiket berdasarkan nama wisata dan lokasi
app.get('/tiket/search', (req, res) => {
  const { nama_wisata, kota, provinsi, negara, lokasi } = req.query;
  let query = 'SELECT * FROM tiket WHERE nama_wisata LIKE ?';
  let params = [`%${nama_wisata}%`];

  if (kota) {
    query += ' AND kota LIKE ?';
    params.push(`%${kota}%`);
  }
  if (provinsi) {
    query += ' AND provinsi LIKE ?';
    params.push(`%${provinsi}%`);
  }
  if (negara) {
    query += ' AND negara LIKE ?';
    params.push(`%${negara}%`);
  }
  if (lokasi) {
    query += ' AND lokasi LIKE ?';
    params.push(`%${lokasi}%`);
  }

  connection.query(query, params, (error, results) => {
    if (error) {
      console.error('Error executing search query:', error);
      res.status(500).send('Internal Server Error');
      return;
    }
    if (results.length === 0) {
      res.status(404).send('Tidak ada tiket yang ditemukan');
    } else {
      res.json(results);
    }
  });
});

// Memperbarui tiket berdasarkan ID
app.put('/tiket/:id', (req, res) => {
  const id = req.params.id;
  const {
    nama_wisata,
    open,
    close,
    kota,
    provinsi,
    negara,
    harga,
    stock,
    image,
  } = req.body;

  const query =
    'UPDATE tiket SET nama_wisata = ?, open = ?, close = ?, kota = ?, provinsi = ?, negara = ?, harga = ?, stock = ?, image = ? WHERE id = ?';
  connection.query(
    query,
    [nama_wisata, open, close, kota, provinsi, negara, harga, stock, image, id],
    (error, results) => {
      if (error) {
        console.error('Error executing update query:', error);
        res.status(500).send('Internal Server Error');
        return;
      }
      if (results.affectedRows === 0) {
        res.status(404).send('Tiket tidak ditemukan');
      } else {
        res.send('Perubahan tiket berhasil');
      }
    }
  );
});

// Menghapus tiket berdasarkan ID
app.delete('/tiket/:id', (req, res) => {
  const id = req.params.id;

  connection.query('DELETE FROM tiket WHERE id = ?', id, (error, results) => {
    if (error) {
      console.error('Error executing delete query:', error);
      res.status(500).send('Internal Server Error');
      return;
    }
    if (results.affectedRows === 0) {
      res.status(404).send('Tiket tidak ditemukan');
    } else {
      res.send('Penghapusan tiket berhasil');
    }
  });
});

// Mendapatkan tiket berdasarkan lokasi
app.get('/lokasi/:kota', (req, res) => {
  const kota = req.params.kota;
  connection.query(
    'SELECT * FROM tiket WHERE kota = ?',
    [kota],
    (error, results) => {
      if (error) {
        console.error('Error executing query:', error);
        res.status(500).send('Internal Server Error');
        return;
      }
      if (results.length === 0) {
        res.status(404).send('Tiket tidak ditemukan');
      } else {
        res.json(results); // Return the entire array of results
      }
    }
  );
});

// // Memperbarui tiket berdasarkan lokasi
// app.put('/lokasi/:lokasi', (req, res) => {
//     const location = req.params.lokasi;
//     const { nama_wisata, open, close, lokasi, harga, stock, image } = req.body;

//     const query = 'UPDATE tiket SET nama_wisata = ?, open = ?, close = ?, lokasi = ?, harga = ?, stock = ?, image = ? WHERE lokasi = ?';
//     connection.query(query, [nama_wisata, open, close, lokasi, harga, stock, image, location], (error, results) => {
//         if (error) {
//             console.error('Error executing update query:', error);
//             res.status(500).send('Internal Server Error');
//             return;
//         }
//         if (results.affectedRows === 0) {
//             res.status(404).send('Tiket tidak ditemukan');
//         } else {
//             res.send('Perubahan tiket berhasil');
//         }
//     });
// });

// Mendapatkan tiket berdasarkan nama_wisata
app.get('/tiket/nama/:nama_wisata', (req, res) => {
  const namaWisata = req.params.nama_wisata;
  connection.query(
    'SELECT * FROM tiket WHERE nama_wisata = ?',
    [namaWisata],
    (error, results) => {
      if (error) {
        console.error('Error executing query:', error);
        res.status(500).send('Internal Server Error');
        return;
      }
      if (results.length === 0) {
        res.status(404).send('Tiket tidak ditemukan');
      } else {
        res.json(results);
      }
    }
  );
});

// Membeli tiket berdasarkan lokasi
app.post('/tiket/beli/nama/:nama_wisata', (req, res) => {
  const namaWisata = req.params.nama_wisata;
  const jumlahBeli = req.body.jumlah;

  connection.query(
    'SELECT stock FROM tiket WHERE nama_wisata = ?',
    namaWisata,
    (error, results) => {
      if (error) {
        console.error('Error executing query:', error);
        res.status(500).send('Internal Server Error');
        return;
      }
      if (results.length === 0) {
        res.status(404).send('Tiket tidak ditemukan');
        return;
      }

      const stock = results[0].stock;
      if (stock < jumlahBeli) {
        res.status(400).send('stock tidak cukup');
        return;
      }

      const stockBaru = stock - jumlahBeli;
      connection.query(
        'UPDATE tiket SET stock = ? WHERE nama_wisata = ?',
        [stockBaru, namaWisata],
        (updateError, updateResults) => {
          if (updateError) {
            console.error('Error executing update query:', updateError);
            res.status(500).send('Internal Server Error');
            return;
          }
          res.send('Pembelian tiket berhasil');
        }
      );
    }
  );
});

// Menjalankan server pada port 3000
app.listen(PORT, '0.0.0.0', () => {
  console.log(`http://localhost:${PORT}/tiket`);
});
