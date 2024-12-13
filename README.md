# PENJELASAN MENGENAI FP

| Name           | NRP        | Kelas     |
| ---            | ---        | ----------|
| Thalyta Vius Pramesti | 5025231055 | KKA F |
| Winda Nafiqih Irawan | 5025231065 | KKA F |
| Miskiyah | 5025231119 | KKA F |

# JUDUL FP : SKINFIT - TEMUKAN PERAWATAN KULIT YANG PAS UNTUKMU​

Deskripsi singkat : SkinFit: Temukan Perawatan Kulit yang Pas Untukmu adalah sebuah platform digital inovatif berbasis web yang dirancang untuk membantu pengguna menemukan produk skincare yang paling sesuai dengan kebutuhan dan kondisi kulit mereka. Dengan pendekatan yang personal, SkinFit memanfaatkan analisis data sederhana melalui tes kulit interaktif untuk mengenali jenis kulit, masalah yang dihadapi, seperti jerawat, penuaan dini, atau kekeringan, serta preferensi pengguna terhadap bahan-bahan tertentu dengan memadukan algoritma CSP (Constraint Satisfaction Problem) dan filtering

## Penjelasan kode `skinfit.py`

Pertama-tama yang dilakukan yaitu melakukan import library seperti library `flask` agar kode python bisa berjalan di web lalu `pandas` untuk membaca file csv, dan `problem` dari `constraint` untuk menyimpan constraint dari algoritma `csp` sendiri. <br>

```c
from flask import Flask, render_template, request // import flask untuk mengintegrasikan web dengan python sebagai back-end
import pandas as pd // import pandas untuk membaca file dataset dengan format csv
from constraint import Problem // untuk algoritma csp nya sendiri
```

Selanjutnya inisialisasi flask dan pembacaan file csv <br>

```c
app = Flask(__name__) // inisialisasi flask

// Load data CSV
data_path = 'dataskin.csv' // mengambil nama filenya
df = pd.read_csv(data_path, quotechar='"')  // mengabaikan tanda " karena hanya sebagai pembatas dan bukan bagiannya
```

Lalu selanjutnya menentukan kriteria filter data

