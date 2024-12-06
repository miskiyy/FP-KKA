from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Set secret key untuk session
app.secret_key = 'windut_cantik'

# Load data CSV
data_path = 'dataskin.csv'
df = pd.read_csv(data_path, quotechar='"')  # Menangani tanda kutip ganda

# Price filter ranges
price_filter = {
    "under_50k": (0, 50000),
    "50_100k": (51000, 100000),
    "100_200k": (101000, 200000),
    "up_to_200k": (201000, 1000000)
}

@app.route("/", methods=["GET", "POST"])
def home():
    filtered_data = []
    no_results_message = ""  # Pesan jika tidak ada produk yang ditemukan
    
    # Ingredients filter sesuai masalah kulit
    ingredients_filter = {
        "hiperpigmentasi": ["Vitamin C", "Ascorbic Acid", "Niacinamide", "Arbutin", "Licorice Extract", "Kojic Acid", "Glycolic Acid", "Salicylic Acid", "Lactic Acid", "Azelaic Acid", "Mulberry Extract", "Green Tea Extract", "Papaya Enzyme", "Retinoid", "Retinol", "Ceramides", "Hyaluronic Acid"],
        "jerawat": ["Salicylic Acid", "Benzoyl Peroxide", "Tea Tree Oil", "Niacinamide", "Zinc PCA", "Centella Asiatica", "Aloe Vera", "Ceramides", "Green Tea Extract", "Hyaluronic Acid", "Zinc Oxide", "Titanium Dioxide", "Vitamin E"],
        "kemerahan": ["Centella Asiatica", "Niacinamide", "Aloe Vera", "Green Tea Extract", "Chamomile Extract", "Panthenol", "Allantoin", "Licorice Extract", "Ceramides", "Calendula Extract", "Beta Glucan", "Bisabolol", "Zinc Oxide", "Vitamin E", "Squalane"],
        "garis_halus": ["Retinol", "Retinoid", "Peptides", "Hyaluronic Acid", "Vitamin C", "Niacinamide", "Bakuchiol", "Ceramides", "Collagen", "Coenzyme Q10 (CoQ10)", "Alpha Hydroxy Acids (AHA)", "Lactic Acid", "Glycolic Acid", "Squalane", "Panthenol", "Vitamin E"],
    }

    # Filter bahan-bahan yang ingin dihindari (reaksi bahan)
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

    # Filter bahan-bahan untuk fungsi tambahan
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
    
    if request.method == "POST":
        try:
            # Ambil data dari form
            produk = request.form.get("produk")        # Kategori produk (misal: Facewash)
            tipe_kulit = request.form.get("tipe_kulit") # Jenis kulit (misal: Berminyak)
            masalah_kulit = request.form.getlist("masalah_kulit")  # Masalah kulit (misal: jerawat)
            reaksi_bahan = request.form.getlist("reaksi_bahan")  # Reaksi terhadap bahan
            fungsi_tambahan = request.form.getlist("fungsi_tambahan")  # Fungsi tambahan yang dipilih
            harga_range = request.form.get("harga_range")  # Range harga

            # Mulai dengan filter berdasarkan kategori dan tipe kulit
            filtered_df = df.copy()

            # Filter berdasarkan kategori produk
            if produk:
                filtered_df = filtered_df[filtered_df["Kategori"].str.contains(produk, case=False, na=False)]

            # Filter berdasarkan tipe kulit
            if tipe_kulit and tipe_kulit != "All Skin Type":
                filtered_df = filtered_df[filtered_df["SkinType"].str.contains(tipe_kulit, case=False, na=False)]

            # Jika tidak ada produk setelah filter kategori dan tipe kulit, kirim pesan dan hentikan
            if filtered_df.empty:
                no_results_message = "Produk tidak ditemukan berdasarkan kategori dan tipe kulit yang dipilih."
                return render_template("index.html", filtered_data=filtered_data, no_results_message=no_results_message)

            # Sekarang filter berdasarkan masalah kulit dan ingredients terkait, hanya jika masih ada produk
            if masalah_kulit:
                matched_ingredients = []
                for masalah in masalah_kulit:
                    matched_ingredients.extend(ingredients_filter.get(masalah, []))  # Ambil ingredients sesuai masalah kulit
                # Filter berdasarkan ingredients yang relevan dengan masalah kulit
                if matched_ingredients:
                    filtered_df = filtered_df[filtered_df["Ingredients"].str.contains("|".join(matched_ingredients), case=False, na=False)]

            # Filter berdasarkan reaksi bahan (alkohol, fragrance, paraben)
            if reaksi_bahan:
                for bahan in reaksi_bahan:
                    if bahan in reaksi_bahan_filter:  # Cek jika bahan ada di filter
                        bahan_list = reaksi_bahan_filter[bahan]
                        # Exclude produk yang mengandung bahan yang dipilih
                        filtered_df = filtered_df[~filtered_df["Ingredients"].str.contains("|".join(bahan_list), case=False, na=False)]

            # Filter berdasarkan fungsi tambahan (anti-aging, brightening, acne-fighting)
            if fungsi_tambahan:
                for fungsi in fungsi_tambahan:
                    if fungsi in fungsi_tambahan_filter:  # Cek jika fungsi ada di filter
                        fungsi_list = fungsi_tambahan_filter[fungsi]
                        # Include hanya produk yang mengandung fungsi tambahan yang dipilih
                        filtered_df = filtered_df[filtered_df["Ingredients"].str.contains("|".join(fungsi_list), case=False, na=False)]

            # Filter berdasarkan harga jika ada pilihan
            if harga_range and harga_range in price_filter:
                min_price, max_price = price_filter[harga_range]
                filtered_df = filtered_df[(filtered_df["Harga"] >= min_price) & (filtered_df["Harga"] <= max_price)]

            # Setelah semua filter, ubah DataFrame menjadi list of dictionaries
            filtered_data = filtered_df.to_dict(orient="records")

            # Jika masih kosong setelah filtering ingredients, beri pesan
            if not filtered_data:
                no_results_message = "Produk tidak ditemukan berdasarkan kriteria yang dipilih."

        except Exception as e:
            print(f"Error: {e}")
            no_results_message = "Terjadi kesalahan saat memproses pencarian."

    return render_template("index.html", filtered_data=filtered_data, no_results_message=no_results_message)


if __name__ == "__main__":
    app.run(debug=True)
