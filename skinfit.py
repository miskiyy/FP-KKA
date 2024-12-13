from flask import Flask, render_template, request
import pandas as pd
from constraint import Problem

app = Flask(__name__)

# Load data CSV
data_path = 'dataskin.csv'
df = pd.read_csv(data_path, quotechar='"')

@app.route("/", methods=["GET", "POST"])
def home():
    filtered_data = []
    no_results_message = ""

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

    # Price filter ranges
    price_filter = {
        "under_50k": (0, 50000),
        "50_100k": (51000, 100000),
        "100_200k": (101000, 200000),
        "up_to_200k": (201000, 1000000)
    }

    if request.method == "POST":
        try:
            # Salin DataFrame asli
            filtered_df = df.copy()

            # Ambil data dari form
            produk = request.form.get("produk")  # Kategori produk
            tipe_kulit = request.form.get("tipe_kulit")  # Jenis kulit
            masalah_kulit = request.form.getlist("masalah_kulit")  # Masalah kulit
            reaksi_bahan = request.form.getlist("reaksi_bahan")  # Reaksi terhadap bahan
            fungsi_tambahan = request.form.getlist("fungsi_tambahan")  # Fungsi tambahan
            harga = request.form.getlist("budget")  # budget

            # CSP Setup
            problem = Problem()

            # Variabel CSP
            problem.addVariable("Produk", filtered_df["Kategori"].unique())
            problem.addVariable("SkinType", filtered_df["SkinType"].unique())
            problem.addVariable("Ingredients", filtered_df["Ingredients"])
            problem.addVariable("Harga", filtered_df["Harga"].unique())

            # Constraints
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

            # Rentang harga
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

            # Cari solusi
            solutions = problem.getSolutions()

            # Cari solusi
            solutions = problem.getSolutions()

            # Filter DataFrame berdasarkan solusi
            if solutions:
                solution_ingredients = [sol["Ingredients"] for sol in solutions]
                filtered_df = filtered_df[filtered_df["Ingredients"].isin(solution_ingredients)]
                
                # Filter lebih lanjut berdasarkan kategori produk yang dipilih
                if produk:
                    filtered_df = filtered_df[filtered_df["Kategori"].str.lower() == produk.lower()]
                
                # Filter lebih lanjut berdasarkan tipe kulit yang dipilih
                if tipe_kulit:
                    if tipe_kulit == "All Skin Type":
                        # Jika tipe kulit "All Skin Type", tampilkan produk yang hanya memiliki "All Skin Type"
                        filtered_df = filtered_df[filtered_df["SkinType"].str.strip() == "All Skin Type"]
                    else:
                        # Untuk tipe kulit lain seperti "normal", "kering", "berminyak", "sensitif"
                        filtered_df = filtered_df[filtered_df["SkinType"].str.lower() == tipe_kulit.lower()]

                # Filter berdasarkan masalah kulit yang dipilih
                if masalah_kulit:
                    filtered_df = filtered_df[filtered_df["Ingredients"].apply(
                        lambda x: any(ingredient.lower() in x.lower() for ingredient in matched_ingredients)
                    )]

                # Cek apakah ada hasil setelah filter
                if filtered_df.empty:
                    no_results_message = "Produk tidak ditemukan berdasarkan kriteria yang dipilih."
                else:
                    # Convert filtered DataFrame to dictionary
                    filtered_data = filtered_df.to_dict(orient="records")

                # Debugging log jika tidak ada produk
                if not filtered_data:
                    print("No products found!")


        except Exception as e:
            print(f"Error: {e}")
            no_results_message = "Terjadi kesalahan saat memproses pencarian."

    return render_template("index.html", filtered_data=filtered_data, no_results_message=no_results_message)

if __name__ == "__main__":
    app.run(debug=True)