```c
@app.route("/", methods=["GET", "POST"])
def home():
    filtered_data = []
    no_results_message = "" // mengambil jawaban dari WEB

    // Ingredients filter sesuai masalah kulit
    ingredients_filter = {
        "hiperpigmentasi": ["Vitamin C", "Ascorbic Acid", "Niacinamide", "Arbutin", "Licorice Extract", "Kojic Acid", "Glycolic Acid", "Salicylic Acid", "Lactic Acid", "Azelaic Acid", "Mulberry Extract", "Green Tea Extract", "Papaya Enzyme", "Retinoid", "Retinol", "Ceramides", "Hyaluronic Acid"],
        "jerawat": ["Salicylic Acid", "Benzoyl Peroxide", "Tea Tree Oil", "Niacinamide", "Zinc PCA", "Centella Asiatica", "Aloe Vera", "Ceramides", "Green Tea Extract", "Hyaluronic Acid", "Zinc Oxide", "Titanium Dioxide", "Vitamin E"],
        "kemerahan": ["Centella Asiatica", "Niacinamide", "Aloe Vera", "Green Tea Extract", "Chamomile Extract", "Panthenol", "Allantoin", "Licorice Extract", "Ceramides", "Calendula Extract", "Beta Glucan", "Bisabolol", "Zinc Oxide", "Vitamin E", "Squalane"],
        "garis_halus": ["Retinol", "Retinoid", "Peptides", "Hyaluronic Acid", "Vitamin C", "Niacinamide", "Bakuchiol", "Ceramides", "Collagen", "Coenzyme Q10 (CoQ10)", "Alpha Hydroxy Acids (AHA)", "Lactic Acid", "Glycolic Acid", "Squalane", "Panthenol", "Vitamin E"],
    } 

    // Filter bahan-bahan yang ingin dihindari (reaksi bahan)
    reaksi_bahan_filter = {
        "alkohol": ["Alcohol Denat", "Ethanol", "Methanol", "Isopropyl Alcohol", "SD Alcohol", 
                     "Cetyl Alcohol", "Stearyl Alcohol", "Cetearyl Alcohol", "Behenyl Alcohol", 
                     "Benzyl Alcohol", "Phenoxyethanol", "Lanolin Alcohol", "Propylene Glycol", 
                     "Butylene Glycol", "Glycerin"],
        "fragrance": ["Fragrance", "Parfum", "Limonene", "Linalool", "Citral", "Geraniol", 
                      "Eugenol", "Coumarin", "Benzyl Salicylate", "Hedione", "Benzyl Alcohol", 
                      "Alpha-Isomethyl Ionone", "Iso Eugenol", "Cinnamal", "Cinnamyl Alcohol", 
                      "Benzyl Cinnamate", "Hydroxycitronellal", "Amyl Cinnamal", "Linalool", 
                      "Methyl Eugenol"],
        "paraben": ["Methylparaben", "Ethylparaben", "Propylparaben", "Butylparaben", 
                    "Isobutylparaben", "Benzylparaben", "Sodium Methylparaben", "Sodium Ethylparaben", 
                    "Sodium Propylparaben", "Sodium Butylparaben"]
    }

    // Filter bahan-bahan untuk fungsi tambahan
    fungsi_tambahan_filter = {
        "anti_aging": ["Retinol", "Retinoid", "Peptides", "Hyaluronic Acid", "Vitamin C", "Niacinamide", 
                       "Alpha Hydroxy Acids (AHA)", "Glycolic Acid", "Lactic Acid", "Vitamin E", 
                       "Coenzyme Q10 (CoQ10)", "Ceramides", "Bakuchiol", "Collagen", "Squalane", 
                       "Green Tea Extract", "Panthenol", "Centella Asiatica", "Beta Glucan"],
        "brightening": ["Vitamin C", "Ascorbic Acid", "Niacinamide", "Arbutin", "Licorice Extract", "Kojic Acid", 
                        "Alpha Arbutin", "Glycolic Acid", "Lactic Acid", "Azelaic Acid", "Mulberry Extract", 
                        "Papaya Extract", "Tranexamic Acid", "Green Tea Extract", "Vitamin E", "Squalane", 
                        "Beta Glucan", "Hyaluronic Acid"],
        "acne_fighting": ["Salicylic Acid", "Benzoyl Peroxide", "Tea Tree Oil", "Niacinamide", "Zinc PCA", "Sulfur", 
                          "Centella Asiatica", "Aloe Vera", "Green Tea Extract", "Resorcinol", "Alpha Hydroxy Acids (AHA)", 
                          "Beta Hydroxy Acid (BHA)", "Retinol", "Retinoid", "Glycolic Acid", "Lactic Acid", "Clindamycin", 
                          "Dapsone", "Azelaic Acid", "Panthenol", "Ceramides", "Squalane"]
    }

    // Price filter ranges
    price_filter = {
        "under_50k": (0, 50000),
        "50_100k": (51000, 100000),
        "100_200k": (101000, 200000),
        "up_to_200k": (201000, 1000000)
    }
```

Lalu selanjutnya sudah masuk ke algoritma `csp`

