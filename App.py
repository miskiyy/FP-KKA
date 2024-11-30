from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Fungsi untuk memuat data dari CSV berdasarkan produk
def load_data(produk_pilihan):
    if produk_pilihan == 'facewash':
        return pd.read_csv('dataset/Facewash.csv')
    elif produk_pilihan == 'moisturizer':
        return pd.read_csv('dataset/Moisturizer.csv')
    elif produk_pilihan == 'sunscreen':
        return pd.read_csv('dataset/Sunscreen.csv')
    else:
        return None

# Fungsi untuk mendapatkan rekomendasi produk
def get_recommendations(data, skin_type, masalah_kulit, reaksi_bahan, fungsi_tambahan, budget):
    # Gabungkan fitur yang relevan untuk dibandingkan
    data['combined_features'] = data['SkinType'] + " " + data['Ingredients'] + " " + data['Category']
    
    # Vectorize fitur gabungan
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['combined_features'])
    
    # Buat query pengguna
    user_query = f"{skin_type} {' '.join(masalah_kulit)} {' '.join(reaksi_bahan)} {' '.join(fungsi_tambahan)} {budget}"
    user_query_vec = tfidf.transform([user_query])
    
    # Hitung cosine similarity antara input pengguna dan dataset
    cosine_similarities = cosine_similarity(user_query_vec, tfidf_matrix).flatten()
    data['similarity'] = cosine_similarities
    
    # Urutkan berdasarkan similarity tertinggi
    recommended_products = data.sort_values(by='similarity', ascending=False)
    
    # Format harga menjadi angka dan hilangkan simbol "Rp"
    recommended_products['Price'] = recommended_products['Price'].replace({' Rp ': '', ',': ''}, regex=True).astype(float)
    
    # Filter berdasarkan budget
    if budget == 'under_50k':
        recommended_products = recommended_products[recommended_products['Price'] <= 50000]
    elif budget == '50_100k':
        recommended_products = recommended_products[(recommended_products['Price'] > 50000) & (recommended_products['Price'] <= 100000)]
    elif budget == '100_200k':
        recommended_products = recommended_products[(recommended_products['Price'] > 100000) & (recommended_products['Price'] <= 200000)]
    elif budget == 'up_to_200k':
        recommended_products = recommended_products[recommended_products['Price'] > 200000]
    
    return recommended_products.head(5)  # Mengambil 5 produk terbaik


# Route untuk halaman index (form)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Mengambil data dari form
        produk_pilihan = request.form.get("produk")
        tipe_kulit = request.form.get("tipe_kulit")
        masalah_kulit = request.form.getlist("masalah_kulit")
        reaksi_bahan = request.form.getlist("reaksi_bahan")
        fungsi_tambahan = request.form.getlist("fungsi_tambahan")
        budget = request.form.get("budget")

        # Memuat dataset berdasarkan produk yang dipilih
        dataset = load_data(produk_pilihan)
        if dataset is None:
            return "Dataset tidak ditemukan", 404

        # Mendapatkan rekomendasi produk berdasarkan input
        recommended_products = get_recommendations(
            dataset, tipe_kulit, masalah_kulit, reaksi_bahan, fungsi_tambahan, budget
        )

        # Render halaman result dengan data produk yang direkomendasikan
        return render_template("result.html", recommended_products=recommended_products)

    # Render halaman index saat pertama kali dibuka
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
