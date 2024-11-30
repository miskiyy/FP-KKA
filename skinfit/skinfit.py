from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Baca dataset
dataset = pd.read_csv('D:/skinfit/dataskin.csv')
dataset.columns = dataset.columns.str.strip()  # Bersihkan spasi pada nama kolom
dataset['Price'] = dataset['Price'].str.replace("Rp", "").str.replace(",", "").str.strip()
dataset['Price'] = pd.to_numeric(dataset['Price'], errors='coerce')

# Filter custom untuk format mata uang
@app.template_filter('format_currency')
def format_currency(value):
    return f"Rp{value:,.0f}".replace(",", ".")  # Format sebagai Rupiah dengan pemisah ribuan titik

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        # Ambil input dari form
        skin_type = request.form['skin_type']
        category = request.form['category']
        
        # Filter dataset berdasarkan skin type dan category
        filtered_data = dataset[
            (dataset['SkinType'].str.contains(skin_type, case=False, na=False)) & 
            (dataset['Category'].str.lower() == category.lower())
        ]

        if not filtered_data.empty:
            results = filtered_data.to_dict('records')
        else:
            results = [{"message": "Tidak ada rekomendasi yang sesuai dengan kriteria Anda."}]

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