```c
if request.method == "POST":
        try:
            // Salin DataFrame asli
            filtered_df = df.copy()

            // Ambil data dari form
            produk = request.form.get("produk")  # Kategori produk
            tipe_kulit = request.form.get("tipe_kulit")  # Jenis kulit
            masalah_kulit = request.form.getlist("masalah_kulit")  # Masalah kulit
            reaksi_bahan = request.form.getlist("reaksi_bahan")  # Reaksi terhadap bahan
            fungsi_tambahan = request.form.getlist("fungsi_tambahan")  # Fungsi tambahan
            harga = request.form.getlist("budget")  # budget

            // CSP Setup
            problem = Problem()

            // Variabel CSP
            problem.addVariable("Produk", filtered_df["Kategori"].unique())
            problem.addVariable("SkinType", filtered_df["SkinType"].unique())
            problem.addVariable("Ingredients", filtered_df["Ingredients"])
            problem.addVariable("Harga", filtered_df["Harga"].unique())

            // Constraints
            if produk:
                problem.addConstraint(lambda p: p.lower() == produk.lower(), ["Produk"])

            if tipe_kulit:
                if tipe_kulit.lower().strip() == "all skin type":
                    # Jika tipe kulit "All Skin Type", maka tampilkan produk yang sesuai dengan "All Skin Type"
                    problem.addConstraint(lambda s: s.strip().lower() == "all skin type", ["SkinType"])
                else:
                    # Untuk tipe kulit lain seperti "normal", "kering", "berminyak", "sensitif"
                    problem.addConstraint(lambda s: s.strip().lower() == tipe_kulit.lower(), ["SkinType"])


            if masalah_kulit:
                matched_ingredients = []
                for masalah in masalah_kulit:
                    matched_ingredients.extend(ingredients_filter.get(masalah, []))
                if matched_ingredients:
                    problem.addConstraint(
                        lambda i: any(ingredient.lower() in i.lower() for ingredient in matched_ingredients),
                        ["Ingredients"],
                    )

            if reaksi_bahan:
                for bahan in reaksi_bahan:
                    if bahan in reaksi_bahan_filter:
                        bahan_list = reaksi_bahan_filter[bahan]
                        problem.addConstraint(
                            lambda i: all(b not in i.lower() for b in bahan_list),
                            ["Ingredients"],
                        )

            if fungsi_tambahan:
                for fungsi in fungsi_tambahan:
                    if fungsi in fungsi_tambahan_filter:
                        fungsi_list = fungsi_tambahan_filter[fungsi]
                        problem.addConstraint(
                            lambda i: any(f.lower() in i.lower() for f in fungsi_list),
                            ["Ingredients"],
                        )

            // Rentang harga
            if "budget" in request.form:
                budget = request.form.get("budget")  # Rentang harga yang dipilih pengguna
                if budget and budget in price_filter:
                    min_price, max_price = price_filter[budget]
                    # Filter harga pada dataframe
                    filtered_df = filtered_df[(filtered_df["Harga"] >= min_price) & (filtered_df["Harga"] <= max_price)]
                else:
                    no_results_message = "Rentang harga tidak valid."

            filtered_df = filtered_df.sort_values(by="Harga", ascending=True)
            filtered_df["Harga"] = filtered_df["Harga"].apply(lambda x: f"Rp {x:,.0f}")

            // Cari solusi
            solutions = problem.getSolutions()

            // Cari solusi
            solutions = problem.getSolutions()

            // Filter DataFrame berdasarkan solusi
            if solutions:
                solution_ingredients = [sol["Ingredients"] for sol in solutions]
                filtered_df = filtered_df[filtered_df["Ingredients"].isin(solution_ingredients)]
                
                // Filter lebih lanjut berdasarkan kategori produk yang dipilih
                if produk:
                    filtered_df = filtered_df[filtered_df["Kategori"].str.lower() == produk.lower()]
                
                // Filter lebih lanjut berdasarkan tipe kulit yang dipilih
                if tipe_kulit:
                    if tipe_kulit == "All Skin Type":
                        # Jika tipe kulit "All Skin Type", tampilkan produk yang hanya memiliki "All Skin Type"
                        filtered_df = filtered_df[filtered_df["SkinType"].str.strip() == "All Skin Type"]
                    else:
                        # Untuk tipe kulit lain seperti "normal", "kering", "berminyak", "sensitif"
                        filtered_df = filtered_df[filtered_df["SkinType"].str.lower() == tipe_kulit.lower()]

                // Filter berdasarkan masalah kulit yang dipilih
                if masalah_kulit:
                    filtered_df = filtered_df[filtered_df["Ingredients"].apply(
                        lambda x: any(ingredient.lower() in x.lower() for ingredient in matched_ingredients)
                    )]

                // Cek apakah ada hasil setelah filter
                if filtered_df.empty:
                    no_results_message = "Produk tidak ditemukan berdasarkan kriteria yang dipilih."
                else:
                    # Convert filtered DataFrame to dictionary
                    filtered_data = filtered_df.to_dict(orient="records")

                // Debugging log jika tidak ada produk
                if not filtered_data:
                    print("No products found!")


        except Exception as e:
            print(f"Error: {e}")
            no_results_message = "Terjadi kesalahan saat memproses pencarian."

    return render_template("index.html", filtered_data=filtered_data, no_results_message=no_results_message)

if __name__ == "__main__":
    app.run(debug=True)
```

Begitu untuk kode algoritma `csp` sebagai `backend` dari web


## Selanjutnya untuk kode `index.html` dan `style.css` yang menjadi `front-end` dari web

Pertama inisiasi `head` dari `html` nya <br>

```c
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuis Produk Skincare</title>
    <link rel="stylesheet" href="../static/style.css"> <!-- Link ke CSS -->
</head>
```

lalu untuk `body` akan berisi pertanyaan-pertanyaan dengan metode `post` untuk mendapatkan informasi

```c
<body>
    <div class="form-container">
        <h2>Kuis Produk Skincare</h2>
        <form id="skincare-form" action="/" method="post">

            <!-- Pertanyaan 1: Produk yang ingin dicari -->
            <div class="question active" id="question1">
                <label for="produk">Apa produk yang ingin Anda cari?</label>
                <select id="produk" name="produk">
                    <option value="facewash">Facewash</option>
                    <option value="moisturizer">Moisturizer</option>
                    <option value="sunscreen">Sunscreen</option>
                </select>
                <button type="button" onclick="nextQuestion(1)">Selanjutnya</button>
            </div>

            <!-- Pertanyaan 2: Tipe kulit -->
            <div class="question" id="question2">
                <label for="tipe_kulit">Apa tipe kulit Anda?</label>
                <select id="tipe_kulit" name="tipe_kulit">
                    <option value="normal">Normal</option>
                    <option value="kering">Kering</option>
                    <option value="berminyak">Berminyak</option>
                    <option value="sensitif">Sensitif</option>
                    <option value="All Skin Type">All Skin Type</option>
                </select>
                <button type="button" onclick="nextQuestion(2)">Selanjutnya</button>
            </div>

            <!-- Pertanyaan 3: Masalah kulit (Multiple Choice) -->
            <div class="question" id="question3">
                <label for="masalah_kulit">Apakah Anda memiliki masalah kulit tertentu? (Pilih semua yang sesuai)</label>
                <div class="checkbox-group">
                    <div>
                        <input type="checkbox" id="hiperpigmentasi" name="masalah_kulit" value="hiperpigmentasi">
                        <label for="hiperpigmentasi">Hiperpigmentasi</label>
                    </div>
                    <div>
                        <input type="checkbox" id="jerawat" name="masalah_kulit" value="jerawat">
                        <label for="jerawat">Jerawat</label>
                    </div>
                    <div>
                        <input type="checkbox" id="kemerahan" name="masalah_kulit" value="kemerahan">
                        <label for="kemerahan">Kemerahan</label>
                    </div>
                    <div>
                        <input type="checkbox" id="garis_halus" name="masalah_kulit" value="garis_halus">
                        <label for="garis_halus">Garis Halus</label>
                    </div>
                    <div>
                        <input type="checkbox" id="tidak_ada" name="tidak_ada" value="tidak_ada">
                        <label for="tidak_ada">Tidak Ada</label>
                    </div>
                </div>
                <button type="button" onclick="nextQuestion(3)">Selanjutnya</button>
            </div>

            <!-- Pertanyaan 4: Reaksi terhadap bahan (Multiple Choice) -->
            <div class="question" id="question4">
                <label for="reaksi_bahan">Apakah kulit Anda cenderung bereaksi terhadap bahan tertentu? (Pilih semua yang sesuai)</label>
                <div class="checkbox-group">
                    <div>
                        <input type="checkbox" id="alkohol" name="reaksi_bahan" value="alkohol">
                        <label for="alkohol">Alkohol</label>
                    </div>
                    <div>
                        <input type="checkbox" id="fragrance" name="reaksi_bahan" value="fragrance">
                        <label for="fragrance">Fragrance</label>
                    </div>
                    <div>
                        <input type="checkbox" id="paraben" name="reaksi_bahan" value="paraben">
                        <label for="paraben">Paraben</label>
                    </div>
                    <div>
                        <input type="checkbox" id="tidak_ada" name="reaksi_bahan" value="tidak_ada">
                        <label for="tidak_ada">Tidak Ada</label>
                    </div>
                </div>
                <button type="button" onclick="nextQuestion(4)">Selanjutnya</button>
            </div>

            <!-- Pertanyaan 5: Fungsi tambahan produk -->
            <div class="question" id="question5">
                <label for="fungsi_tambahan">Apakah Anda mencari produk yang memiliki fungsi tambahan?</label>
                <div class="checkbox-group">
                    <div>
                        <input type="checkbox" id="anti_aging" name="fungsi_tambahan" value="anti_aging">
                        <label for="anti_aging">Anti-aging</label>
                    </div>
                    <div>
                        <input type="checkbox" id="brightening" name="fungsi_tambahan" value="brightening">
                        <label for="brightening">Brightening</label>
                    </div>
                    <div>
                        <input type="checkbox" id="acne_fighting" name="fungsi_tambahan" value="acne_fighting">
                        <label for="acne_fighting">Acne-fighting</label>
                    </div>
                    <div>
                        <input type="checkbox" id="tidak_ada" name="fungsi_tambahan" value="tidak_ada">
                        <label for="acne_fighting">Tidak-Ada</label>
                    </div>
                </div>
                <button type="button" onclick="nextQuestion(5)">Selanjutnya</button>
            </div>

            <!-- Pertanyaan 6: Rentang budget -->
            <div class="question" id="question6">
                <label for="budget">Kamu punya rentang budget berapa?</label>
                <select id="budget" name="budget">
                    <option value="under_50k">Rp 0 - Rp 50.000</option>
                    <option value="50_100k">Rp 50.000 - Rp 100.000</option>
                    <option value="100_200k">Rp 100.000 - Rp 200.000</option>
                    <option value="up_to_200k">Rp 200.000+</option>
                </select>
                <button type="submit">Kirim</button>
            </div>
        </form>
```

Lalu selanjutnya untuk memunculkan hasil. <br> <br>

Misal produk tidak ditemukan : <br> 

```c
<!-- Menampilkan Pesan Tidak Ditemukan -->
        {% if no_results_message %}
            <div class="alert alert-warning mt-4">
                {{ no_results_message }}
            </div>
        {% endif %}
```

Misal produk ditemukan : <br>

```c
<!-- Display Results after Quiz -->
        {% if filtered_data %}
        <div class="results">
            <h3>Hasil Pencarian Produk</h3>
            <table>
                <thead>
                    <tr>
                        <th>Brand</th>
                        <th>Nama Produk</th>
                        <th>Kategori</th>
                        <th>Tipe Kulit</th>
                        <th>Bahan</th>
                        <th>Harga</th>
                        <th>Link Pembelian</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in filtered_data %}
                    <tr>
                        <td>{{ item['Brand'] }}</td>
                        <td>{{ item['NamaProduk'] }}</td>
                        <td>{{ item['Kategori'] }}</td>
                        <td>{{ item['SkinType'] }}</td>
                        <td>{{ item['Ingredients'] }}</td>
                        <td>{{ item['Harga'] }}</td>
                        <td>
                            <a href="{{ item['Link'] }}" target="_blank" rel="noopener noreferrer">Beli di sini</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <br>
            <!-- Tombol Mulai Lagi -->
            <button class="play-again" onclick="window.location.href = '/'">Mulai Lagi</button>
        </div>
        {% endif %}
    </div>
```

Lalu selanjutnya untuk `script` sebagai animasinya

```c
    <script>
        // Fungsi untuk menampilkan pertanyaan berikutnya
        function nextQuestion(currentQuestion) {
            const current = document.getElementById('question' + currentQuestion);
            current.classList.remove('active');
            const next = document.getElementById('question' + (currentQuestion + 1));
            if (next) {
                next.classList.add('active');
            }
        }
    </script>
```

Lalu berikut untuk penjelasan kode `style.css`

```c
body {
    font-family: Arial, sans-serif;
    background-color: #FCF4B3; /* Light background */
    margin: 0;
    padding: 0;
}

.form-container {
    width: 90%; /* Ubah dari max-width ke width agar form mengambil 90% dari lebar layar */
    margin: 50px auto;
    padding: 20px;
    background-color: #FFFFFF; /* White background for the form */
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
}

h2 {
    text-align: center;
    color: #F78B93; /* Main color for headings */
}

.question {
    display: none; /* Hide all questions initially */
}

.question.active {
    display: block; /* Show the active question */
}

label {
    display: block;
    margin-bottom: 10px;
    color: #8CB9EA; /* Color for labels */
    font-size: 16px;
}

input[type="text"], input[type="number"], select {
    width: 100%;
    padding: 12px;
    margin-bottom: 20px;
    border: 1px solid #84DBFF; /* Light blue border */
    border-radius: 5px;
    font-size: 16px; /* Increase font size for better readability */
    background-color: #fff; /* White background for the select */
    color: #333; /* Dark text for better contrast */
    text-align: left;
}

.checkbox-group {
    margin-bottom: 20px;
}

.checkbox-group div {
    display: flex;
    align-items: center; /* Vertically align checkbox and label */
    margin-bottom: 10px;
}

.checkbox-group input[type="checkbox"] {
    margin-right: 10px; /* Space between checkbox and label */
}

.checkbox-group label {
    font-size: 14px; /* Adjust font size for checkbox labels */
    margin: 0;
    display: inline; /* Ensure label is inline with checkbox */
}

select[multiple] {
    height: 150px; /* Adjust height for multiple select dropdown */
    overflow-y: auto;
}

@media (max-width: 768px) {
    .form-container {
        padding: 15px;
    }

    button {
        padding: 10px;
    }

    label {
        font-size: 14px;
    }
}

button {
    background-color: #F78B93; /* Button color */
    color: white;
    border: none;
    padding: 12px 18px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-size: 16px;
    margin-top: 10px;
    width: 100%;
}

button:hover {
    background-color: #FCF4B3; /* Change on hover */
    color: #F78B93; /* Change text color on hover */
}

/* Results Section */
.results {
    width: 90%; /* Set width to 90% of the screen */
    margin: 30px auto;
    padding: 30px;
    background-color: #FFFFFF; /* White background for the results */
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    overflow-x: auto; /* Ensures content doesn't overflow horizontally */
}

/* Styling untuk Tabel Hasil */
table {
    width: 100%; /* Ensure table takes up full width */
    border-collapse: collapse;
    table-layout: fixed; /* Ensure table columns are evenly distributed */
}

th, td {
    padding: 15px; /* Increase padding for table cells */
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #F78B93; /* Light pink for header */
    color: white;
    font-weight: bold;
    margin-top: 30cm;
}

td {
    background-color: #F9F9F9;
}

td:hover {
    background-color: #FCF4B3; /* Highlight row when hovered */
}

/* Tombol Mulai Lagi */
button.play-again {
    background-color: #F78B93; /* Warna pink */
    color: white;
    border: none;
    padding: 12px 18px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-size: 16px;
    margin-top: 20px;
    width: 100%;
}

button.play-again:hover {
    background-color: #FCF4B3; /* Warna kuning terang saat hover */
    color: #F78B93; /* Warna teks menjadi pink saat hover */
}

.alert-warning {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 100%;
    margin-top: 20px;
    background-color: #ffdddd; /* Ubah warna background sesuai kebutuhan */
    color: #d9534f; /* Ubah warna text jika perlu */
}
```

# Sekian Terimakasih